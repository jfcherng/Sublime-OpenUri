# Sublime-OpenUri

<a href="https://www.sublimetext.com"><img alt="Required ST Build" src="https://img.shields.io/badge/ST-Build%203118+-orange.svg?style=flat-square&logo=sublime-text"></a>
<a href="https://travis-ci.org/jfcherng/Sublime-OpenUri"><img alt="Travis (.org) branch" src="https://img.shields.io/travis/jfcherng/Sublime-OpenUri/master?style=flat-square"></a>
<a href="https://packagecontrol.io/packages/OpenUri"><img alt="Package Control" src="https://img.shields.io/packagecontrol/dt/OpenUri?style=flat-square"></a>
<a href="https://github.com/jfcherng/Sublime-OpenUri/tags"><img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/tag/jfcherng/Sublime-OpenUri?style=flat-square&logo=github"></a>
<a href="https://github.com/jfcherng/Sublime-OpenUri/blob/master/LICENSE"><img alt="Project license" src="https://img.shields.io/github/license/jfcherng/Sublime-OpenUri?style=flat-square&logo=github"></a>
<a href="https://github.com/jfcherng/Sublime-OpenUri/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/jfcherng/Sublime-OpenUri?style=flat-square&logo=github"></a>
<a href="https://www.paypal.me/jfcherng/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal"></a>

Finally! A performant and highly customizable URI-opening plugin comes.

![screenshot](https://raw.githubusercontent.com/jfcherng/Sublime-OpenUri/master/docs/screenshot.png)

`OpenUri` is a Sublime Text 3 plugin which provides an easy access to URIs (mostly URLs)
in a file by clicking on a phantom, the popup or key/mouse bindings.


## Bug fix for `PhantomSet`

The official `PhantomSet` implementation before Sublime Text 4 (not released yet) is buggy.
You can fix it by overwriting it with [a patched sublime.py](https://gist.github.com/jfcherng/0ea38bd05a8875be1a40f30b5b9f784c).
Remember, backup `sublime.py` before patching it.

- On Windows: `C:\Program Files\Sublime Text 3\sublime.py`
- On Linux: `/opt/sublime_text/sublime.py`
- On Mac OSX: `/Applications/Sublime Text.app/Contents/MacOS/sublime.py`

Reference: https://github.com/SublimeTextIssues/Core/issues/2897#issuecomment-514868381


## Installation

This plugin is available on Package Control by the name of [OpenUri](https://packagecontrol.io/packages/OpenUri).

Note that this plugin only supports ST >= 3118 because of Phantom API.

💡 You may also be interested in my other plugins: https://packagecontrol.io/search/jfcherng


## Settings

To edit settings, go to `Preferences` » `Package Settings` » `OpenUri` » `Settings`.

I try to make the [settings file](https://github.com/jfcherng/Sublime-OpenUri/blob/master/OpenUri.sublime-settings) 
self-explanatory. But if you still have questions, feel free to open an issue.


## Default Bindings


### Key Binding

- <kbd>Alt + o</kbd>, <kbd>Alt + u</kbd>:
  Open URIs from (multiple) cursors. `o, u` is mnemonic for `Open, URI`.


### Mouse Binding

- <kbd>Ctrl + Right Click</kbd>: Open the clicked URI. (`open_uri_from_cursors`)

You may also add a mouse binding for `select_uri_from_cursors`.
There are just too few modifier keys to be chosen so I am not adding a default one for it.


### How to disable default bindings?

If you do not want those default key/mouse bindings, you can use an empty one to overwrite them.
Or if you want to change them, you can use a non-empty one.

Here I take the default mouse binding as an example.

1. Go to `Preferences` » `Browser Packages...`.
1. Create file `OpenUri/bindings/Default.sublime-mousemap` (and its parent directories if necessary).
1. Fill `Default.sublime-mousemap` with `[]`.
   Then this `Default.sublime-mousemap` will overwrite this plugin's.


## Commands

These commands are always available no matter what `show_open_button` is or how large the file is.

| Command | Functionality |
|---|---|
| open_uri_from_cursors | Open URIs from cursors |
| open_uri_from_view | Open URIs from the current view |
| select_uri_from_cursors | Select URIs from cursors |
| select_uri_from_view | Select URIs from the current view |
