from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
import zipfile
import os
import shutil
import re
import ast
from django.conf import settings

unzipped_path=str(settings.BASE_DIR)+"\\media"
main_project_path=str(settings.BASE_DIR)+"\\shellcontainerproject"

def list_installed_apps(path):
    print("instedapp",path)
    pattern = r"INSTALLED_APPS = \[(.*?)\]"
    with open(str(path) , 'r') as myfile:
        data=myfile.read()
        match = re.search(pattern, data, re.DOTALL)
        if match:
            print(match.group(0)) 
            get_app_list = match.group(0)
    list_of_installed = ast.literal_eval(ast.parse(get_app_list).body[0].value)
    print(list_of_installed)
    return list_of_installed

def check_folder_status(unzipped_path):
    root=unzipped_path
    dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
    return dirlist
    
def checking_app_status(file_name):
    print("enter")
    with open(os.path.join(main_project_path,file_name), "r") as myfile:
        file_value=myfile.read()
        if "my_apps =" in file_value:
            settings_file_value=file_value.split("my_apps =")[0]
            myfile.close()
            return settings_file_value
        elif "append_urls =" in file_value :
            url_file_value=file_value.split("append_urls =")[0]
            myfile.close()
            return url_file_value
        else:
            return file_value

@api_view(["POST"])
def listener(request):
    if request.method=="POST":
        json_input_request=request.data
        print(json.dumps(json_input_request,indent=4))
        print(json_input_request["Pipeline_path"])
        with zipfile.ZipFile(json_input_request["Pipeline_path"], 'r') as zip_ref:
            previous_dir_list=check_folder_status(unzipped_path)
            zip_ref.extractall(unzipped_path)
            current_dir_list=check_folder_status(unzipped_path)
            filename=list(set(current_dir_list)-set(previous_dir_list))
            if len(filename)==0:
                return JsonResponse({"result":"file already exist"})
            else:
                url_names =[]
                extracted_folder_path=str(unzipped_path)+"\\"+str(filename[0])
                print(extracted_folder_path)
                for (root,dirs,files) in os.walk(extracted_folder_path, topdown=True):
                        if os.path.exists(os.path.join(root,"views.py")):
                            App_path = root
                            url_names.append(os.path.basename(App_path))
                        elif os.path.exists(os.path.join(root,"settings.py")):
                            Project_path = root
                for item in os.listdir(App_path):
                    source = os.path.join(App_path, item)
                    if "migrations" not in source and "__pycache__" not in source:
                        if not os.path.exists(os.path.join(str(settings.BASE_DIR),str(os.path.basename(App_path)))):
                            os.mkdir(os.path.join(str(settings.BASE_DIR),str(os.path.basename(App_path))))
                        distination = os.path.join(str(settings.BASE_DIR),str(os.path.basename(App_path)), item)
                        if os.path.isdir(source):
                            shutil.copytree(App_path, distination, symlinks=False, ignore=None)
                        else:
                            shutil.copy2(source, distination)
                shell_installed_app = list_installed_apps(os.path.join(main_project_path,"settings.py"))
                pipe_installed_app = list_installed_apps(os.path.join(Project_path,"settings.py"))
                app_list_append = [x for x in pipe_installed_app if x not in shell_installed_app]
                listToStr = ", ".join([str("'"+elem+"'") for elem in app_list_append])
                listToStr = "\n\nmy_apps = ["+listToStr+"]\n\nINSTALLED_APPS += my_apps"
                setting_file_read=checking_app_status("settings.py")
                with open(os.path.join(main_project_path,"settings.py"), "w+") as myfile:
                    myfile.write(setting_file_read+listToStr)
                    myfile.close()
                urlpatterns = []
                for name in url_names:
                    urlpatterns.append('path(\'\', include(\''+name+'.urls\'))')
                print(urlpatterns)
                listToStr = ", ".join([str(elem) for elem in urlpatterns])
                print(listToStr)
                listToStr = "\n\nappend_urls = ["+listToStr+"]\nurlpatterns +=append_urls"
                url_file_read=checking_app_status("urls.py")
                with open(os.path.join(main_project_path,"urls.py"), "w+") as myfile:
                    myfile.write(url_file_read+listToStr)
                    myfile.close()
                return JsonResponse({"json_input_request":json_input_request},safe=False)

