import sublime, sublime_plugin
import ntpath
import os


# ---------------------------------------------------------------------------------------------------------------------
PACKAGE_SETTINGS = "ReaSyntax.sublime-settings"
JS_SETTINGS      = "ReaSyntax - JS.sublime-settings"
EEL_SETTINGS     = "ReaSyntax - EEL.sublime-settings"
WALTER_SETTINGS  = "ReaSyntax - WALTER.sublime-settings"
JS_SYNTAX        = "Packages/ReaSyntax/ReaSyntax - JS.tmLanguage"
LUA_COMPLETIONS  = "ReaSyntax - Lua completions.sublime-settings"
#PY_COMPLETIONS   = "ReaSyntax - Python completions.sublime-settings"


# ---------------------------------------------------------------------------------------------------------------------
class ReaSyntax:

	detectJs = False

	luaScriptsPath = None
	luaCompletions = []
	#pythonScriptsPath = None
	#pythonCompletions = []

	lastUsedCompletions        = []
	lastCheckedCompletionsFile = None

	@classmethod
	def Init (cls):

		# Load package settings
		cls.settings = sublime.load_settings(PACKAGE_SETTINGS)
		cls.settings.add_on_change(PACKAGE_SETTINGS, cls.SettingsChange)

		# Load specific settings for Lua
		cls.settingsLua = sublime.load_settings(LUA_COMPLETIONS)
		cls.settingsLua.add_on_change(LUA_COMPLETIONS, cls.SettingsChange)

		# Load specific settings for Python
		# cls.settingsPy  = sublime.load_settings(PY_COMPLETIONS)
		# cls.settingsPy.add_on_change(PY_COMPLETIONS, cls.SettingsChange)

		# Apply current settings
		cls.SettingsChange()

	@classmethod
	def SettingsChange (cls):

		# Reset cached completions data
		ReaSyntax.lastUsedCompletions        = []
		ReaSyntax.lastCheckedCompletionsFile = None

		# Load general package settings
		ReaSyntax.detectJs = cls.settings.get("detect_js_file", True)

		# Load Lua completions and paths for files which should have auto completions
#		ReaSyntax.luaScriptsPath = cls.settings.get("lua_scripts_folders", None)
#		ReaSyntax.luaScriptsPath = None if (ReaSyntax.luaScriptsPath is not None and len(ReaSyntax.luaScriptsPath) <= 0) else ReaSyntax.luaScriptsPath
#		del ReaSyntax.luaCompletions[:]
#		if ReaSyntax.luaScriptsPath is not None:
#			ReaSyntax.luaScriptsPath = [""] if ("" in ReaSyntax.luaScriptsPath) else ReaSyntax.luaScriptsPath
#			ReaSyntax.luaCompletions = cls.settingsLua.get("completions", [])

		# Load Python completions and paths for files which should have auto completions
		#ReaSyntax.pythonScriptsPath = cls.settings.get("python_scripts_folders", None)
		#ReaSyntax.pythonScriptsPath = None if (ReaSyntax.pythonScriptsPath is not None and len(ReaSyntax.pythonScriptsPath) <= 0) else ReaSyntax.pythonScriptsPath
		#del ReaSyntax.pythonCompletions[:]
		#if ReaSyntax.pythonScriptsPath is not None:
		#	ReaSyntax.pythonScriptsPath = [""] if ("" in ReaSyntax.pythonScriptsPath) else ReaSyntax.pythonScriptsPath
		#	ReaSyntax.pythonCompletions = cls.settingsLua.get("completions", [])

		# Set color scheme for each syntax
		for i in range(3):
			syntax = (JS_SETTINGS       if (i == 0) else (EEL_SETTINGS       if (i == 1) else  WALTER_SETTINGS))
			key    = ("color_scheme_js" if (i == 0) else ("color_scheme_eel" if (i == 1) else "color_scheme_walter"))

			colorScheme = cls.settings.get(key)
			if (colorScheme):
				sublime.load_settings(syntax).set("color_scheme", colorScheme)
			else:
				sublime.load_settings(syntax).erase("color_scheme")
			sublime.save_settings(syntax)

#	@classmethod
#	def GetCompletions (cls, filePath):
#		completions = []

#		# We cache last requested file path and completion file to skip checks for every call
#		if ReaSyntax.lastCheckedCompletionsFile is not None and ReaSyntax.lastCheckedCompletionsFile == filePath:
#			completions = ReaSyntax.lastUsedCompletions
#		else:

#			# Save this file path as last checked before converting it to real path
#			ReaSyntax.lastCheckedCompletionsFile = filePath
#			filePath = os.path.realpath(filePath)

#			# Get correct path and completions list for current file type
#			fileType  = ntpath.splitext(filePath)[1]
#			pathsList = None
#			if   fileType == ".lua": pathsList = ReaSyntax.luaScriptsPath;    completions = ReaSyntax.luaCompletions
#			#elif fileType == ".py":  pathsList = ReaSyntax.pythonScriptsPath; completions = ReaSyntax.pythonCompletions

#			# Search for current file path in list of allowable paths
#			pathFound = False
#			if pathsList is not None:
#				if ("" in pathsList):
#					pathFound = True
#				else:
#					for path in pathsList:
#						currentPath = os.path.join(os.path.realpath(path), '')
#						if os.path.commonprefix([currentPath, filePath]) == currentPath:
#							pathFound = True
#							break
#			if not pathFound:
#				completions = []

#			# Cache last detected completions
#			ReaSyntax.lastUsedCompletions = completions

#		return completions

# ---------------------------------------------------------------------------------------------------------------------
class EventDump (sublime_plugin.EventListener):

	def on_load (self, view):
		if ReaSyntax.detectJs and ntpath.splitext(view.file_name())[1] == "":

			jsFile = False
			descPos  = view.find("^\\s*desc:", 0)

			# Found "desc:" line, check if it's the first line in the file (omitting comments and empty lines)
			if not descPos.empty():
				if descPos.begin() == 0:
					jsFile = True
				else:
					lastComment = view.find("(^\\s*/\\*([^*]|[\r\n]|(\\*+([^*/]|[\r\n])))*\\*+/)|(^\\s*//.*)|(^\\s*$)", 0)
					if not lastComment.empty() and lastComment.begin() == 0:

						while lastComment.end() < descPos.begin():

							if (lastComment.end() + 1 == descPos.begin()):
								jsFile = True
								break

							comment = view.find("(/^\\s*\\*([^*]|[\r\n]|(\\*+([^*/]|[\r\n])))*\\*+/)|(^\\s*//.*)|(^\\s*$)", lastComment.end())
							if lastComment.end() + 1 != comment.begin(): # There's something between comments, abort
								break
							if (comment.empty()):                        # Reached last comment before "desc:"
								break
							lastComment = comment

			# No match yet, try to find at least 2 code sections
			if not jsFile:
				codeSections = list()
				view.find_all("^@(init|slider|block|sample|serialize|gfx)", 0, "\\1", codeSections)

				# Make sure there isn't more than one code section per type
				if len(codeSections) == len(set(codeSections)) and len(codeSections) >= 2:
					view.set_syntax_file(JS_SYNTAX)

			if jsFile:
				view.set_syntax_file(JS_SYNTAX)

#	def on_query_completions (self, view, prefix, locations):
#		region   = view.line(locations[0])
#		region.b = locations[0]
#		print(view.substr(region))
#		return ReaSyntax.GetCompletions(view.file_name())


# ---------------------------------------------------------------------------------------------------------------------
def plugin_loaded():
	ReaSyntax.Init()

st = 3000 if sublime.version() == '' else int(sublime.version())
if st < 3000:
    plugin_loaded() # won't get called by ST2 automatically so do it manually