ReaSyntax
=========

[Sublime text](http://www.sublimetext.com/3) syntax package for scripting languages found in [Cockos REAPER](http://www.reaper.fm/): Jesusonic/EEL/WALTER

## Features
* Package consists of syntax files for 3 languages found in REAPER:
 * [JS](http://www.reaper.fm/sdk/js/js.php) - scripting language which is compiled on the fly and allows you to modify and/or generate audio and MIDI, as well as draw custom vector based UI and analysis displays.

 * [ReaScript/EEL](http://www.reaper.fm/sdk/reascript/reascript.php) - REAPER lets you use both [Python](https://www.python.org/) and its own language EEL to create scripts that can call any action and use most of the API functions. EEL looks a lot like JS _(good part of JS reference is valid for EEL)_ and is implemented natively in REAPER so there are no dependencies to run EEL scripts. It also appears to run somewhat faster than Python.

 * [WALTER](http://www.reaper.fm/sdk/walter/walter.php) - enables definition of visual layout and appearance of objects within REAPER -- currently, it can be used to customize the layout and appearance of the track panels, mixer panels, envelope panels, transport etc...

* It also includes 2 color schemes:
 * Default - Modification of built-in Monokai Bright
 * JS Editor - Replication of built-in JS Editor found in REAPER

* JS files have no file extensions, but ReaSyntax will try to detect JS file directly from the file content. The feature is enabled by default but can be turn off in package settings.

* Default color scheme for each individual syntax can be set in package settings

## Screenshots
* EEL Syntax using Default color scheme:
  ![EEL Syntax using Default color scheme](https://raw.githubusercontent.com/Breeder/ReaSyntax/master/wiki/EEL%20-%20Default.png)

* JS Syntax using JS Editor color scheme:
  ![EEL Syntax using JS Editor color scheme](https://raw.githubusercontent.com/Breeder/ReaSyntax/master/wiki/JS%20-%20JS%20Editor.png)

* WALTER Syntax using Default color scheme:
  ![EEL Syntax using Default color scheme](https://raw.githubusercontent.com/Breeder/ReaSyntax/master/wiki/WALTER%20-%20Default.png)
