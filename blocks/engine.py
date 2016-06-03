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


    def removeDollarSlashes(text):
        return text.replace('\\','')


    def runEngine(self,view):
        if Engine.isSass(view):   

                allSass=Engine.getFilesAndFoldersText(Engine.getFolders(),Engine.getFiles())

                jsonText='{"scope": "source.scss - string, source.scss","completions":[';

                for x in re.findall(r'\$(.*?):(.*?);', allSass):
                    variableName=Engine.removeSpecialChars(x[0])
                    variableValue=Engine.removeSpecialChars(x[1],False)

                    jsonText+='["'+('$'+variableName+'\t'+variableValue)+'","'+('\\\$'+variableName)+'"],'

                for x in re.findall('\@mixin (\w*)\s{0,}(\((.*?)\)|{|\n)',allSass):
                    mixinName=Engine.removeSpecialChars(x[0])
                    mixinArguments=Engine.removeSpecialChars(x[2])
                    print(x)

                    zeroSlashesMixinArguments=Engine.removeDollarSlashes(mixinArguments)

                    jsonText+='["'+mixinName+'('+zeroSlashesMixinArguments+')'+'","@include '+mixinName+'('+mixinArguments+')'+'"],'

                jsonText+=']}'

                Engine.writeJsonFile(jsonText)