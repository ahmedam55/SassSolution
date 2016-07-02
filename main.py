import sublime
import sublime_plugin
import re
import os
import fnmatch

class SassSolutionCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        Engine.runEngine(self,view)


class AddToAutoCompleteCommand(sublime_plugin.WindowCommand):
    def run(self,paths=[]):

        for x in paths:
            if os.path.isfile(x):
                filesList=Engine.getFiles()
                filesList.append(x+'\\')
                Engine.setFiles(filesList)
            else:                
                foldersList=Engine.getFolders()
                foldersList.append(x+'\\')
                Engine.setFolders(foldersList)

        Engine.saveSettings()


class RemoveFromAutoCompleteCommand(sublime_plugin.WindowCommand):
    def run(self,paths=[]):

        for x in paths:
            settingsList=Engine.getFiles() if os.path.isfile(x) else Engine.getFiles()
            settingsList.remove(x) 
            Engine.loadSettings().set()

        Engine.saveSettings()


class ClearAutoCompleteCommand(sublime_plugin.WindowCommand):
    def run(self,paths=[]):
        Engine.eraseFiles()
        Engine.eraseFolders()
        Engine.saveSettings()
class Engine:

    def isSass(myview):
        extension='.scss'

        if(isinstance(myview,sublime.View)):
            return myview.file_name().endswith(extension)
        else:
            return myview.endswith(extension)


    def loadSettings():
        return sublime.load_settings('sassSolution.sublime-settings')


    def saveSettings():
        sublime.save_settings('sassSolution.sublime-settings')


    def getFolders():
        return Engine.loadSettings().get('folders')


    def getFiles():
        return Engine.loadSettings().get('files')


    def setFolders(newList):
        Engine.loadSettings().set('folders',newList)


    def setFiles(newList):
        Engine.loadSettings().set('files',newList)


    def eraseFiles():
        Engine.loadSettings().erase('files');


    def eraseFolders():
        Engine.loadSettings().erase('folders');


    def getFoldersFilesRecursively(folder):
        matches=[]

        for root, dirnames, filenames in os.walk(folder):
            for filename in fnmatch.filter(filenames, '*.scss'):
                matches.append(os.path.join(root, filename))

        return matches


    def getFilesAndFoldersText(folders,files):
        code=''
        print(folders)

        for x in folders:
            for file in Engine.getFoldersFilesRecursively(x):
                code+=open(file,'r', encoding="utf8").read()

        for x in files:
            code+=open(x,'r' ,encoding="utf8").read()

        return code


    def writeJsonFile(content):
        path=sublime.packages_path()+'\\User\\sbc-api-mysass.sublime-settings'
        f=open(path,'w',encoding="utf8")

        contents = "".join(content)
        f.write(contents)
        f.close()


    def removeSpecialChars(text,replaceDollar=True):
        return text.replace('"',"").replace('\\','\\\\').replace('$','\\\$' if replaceDollar else '$')


    def addMixinsCompletion(pattern,code):
        mixinsCompletion=''

        for x in re.findall(pattern,code):
            mixinName=Engine.removeSpecialChars(x[0])
            mixinArguments=Engine.removeSpecialChars(x[2])

            zeroSlashesMixinArguments=Engine.removeDollarSlashes(mixinArguments)

            mixinsCompletion+='["'+mixinName+'('+zeroSlashesMixinArguments+')'+'","@include '+mixinName+'('+mixinArguments+')'+'"],'

        return mixinsCompletion


    def addVariablesCompletion(pattern,code):
        variablesCompletion=''

        for x in re.findall(pattern,code):
            variableName=Engine.removeSpecialChars(x[0])
            variableValue=Engine.removeSpecialChars(x[1],False)

            variablesCompletion+='["'+('$'+variableName+'\t'+variableValue)+'","'+('\\\$'+variableName)+'"],'

        return variablesCompletion


    def removeDollarSlashes(text):
        return text.replace('\\','')


    def runEngine(self,view):
        if Engine.isSass(view):   

                allSass=Engine.getFilesAndFoldersText(Engine.getFolders(),Engine.getFiles())

                jsonText='{"scope": "source.scss - string, source.scss","completions":[';

                jsonText+=Engine.addVariablesCompletion(r'\$(.*?):(.*?);',allSass)
                jsonText+=Engine.addMixinsCompletion('\@mixin ([\w*-]*)\s{0,}(\((.*?)\)|{|\n)',allSass)

                jsonText+=']}'

                Engine.writeJsonFile(jsonText)