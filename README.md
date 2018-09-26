ReaSyntax
=========

[Sublime text](http://www.sublimetext.com/3) syntax package for scripting languages found in [Cockos REAPER](http://www.reaper.fm/): Jesusonic/EEL/WALTER

A lot of effort has been invested in this. If you seriously use it, please consider [supporting the developer :heart::heart::heart:](http://www.paypal.me/ReaBreeder)



## Installation

#### Using Package Control
 * Install [Package Control](http://sublime.wbond.net/installation)
 * Use `Cmd+Shift+P` or `Ctrl+Shift+P` and search for `Package Control: Install Package`
 * Wait for Package Control to download latest package list and search for `ReaSyntax`

#### Download manually
 * Download zipped repository from [here](https://github.com/Breeder/ReaSyntax/archive/master.zip)
 * Unzip the files and rename the folder to `ReaSyntax`
 * Find your `Packages` directory using the menu item  `Preferences -> Browse Packages...`
 * Copy the folder into your Sublime Text `Packages` directory

#### Using git
 * Find your `Packages` directory using the menu item  `Preferences -> Browse Packages...`
 * While inside the `Packages` directory, clone the repository using the command: `git clone https://github.com/Breeder/ReaSyntax/ "ReaSyntax"`

## Features
##### Syntax for 3 languages found in REAPER:
 * [JS](http://www.reaper.fm/sdk/js/js.php) - scripting language which is compiled on the fly and allows you to modify and/or generate audio and MIDI, as well as draw custom vector based UI and analysis displays.

 * [ReaScript/EEL](http://www.reaper.fm/sdk/reascript/reascript.php) - REAPER lets you use both [Python](https://www.python.org/) and its own language EEL to create scripts that can call any action and use most of the API functions. EEL looks a lot like JS _(good part of JS reference is valid for EEL)_ and is implemented natively in REAPER so there are no dependencies to run EEL scripts. It also appears to run somewhat faster than Python.

 * [WALTER](http://www.reaper.fm/sdk/walter/walter.php) - enables definition of visual layout and appearance of objects within REAPER -- currently, it can be used to customize the layout and appearance of the track panels, mixer panels, envelope panels, transport etc...

##### Auto complete:
ReaSyntax includes completions for all built-in functions and their parameters (JS and EEL). WALTER completions consist of all possible keywords.

##### Additional color schemes:
 * Default - Modification of built-in Monokai Bright made to work a bit better with supplied syntax
 * JS Editor - Replica of the built-in JS Editor found in REAPER

##### Automatic detection of JS files:
JS files have no file extension, but ReaSyntax can detect JS file directly from the file content. The feature is enabled by default but can be turned off in package settings.

Open `Preferences -> Package Settings -> ReaSyntax -> Settings - User` and set `"detect_js_file:"` to `true` or `false`.
For examples, go to `Preferences -> Package Settings -> ReaSyntax -> Settings - Default`

##### Automatically load color schemes for each syntax individually:
Open `Preferences -> Package Settings -> ReaSyntax -> Settings - User` and set `"color_scheme_js"`, `"color_scheme_eel"` or `"color_scheme_walter"` to color scheme you would like to use with that specific syntax.
If you would like to use currently selected color scheme (in `Preferences -> Color Scheme`) just set those to `null`.

For examples, go to `Preferences -> Package Settings -> ReaSyntax -> Settings - Default`

## Screenshots
* EEL Syntax using Default color scheme:
  ![EEL Syntax using Default color scheme](http://stash.reaper.fm/20871/EEL%20-%20Default.png)

* JS Syntax using JS Editor color scheme:
  ![EEL Syntax using JS Editor color scheme](http://stash.reaper.fm/20872/JS%20-%20JS%20Editor.png)

* WALTER Syntax using Default color scheme:
  ![EEL Syntax using Default color scheme](http://stash.reaper.fm/20873/WALTER%20-%20Default.png)
