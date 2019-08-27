import re
import sublime
import webbrowser
from collections.abc import Iterable
from .Globals import global_get
from .libs import triegex
from .log import log
from .settings import get_setting, get_timestamp
from .utils import (
    is_regions_intersected,
    region_expand,
    region_into_st_region_form,
    region_shift,
    simplify_intersected_regions,
)


def open_uri_with_browser(uri: str, browser: str = "") -> None:
    """
    @brief Open the URI with the browser.

    @param uri     The uri
    @param browser The browser
    """

    if not browser:
        browser = get_setting("browser")

    # modify browser to None to use the system's default
    if browser == "":
        browser = None

    try:
        # https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
        webbrowser.get(browser).open(uri, autoraise=True)
    except Exception as e:
        log(
            "critical",
            'Failed to open browser "{browser}" to "{uri}" '
            "because {reason}".format(browser=browser, uri=uri, reason=e),
        )


def compile_uri_regex() -> tuple:
    """
    @brief Get the compiled regex object for matching URIs.

    @return (activated schemes, compiled regex object)
    """

    detect_schemes = get_setting("detect_schemes")
    uri_path_regexes = get_setting("uri_path_regexes")

    activated_schemes = []
    uri_regexes = []
    for scheme, scheme_settings in detect_schemes.items():
        if not scheme_settings.get("enabled", False):
            continue

        path_regex_name = scheme_settings.get("path_regex", "@default")
        if path_regex_name not in uri_path_regexes:
            log(
                "warning",
                'Ignore scheme "{scheme}" due to invalid "path_regex": {path_regex}'.format(
                    scheme=scheme, path_regex=path_regex_name
                ),
            )
            continue

        activated_schemes.append(scheme)
        uri_regexes.append(re.escape(scheme) + r"(?:(?#{}))".format(path_regex_name))

    regex = r"\b" + (
        triegex.Triegex(*uri_regexes)
        .to_regex()
        .replace(r"\b", "")
        .replace(r"|~^(?#match nothing)", "")
    )

    log("debug", "Optimized URI matching regex (before expanding): {}".format(regex))

    # expand path regexes by their names
    for path_regex_name, path_regex in uri_path_regexes.items():
        regex = regex.replace(r"(?#{})".format(path_regex_name), path_regex)

    log("debug", "Optimized URI matching regex: {}".format(regex))

    try:
        regex_obj = re.compile(regex, re.IGNORECASE)
    except Exception as e:
        log(
            "critical",
            "Cannot compile regex `{regex}` because `{reason}`. "
            'Please check "uri_path_regex" in plugin settings.'.format(regex=regex, reason=e),
        )

    return regex_obj, sorted(activated_schemes)


def find_uri_regions_by_region(view: sublime.View, region, search_radius: int = 200) -> list:
    """
    @brief Found intersected URI regions from view by the region

    @param view   The view
    @param region The region

    @return list[sublime.Region] Found URI regions
    """

    return find_uri_regions_by_regions(view, [region], search_radius)


def find_uri_regions_by_regions(
    view: sublime.View, regions: Iterable, search_radius: int = 200
) -> list:
    """
    @brief Found intersected URI regions from view by regions

    @param view    The view
    @param regions The regions

    @return list[sublime.Region] Found URI regions
    """

    regions = sorted(map(region_into_st_region_form, regions))
    search_regions = simplify_intersected_regions(
        (region_expand(region, search_radius) for region in regions), True
    )

    uri_regions = []
    for region in search_regions:
        coordinate_bias = max(0, region.begin())

        uri_regions.extend(
            # convert "finditer()" coordinate into ST's coordinate
            sublime.Region(*region_shift(m.span(), coordinate_bias))
            for m in global_get("uri_regex_obj").finditer(view.substr(region))
        )

    # only pick up "uri_region"s that are intersected with "regions"
    # note that both "regions" and "uri_regions" are guaranteed sorted here
    regions_idx = 0
    uri_regions_intersected = []

    for uri_region in uri_regions:
        for idx in range(regions_idx, len(regions)):
            region = regions[idx]

            # later "uri_region" is always even larger so this "idx" is useless since now
            if uri_region.begin() > region.end():
                regions_idx = idx + 1

            if is_regions_intersected(uri_region, region, True):
                uri_regions_intersected.append(uri_region)

                break

    return uri_regions_intersected


def view_last_typing_timestamp_val(view: sublime.View, timestamp_s=...):
    """
    @brief Set/Get the last timestamp (in sec) when "OUIB_uri_regions" is updated

    @param view        The view
    @param timestamp_s The last timestamp (in sec)

    @return Optional[float] None if the set mode, otherwise the value
    """

    if timestamp_s is ...:
        return view.settings().get("OUIB_last_update_timestamp", False)

    view.settings().set("OUIB_last_update_timestamp", timestamp_s)


def view_is_dirty_val(view: sublime.View, is_dirty=...):
    """
    @brief Set/Get the is_dirty of the current view

    @param view     The view
    @param is_dirty Indicates if dirty

    @return Optional[bool] None if the set mode, otherwise the is_dirty
    """

    if is_dirty is ...:
        return view.settings().get("OUIB_is_dirty", True)

    view.settings().set("OUIB_is_dirty", is_dirty)


def is_view_typing(view: sublime.View) -> bool:
    """
    @brief Determine if the view typing.

    @param view The view

    @return True if the view is typing, False otherwise.
    """

    now_s = get_timestamp()
    pass_ms = (now_s - view_last_typing_timestamp_val(view)) * 1000

    return pass_ms < get_setting("typing_period")


def is_view_too_large(view: sublime.View) -> bool:
    """
    @brief Determine if the view is too large. Note that size will be 0 if the view is loading.

    @param view The view

    @return True if the view is too large, False otherwise.
    """

    return view.size() > get_setting("large_file_threshold")
