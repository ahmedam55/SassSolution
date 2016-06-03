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