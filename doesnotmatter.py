import sublime
import sublime_plugin
import re
import os

class SassSolutionCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
            if view.file_name().endswith('.scss'):
                print('DONE')
                folders=sublime.load_settings('sassSolution.sublime-settings').get('folders')
                files=sublime.load_settings('sassSolution.sublime-settings').get('files');
                
                AllSass=''
                for x in folders:
                    for file in os.listdir(x):
                        if file.endswith('.scss'):
                            AllSass+=open(x+file,'r', encoding="utf8").read()
                            # print(x,file)
                            
                for x in files:
                    AllSass+=open(x,'r' ,encoding="utf8").read()

                MAGIC='{"scope": "source.scss - string, source.scss","completions":[';



                for x in re.findall(r'\$(.*?):(.*?);', AllSass):
                      MAGIC+='["'+('$'+x[0].replace('"',"").replace('\\','\\\\')+'\t'+x[1].replace('"',"").replace('\\','\\\\'))+'","'+('\\\$'+x[0].replace('"',"'"))+'"],'
                      # pass


                # for x in view.find_all('\$(.*?):(.*?);'):
                    # MAGIC+='["'+(view.substr(x).replace(':','\t'))+'","'+(view.substr(x)).split(':')[0].replace('$','\\\$')+'"],'
                for x in re.findall('\@mixin (.*?)\((.*?)\)',AllSass):
                    MAGIC+='["'+x[0].replace('"',"'").replace(' ','')+'('+x[1].replace('"',"'")+')'+'","'+x[0].replace('"',"'").replace(' ','')+'('+x[1].replace('"',"'").replace('$','\\\$')+')'+'"],'


                # for x in view.find_all('\@mixin (.*?)\((.*?)\)'):
                    # MAGIC+='["'+(view.substr(x).replace('@mixin ','').replace(' ',''))+'","'+(view.substr(x).replace('@mixin ','').replace(' ','').replace('$','\\\$'))+'"],'


                path=sublime.packages_path()+'\\User\\sbc-api-mysass.sublime-settings'
                f=open(path,'w+',encoding="utf8")
                content=f.readlines()
                # point=(f.read().find('"completions":\n  ['))
                f.close()

                
                # print(point)
                # content.insert(5,MAGIC)

                MAGIC+=']}'

                content=MAGIC
                # print('HI',content)
                f=open(path,'w',encoding="utf8")
                # f.seek(71)
                # print("".join(content))
                contents = "".join(content)
                f.write(contents)
                f.close()
                # print(sublime.ok_cancel_dialog('Mr xxxx'))
                # print(sublime.status_message('dddd'))
                # sublime.error_message('dddd')
                # print(sublime.windows().__dir__())
            # print(view.__dir__())
            # print(view.file_name())
            # print('view.file_name()')
            # print(view.find_all('\$(.*?):(.*?);'))
            # print(view.substr(view.find_all('\$(.*?):(.*?);')[0]))

            # fff=view.find_all('\$(.*?):(.*?);')
                # sublime.load_settings('ahmed').set('a',':P')
                # print(sublime.load_settings('ahmed').get('a'))
                
                # sublime.save_settings('ahmed')
                # print(AllSass)
                # print(re.findall('\@mixin (.*?)\((.*?)\)',AllSass)