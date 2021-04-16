# --------------------------------------------------------------------------------------------------------------------#
# To add functions from various REAPER extensions (like SWS), they need to be installed in REAPER                     #
#                                                                                                                     #
#   - Note that the easiest way to use this and debug it is to add to REAPER as a script and work from there          #                                                                                                                     #
# --------------------------------------------------------------------------------------------------------------------#
import os.path
import re
from html.parser import HTMLParser

# ---------------------------------------------------------------------------------------------------------------------
PATH_TO_REASCRIPT_API = os.path.expanduser("~") + "\\AppData\\Local\\Temp\\reascripthelp.html"
TARGET_FOLDER         = "C:\\Users\\Martin\\AppData\\Roaming\\Sublime Text 3\\Packages\\ReaSyntax\\"
DEBUG_MODE            = True

# ---------------------------------------------------------------------------------------------------------------------
def msg(m):
	if DEBUG_MODE == True:
		RPR_ShowConsoleMsg(str(m) + "\n")

# ---------------------------------------------------------------------------------------------------------------------
class ApiFunction:
	def __init__ (self, functionSig, language, isBuiltIn):
		self.__funcName          = ""
		self.__returnVars        = []
		self.__returnTypes       = []
		self.__parameterVars     = []
		self.__parameterTypes    = []
		self.__language          = ""
		self.__builtIn           = isBuiltIn
		self.__eelIsExtensionApi = False
		self.__luaGfx            = False
		self.__luaReaperArray    = False

		if   language == "C":      self.__parseCFunc(functionSig);   self._language = language;
		elif language == "EEL":    self.__parseEelFunc(functionSig); self._language = language;
		elif language == "Lua":    self.__parseLuaFunc(functionSig); self._language = language;
		elif language == "Python": self.__parsePyFunc(functionSig,); self._language = language;

	def __parseCFunc (self, functionSig):

		# Get return type
		functionSig = functionSig.split(" ", 1)
		self.__returnTypes.append(functionSig[0].strip())

		# Get function name
		functionSig = functionSig[1].split("(", 1)
		self.__funcName = functionSig[0].strip()

		# Get function parameters
		parameters = functionSig[1].strip().rstrip(")").split(",")
		if len(parameters) > 0 and not (len(parameters) == 1 and parameters[0] == ""):
			for parameter in parameters:
				self.__parameterTypes.append(parameter.rsplit(" ", 1)[0].strip())
				self.__parameterVars.append (parameter.rsplit(" ", 1)[1].strip())

	def __parseEelFunc (self, functionSig):
		functionSig = functionSig.replace(" (requires REAPER 6.24 or later)", "")
		functionSig = functionSig.replace(" (legacy syntax, also useful for allowing script to run when third-party extension is not installed)", "")

		# Check for extension_api which isn't used
		checkExtensionApi = True
		if functionSig == "extension_api(\"function_name\"[,...])":
			checkExtensionApi = False

		# Replace &amp; special entity with & symbol
		functionSig = functionSig.replace("&amp;", "&")

		# Remove [, ...] parameters (they aren't used by auto-complete)
		functionSig = re.sub(r"\[\s*,\s*\.\s*\.\s*\.\s*\]", "", functionSig)

		# Remove optional parameters surrounding brackets (always display all parameters)
		functionSig = functionSig.replace("[", "")
		functionSig = functionSig.replace("]", "")

		# Check if function has return type
		noReturnType = False
		if self.__builtIn or (not self.__builtIn and len(functionSig.split("(", 1)[0].split()) < 2):
			noReturnType = True

		# Get return type (only if not built-in)
		if noReturnType:
			self.__returnTypes.append("void")
		else:
			functionSig = functionSig.split(" ", 1)
			self.__returnTypes.append(functionSig[0].strip())
		self.__returnVars.append("")

		# Get function name
		if noReturnType:
			functionSig = functionSig.split("(", 1)
		else:
			functionSig = functionSig[1].split("(", 1)
		self.__funcName = functionSig[0].strip()

		# Get function parameters
		parameters = functionSig[1].strip().rstrip(")").split(",")
		if len(parameters) > 0 and not (len(parameters) == 1 and parameters[0] == ""):
			for parameter in parameters:

				# EEL function signatures have a few distinct semantics which we "normalize" here to separate type and variable name
				parameterTypeAndVal = parameter.rsplit(" ", 1)
				if len(parameterTypeAndVal) > 0:

					parameterType = ""
					parameterVar  = ""

					# EEL built-in functions never have types written next to them, so ignore for now
					if self.__builtIn:
						parameterVar = parameterTypeAndVal[0].strip()
					else:
						if len(parameterTypeAndVal) < 2:
							parameterVar = parameterTypeAndVal[0].strip()
						else:
							parameterType = parameterTypeAndVal[0].strip()
							parameterVar  = parameterTypeAndVal[1].strip()

					# EEL displays const char* as a text wrapped in quotes
					if (parameterTypeAndVal[0].find("\"") != -1 or (len(parameterTypeAndVal) > 1 and parameterTypeAndVal[1].find("\"") != -1)):
						if parameterTypeAndVal[0].find("\"") != -1:
							parameterVar = parameterTypeAndVal[0].replace("\"", "")
						else:
							parameterVar = parameterTypeAndVal[1].replace("\"", "")
						parameterType = "const char*"

					# Variables without types are treated as doubles and char* variables are stripped of their prefix #
					if parameterType == "":
						parameterType = "char*" if parameterVar.find("#") != -1 else "double"
					parameterVar = parameterVar.replace("#", "")

					# Reference symbol is attached to parameter type, not variable (REAPER names its reference variables clearly enough with suffix "Out")
					if parameterVar.find("&") != -1:
						parameterType += "&"
						parameterVar = parameterVar.replace("&", "")

					# Save "normalized" parameters information
					self.__parameterTypes.append(parameterType.replace("optional ", "").strip())
					self.__parameterVars.append (parameterVar)

					# Check if function is native API or imported from some kind of extension
					if checkExtensionApi:
						if self.__funcName == "extension_api":
							self.__eelIsExtensionApi = True

		# Print end result to console for debugging
		if DEBUG_MODE == True and self.__funcName == "Debug":
			msg(str(self.__returnTypes) + " @@@ " + str(self.__returnVars) + " @@@ " + self.__funcName + " @@@ " + str(self.__parameterTypes) + " @@@ " + str(self.__parameterVars))
			msg(self.__returnTypes)
			msg(self.__returnVars)
			msg(self.__funcName)
			msg(self.__parameterTypes)
			msg(self.__parameterVars)

	def __parseLuaFunc (self, functionSig):
		self.__language = "Lua"

		# Remove [, ...] parameters (they aren't used by auto-complete)
		functionSig = re.sub(r"\[\s*,\s*\.\s*\.\s*\.\s*\]", "", functionSig)

		# Remove optional parameters surrounding brackets (always display all parameters)
		functionSig = functionSig.replace("[", "")
		functionSig = functionSig.replace("]", "")

		# Separate return variables from the rest of the function signature
		functionSig = functionSig.split("reaper.", 1)

		# Get return variables
		if len(functionSig) > 1:
			returnVars = functionSig[0].strip().split(",")
			for typeAndVal in returnVars:
				if typeAndVal.strip() == "" and len(returnVars) == 1:
					self.__returnTypes.append("void")
					self.__returnVars.append("")
					break;
				else:

					# Due to bug in generated html, retval will be appended to one of the return parameters if function returns void
					if len(typeAndVal.rsplit(" ")) > 2:
						typeAndVal = typeAndVal.replace(" retval", "").strip()

					typeAndVal = typeAndVal.rsplit(" ", 1)
					if len(typeAndVal) > 0:
						self.__returnTypes.append(typeAndVal[0].strip().replace("optional ", "").strip())
						if (len(typeAndVal) > 1):
							self.__returnVars.append(typeAndVal[1].strip())
						else:
							self.__returnVars.append("")
		else:
			self.__returnTypes.append("void")
			self.__returnVars.append("")

		# Get function name
		functionSig = functionSig[1 if len(functionSig) > 1 else 0].split("(", 1)
		self.__funcName = functionSig[0].strip()

		if self.__funcName.find("gfx.") != -1:
			self.__funcName = self.__funcName.replace("gfx.", "").strip()
			self.__luaGfx = True

		if self.__funcName.find("array}.") != -1:
			self.__funcName = self.__funcName.replace("array}.", "").strip()
			self.__luaReaperArray = True

		# Get function parameters
		parameters = functionSig[1].strip().rstrip(")").split(",")
		if len(parameters) > 0 and not (len(parameters) == 1 and parameters[0] == ""):
			for parameter in parameters:

				parameterVar  = ""
				parameterType = ""

				typeAndVal = parameter.rsplit(" ", 1)
				if len(typeAndVal) > 1:
					parameterType = typeAndVal[0].strip().replace("optional ", "").strip()
					parameterVar = typeAndVal[1].strip()
				else:
					parameterVar = typeAndVal[0].strip()

				# Built-in Lua functions display const char* as a text wrapped in quotes
				if (typeAndVal[0].find("\"") != -1 or (len(typeAndVal) > 1 and typeAndVal[1].find("\"") != -1)):
					if typeAndVal[0].find("\"") != -1:
						parameterVar = typeAndVal[0].replace("\"", "")
					else:
						parameterVar = parameterTypeAndVal[1].replace("\"", "")
					parameterType = "const char*"

				self.__parameterTypes.append(parameterType)
				self.__parameterVars.append(parameterVar)

		# Print end result to console for debugging
		if DEBUG_MODE == True and self.__funcName == "Debug":
			msg(str(self.__returnTypes) + " @@@ " + str(self.__returnVars) + " @@@ " + self.__funcName + " @@@ " + str(self.__parameterTypes) + " @@@ " + str(self.__parameterVars))
			msg(self.__returnTypes)
			msg(self.__returnVars)
			msg(self.__funcName)
			msg(self.__parameterTypes)
			msg(self.__parameterVars)

	def __parsePyFunc (self, functionSig):
		self.__language = "Python"

	def getLanguage (self):
		return self.__language

	def getFuncName (self):
		return self.__funcName

	def getReturnVars (self):
		return self.__returnVars

	def getReturnTypes (self):
		return self.__returnTypes

	def getParameterVars (self):
		return self.__parameterVars

	def getParameterTypes (self):
		return self.__parameterTypes

	def isEelImportedApi (self):
		return self.__eelIsExtensionApi

	def isBuiltIn (self):
		return self.__builtIn

	def isLuaGFx (self):
		return self.__luaGfx

	def isLuaArray (self):
		return self.__luaReaperArray

# ---------------------------------------------------------------------------------------------------------------------
def AskForReaScriptHtmlPath ():
	import sys
	sys.argv=["Main"]
	import tkinter as tk
	from tkinter import filedialog

	root = tk.Tk()
	root.withdraw()
	return os.path.realpath(filedialog.askopenfilename())

def GetReaScriptHtmlPath ():
	if os.path.exists(PATH_TO_REASCRIPT_API):
		return PATH_TO_REASCRIPT_API
	else:
		return AskForReaScriptHtmlPath()

def StripHtmlTagsFromCodeTags (htmlLine):
	return re.sub("<[^<]+?>", "", re.search(r"<code>(.*?)</code>", htmlLine).group(1)).strip()

def IsFunctionSigLegal (str, language, isBuiltIn):
	legal = True;

	if language == "EEL" and isBuiltIn:
		if str == "gfx VARIABLES":                            legal = False; # Not an API function
		#elif str == "extension_api(\"function_name\"[,...])": legal = False; # used by extensions, no need to document it itself
	if language == "Lua" and isBuiltIn:
		if str == "gfx VARIABLES":                            legal = False; # Not an API function
	return legal;

# ---------------------------------------------------------------------------------------------------------------------
def SaveApi (cFunc, eelFuncs, luaFuncs, pyFuncs):
	for functionSig in open(GetReaScriptHtmlPath(), "r"):

		language  = ""
		isBuiltIn = False
		funcList  = []

		if   functionSig.startswith("<div class=\"c_func\"><span class=\'all_view\'>C: </span><code>"):      language = "C";      isBuiltIn = False; funcList = cFuncs;
		elif functionSig.startswith("<div class=\"e_func\"><span class=\'all_view\'>EEL2: </span><code>"):   language = "EEL";    isBuiltIn = False; funcList = eelFuncs;
		elif functionSig.startswith("EEL2: <code>"):                                                         language = "EEL";    isBuiltIn = True;  funcList = eelFuncs
		elif functionSig.startswith("<div class=\"l_func\"><span class=\'all_view\'>Lua: </span><code>"):    language = "Lua";    isBuiltIn = False; funcList = luaFuncs;
		elif functionSig.startswith("Lua: <code>"):                                                          language = "Lua";    isBuiltIn = True;  funcList = luaFuncs;
		elif functionSig.startswith("<div class=\"p_func\"><span class=\'all_view\'>Python: </span><code>"): language = "Python"; isBuiltIn = False; funcList = pyFuncs;

		if language != "":
			functionSig = StripHtmlTagsFromCodeTags(functionSig)
			if functionSig and IsFunctionSigLegal(functionSig, language, isBuiltIn):
				funcList.append(ApiFunction(functionSig, language, isBuiltIn))

	cFunc.sort(key = lambda x: x.getFuncName().lower())
	eelFuncs.sort(key = lambda x: x.getFuncName().lower())
	luaFuncs.sort(key = lambda x: x.getFuncName().lower())
	pyFuncs.sort(key = lambda x: x.getFuncName().lower())

# ---------------------------------------------------------------------------------------------------------------------
def CreateEelCompletions (apiFunctionList, filePath):
	f = open(filePath,'w')

	f.write("{\n\t\"scope\": \"source.EEL\",\n\t\"completions\":\n\t[\n")

	for apiFunc in apiFunctionList:
		triggerStr = apiFunc.getParameterVars()[0] if apiFunc.isEelImportedApi() else apiFunc.getFuncName()

		i = 0
		contentsStr = apiFunc.getFuncName() + "("
		for parameter in apiFunc.getParameterVars():
			i += 1
			if i != 1:
				contentsStr += ", "

			if   apiFunc.getParameterTypes()[i-1] == "const char*": parameter = "\\\"" + parameter + "\\\"";
			elif apiFunc.getParameterTypes()[i-1] == "char*":   	parameter = "#" + parameter;

			if i == 1 and apiFunc.isEelImportedApi():
				contentsStr += "\\\"" + str(parameter) + "\\\""
			else:
				contentsStr += "${" + str(i - 1 if apiFunc.isEelImportedApi() else i) + ":" + parameter + "}"
		contentsStr += ")"

		f.write("\t\t{")
		f.write("\"trigger\": \""  + triggerStr  + "\", ")
		f.write("\"contents\": \"" + contentsStr + "\"")
		f.write("},\n")

	f.write("\t]\n}")
	f.close()

def CreateLuaCompletions (apiFunctionList, filePath):
	f = open(filePath,'w')

	f.write("{\n\t\"scope\": \"source.lua\",\n\t\"completions\":\n\t[\n")

	for apiFunc in apiFunctionList:

		triggerStr  = ""
		contentsStr = ""
		triggerStr  = ("reaper." if apiFunc.isLuaGFx() == False and apiFunc.isLuaArray() == False else "gfx." if apiFunc.isLuaGFx() else "") + apiFunc.getFuncName()
		contentsStr = triggerStr + "("

		j = 0
		for parameter in apiFunc.getParameterVars():
			j += 1
			if j != 1:
				contentsStr += ", "
			contentsStr += "${" + str(j) + ":" + parameter + "}"
		contentsStr += ")"

		#f.write("\t\t[")
		#f.write("\""  + triggerStr  + "\", ")
		#f.write("\"" + contentsStr + "\"")
		#f.write("],\n")

		f.write("\t\t{")
		f.write("\"trigger\": \""  + triggerStr  + "\", ")
		f.write("\"contents\": \"" + contentsStr + "\"")
		f.write("},\n")

	f.write("\t]\n}")
	f.close()

# ---------------------------------------------------------------------------------------------------------------------
cFuncs   = []
eelFuncs = []
luaFuncs = []
pyFuncs  = []

SaveApi(cFuncs, eelFuncs, luaFuncs, pyFuncs)
CreateEelCompletions(eelFuncs, TARGET_FOLDER + "ReaSyntax - EEL.sublime-completions")
CreateLuaCompletions(luaFuncs, TARGET_FOLDER + "ReaSyntax - Lua.sublime-completions")# completions.sublime-settings")