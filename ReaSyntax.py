import sublime, sublime_plugin
import ntpath


# ---------------------------------------------------------------------------------------------------------------------
PACKAGE_SETTINGS = "ReaSyntax.sublime-settings"
JS_SETTINGS      = "ReaSyntax - JS.sublime-settings"
EEL_SETTINGS     = "ReaSyntax - EEL.sublime-settings"
WALTER_SETTINGS  = "ReaSyntax - WALTER.sublime-settings"
JS_SYNTAX        = "Packages/ReaSyntax/ReaSyntax - JS.tmLanguage"


# ---------------------------------------------------------------------------------------------------------------------
class ReaperSyntax:

	detectJs = False

	@classmethod
	def Init (cls):
		cls.settings = sublime.load_settings(PACKAGE_SETTINGS)
		cls.settings.add_on_change(PACKAGE_SETTINGS + "-reaper_test", cls.SettingsChange)
		cls.SettingsChange()

	@classmethod
	def SettingsChange (cls):
		cls.detectJs = cls.settings.get("detect_js_file", True)

		for i in range(3):
			syntax = JS_SETTINGS       if (i == 0) else EEL_SETTINGS       if (i == 1) else  WALTER_SETTINGS
			key    = "color_scheme_js" if (i == 0) else "color_scheme_eel" if (i == 1) else "color_scheme_walter"

			colorScheme = cls.settings.get(key)
			if (colorScheme):
				sublime.load_settings(syntax).set("color_scheme", colorScheme)
			else:
				sublime.load_settings(syntax).erase("color_scheme")
			sublime.save_settings(syntax)


# ---------------------------------------------------------------------------------------------------------------------
class EventDump (sublime_plugin.EventListener):

	def on_load (self, view):
		if ReaperSyntax.detectJs and ntpath.splitext(view.file_name())[1] == "":

			descPos  = view.find("^\\s*desc:", 0)
			jsFile = False

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
							if lastComment.end() + 1 != comment.begin():   # There's something between comments, abort
								break
							if (comment.empty()):                          # Reached last comment before "desc:"
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

# ---------------------------------------------------------------------------------------------------------------------
def plugin_loaded():
	ReaperSyntax.Init()

st = 3000 if sublime.version() == '' else int(sublime.version())
if st < 3000:
    plugin_loaded() # won't get called by ST2 automatically so do it manually