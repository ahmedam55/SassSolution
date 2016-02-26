import sublime
import sublime_plugin
import re
import os

class SassSolutionCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        Engine.runEngine(self,view)







































class Engine:

    def runEngine(self,view):

        def isSass(myview):
            extension='.scss'

            if(isinstance(myview,sublime.View)):
                return myview.file_name().endswith(extension)
            else:
                return myview.endswith(extension)


        def getFolders():
            return sublime.load_settings('sassSolution.sublime-settings').get('folders')


        def getFiles():
            return sublime.load_settings('sassSolution.sublime-settings').get('files')


        def getFilesAndFoldersText(folders,files):
            code=''

            for x in folders:
                for file in os.listdir(x):
                    if isSass(file):
                        code+=open(x+file,'r', encoding="utf8").read()

            for x in files:
                code+=open(x,'r' ,encoding="utf8").read()

            return code


        def writeJsonFile(content):
            path=sublime.packages_path()+'\\User\\sbc-api-mysass.sublime-settings'
            f=open(path,'w',encoding="utf8")

            contents = "".join(content)
            f.write(contents)
            f.close()

        def removeSpecialChars(text):
            return text.replace('"',"").replace('\\','\\\\').replace('$','\\\$')

        def callEngine():
            if isSass(view):   

                    allSass=getFilesAndFoldersText(getFolders(),getFiles())

                    jsonText='{"scope": "source.scss - string, source.scss","completions":[';

                    for x in re.findall(r'\$(.*?):(.*?);', allSass):
                        variableName=removeSpecialChars(x[0])
                        variableValue=removeSpecialChars(x[1])

                        jsonText+='["'+('$'+variableName+'\t'+variableValue)+'","'+('\\\$'+variableName)+'"],'

                    for x in re.findall('\@mixin (.*?)\((.*?)\)',allSass):
                        mixinName=removeSpecialChars(x[0])
                        mixinArguments=removeSpecialChars(x[1])

                        jsonText+='["'+mixinName+'('+mixinArguments+')'+'","'+mixinName+'('+mixinArguments+')'+'"],'

                    jsonText+=']}'

                    writeJsonFile(jsonText)


        #main function                
        callEngine()