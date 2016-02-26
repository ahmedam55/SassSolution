import sublime
import sublime_plugin
import re
import os

class SassSolutionCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        engine.run_engine(self,view)




        
class engine:
    def run_engine(self,view):
        if view.file_name().endswith('.scss'):
                print('DONE')
                folders=sublime.load_settings('sassSolution.sublime-settings').get('folders')
                files=sublime.load_settings('sassSolution.sublime-settings').get('files');
                
                AllSass=''
                for x in folders:
                    for file in os.listdir(x):
                        if file.endswith('.scss'):
                            AllSass+=open(x+file,'r', encoding="utf8").read()

                            
                for x in files:
                    AllSass+=open(x,'r' ,encoding="utf8").read()

                MAGIC='{"scope": "source.scss - string, source.scss","completions":[';



                for x in re.findall(r'\$(.*?):(.*?);', AllSass):
                      MAGIC+='["'+('$'+x[0].replace('"',"").replace('\\','\\\\')+'\t'+x[1].replace('"',"").replace('\\','\\\\'))+'","'+('\\\$'+x[0].replace('"',"'"))+'"],'



                for x in re.findall('\@mixin (.*?)\((.*?)\)',AllSass):
                    MAGIC+='["'+x[0].replace('"',"'").replace(' ','')+'('+x[1].replace('"',"'")+')'+'","'+x[0].replace('"',"'").replace(' ','')+'('+x[1].replace('"',"'").replace('$','\\\$')+')'+'"],'



                path=sublime.packages_path()+'\\User\\sbc-api-mysass.sublime-settings'
                f=open(path,'w+',encoding="utf8")
                content=f.readlines()
                f.close()




                MAGIC+=']}'

                content=MAGIC

                f=open(path,'w',encoding="utf8")

                contents = "".join(content)
                f.write(contents)
                f.close()