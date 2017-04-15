import sublime
import sublime_plugin
import os
import re
import fnmatch

pathSlash ='/' if sublime.platform()!='windows' else '\\'

class SassSolutionCommand(sublime_plugin.EventListener):
    def on_activated(self, view):        
        if not len(Engine.completionList):
            Engine.runEngine(self,view)

    def on_post_save(self, view):        
        Engine.runEngine(self,view)

    def on_query_completions(self, view, prefix, locations):

        isSass = view.match_selector(locations[0], 'source.scss')
        if isSass:
            return Engine.completionList




class AddToAutoCompleteCommand(sublime_plugin.WindowCommand):
    def run(self,paths=[]):

        for x in paths:
            if os.path.isfile(x):
                filesList=Engine.getFiles()
                filesList.append(x+pathSlash)
                Engine.setFiles(filesList)
            else:                
                foldersList=Engine.getFolders()
                foldersList.append(x+pathSlash)
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