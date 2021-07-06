##### v0.3.8 (July 06 2021)
 * [Lua, EEL] Updated completions to match REAPER 6.30, js_ReaScriptAPI 1.220, ReaImGui 0.5.2, ReaPack 1.2.3.1 and SWS 2.12.1.3

##### v0.3.7 (May 24 2021)
 * [Lua, EEL] Updated completions to match REAPER 6.29, js_ReaScriptAPI 1.220, ReaImGui 0.4, ReaPack 1.2.3.1 and SWS 2.12.1.3

##### v0.3.5 (April 20 2021)
 * [Lua] Removed three completions that were messing with the Sublime Text's auto-complete (Fixes #6):
   * reaper.ImGui_TableFlags_NoHostExtendX()
   * reaper.ImGui_TableFlags_NoHostExtendY()
   * reaper.ImGui_GetTextLineHeightWithSpacing(ImGui_Context ctx)

##### v0.3.4 (April 16 2021)
 * [EEL] Added completions support for extension API (REAPER 6.24 introduced new syntax for extension API functions without using extension_api)
 * [EEL] Added completions back (due to recent changes in REAPER, auto-build script wasn't exporting EEL completions)
 * [Lua] Added completions support for ReaImGui (current version: 0.2)
 * [Lua, EEL] Updated completions to match REAPER 6.27, SWS 2.12.1.3, ReaPack 1.2.3.1 and js_ReaScriptAPI 1.220

##### v0.3.4 (April 16 2021)
 * [EEL] Added completions support for extension API (REAPER 6.24 introduced new syntax for extension API functions without using extension_api)
 * [EEL] Added completions back (due to recent changes in REAPER, auto-build script wasn't exporting EEL completions)
 * [Lua, EEL] Added completions support for ReaImGui (current version: 0.2)
 * [Lua, EEL] Updated completions to match REAPER 6.27, SWS 2.12.1.3, ReaPack 1.2.3.1 and js_ReaScriptAPI 1.220

##### v0.3.3 (March 30 2021)
 * [Lua, EEL] Updated completions to match REAPER 6.26, SWS 2.12.1.3, ReaPack 1.2.3.1 and js_ReaScriptAPI 1.220

##### v0.3.2 (March 07 2021)
 * [Lua, EEL] Updated completions to match REAPER 6.25, SWS 2.12.1.3, ReaPack 1.2.3.1 and js_ReaScriptAPI 1.220

##### v0.3.1 (December 05 2020)
 * [Lua, EEL] Updated completions to match REAPER 6.18, SWS 2.12.1, ReaPack 1.2.3.1 and js_ReaScriptAPI 1.217

##### v0.3.0 (July 08 2020)
 * [Lua, EEL] Updated completions to match REAPER 6.12, SWS 2.12.0 #0, ReaPack 1.2.3 and js_ReaScriptAPI 1.215

##### v0.2.9 (December 04 2019)
 * [Lua, EEL] Updated completions to match REAPER 6.0, SWS 2.11.0 #0, ReaPack 1.2.2 and js_ReaScriptAPI 0.995

##### v0.2.8 (November 03 2019)
 * [Lua, EEL] Updated completions to match REAPER 5.984, SWS 2.10.0 #1, ReaPack 1.2.2 and js_ReaScriptAPI 0.995

##### v0.2.7 (August 18 2019)
 * [Lua, EEL] Updated completions to match REAPER 5.982, SWS 2.10.0 #1, ReaPack 1.2.2 and js_ReaScriptAPI 0.990

##### v0.2.6 (May 01 2019)
 * [Lua, EEL] Updated completions to match REAPER 5.975, SWS 2.10.0 #1, ReaPack 1.2.2 and js_ReaScriptAPI 0.985

##### v0.2.5 (April 10 2019)
 * [JS] Load JS syntax automatically for files with file extenstion ".jsfx"

##### v0.2.4 (April 07 2019)
 * [Lua, EEL] Updated completions to match REAPER 5.974, SWS 2.10.0 #1, ReaPack 1.2.2 and js_ReaScriptAPI 0.980

##### v0.2.3 (March 12 2019)
 * [Lua, EEL] Updated completions to match REAPER 5.973, SWS 2.10.0 #1, ReaPack 1.2.2 and js_ReaScriptAPI 0.972

##### v0.2.2 (February 04 2019)
 * [Lua, EEL] Updated completions to match REAPER 5.965, SWS 2.10.0, ReaPack 1.2.1 and js_ReaScriptAPI 0.963

##### v0.2.1 (September 29 2018)
 * [Lua] Due to bug in Sublime Text API, when using Lua completions, words in current file weren't auto-completed.
         So instead of working on specific folders, auto complete works on all Lua scripts. If you don't want
         REAPER auto-completions for other Lua scripts, simply disable ReaSyntax while editing those files

##### v0.2.0 (September 29 2018)
 * [Lua] Added Lua completion list. All scripts load it - REAPER or not. This can be limited to specific folders through settings
 * [JS, EEL, WALTER] Updated syntax and completion lists to match REAPER 5.96pre12, SWS 2.9.8 and ReaPack 1.2.1
 * [JS, EEL] Fixed indentation

##### v0.1.1 (October 6 2014)
 * [JS, EEL, WALTER] Fixed toggling comments
 * [EEL] Added SetCursorContext() to completion list

##### v0.1.0 (September 21 2014)
 * [JS, EEL, WALTER] Added auto completion for built-in functions (EEL, JS) and keywords (WALTER)
 * [JS, EEL] Fixed local/global/instance parameters
 * [JS, EEL] Added support for namespace function parameters
 * [JS] Fixed slider description when using various characters that were not letters
 * [JS] Added support for gfx_ext_retina, import and options:gmem

##### v0.0.1 (June 5 2014)
 * Initial release