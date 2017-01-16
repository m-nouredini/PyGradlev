import glob
import re
import sys
from gradle_values import *


def change(pwd):
    print("current working directory: " + pwd)
    answer = input("is this ok?(y) ")
    if answer == 'n':
        return
    gradle_wrapper_properties = pwd+'/gradle/wrapper/gradle-wrapper.properties'
    project_build_gradle = pwd+'/build.gradle'
    #app_build_gradle = pwd+'/app/build.gradle'
    gradle_properties = pwd+'/gradle.properties'
    local_properties = pwd+'/local.properties'
    settings_gradle = pwd+'/settings.gradle'

    try:
        with open(gradle_wrapper_properties,"r+") as f:
            file_str = f.read()
            rst = re.sub('distributionUrl=(.*)',distribution_url,file_str)
            f.seek(0)
            f.write(rst)
            print(gradle_wrapper_properties + ' ... DONE!')
    except FileNotFoundError as e:
        print('gradle_wrapper_properties not found')
    try:
        with open(project_build_gradle,"r+") as f:
            file_str = f.read()
            rst = re.sub("classpath 'com.android.tools.build:gradle(.*)",build_tools,file_str)
            f.seek(0)
            f.write(rst)
            print(project_build_gradle + ' ... DONE!')
    except FileNotFoundError as e:
        print('project_build_gradle not found')
    try:
        for app_build_gradle in glob.iglob(pwd+'/**/build.gradle', recursive=True):
            print(app_build_gradle)
            with open(app_build_gradle,"r+") as f:
                file_str = f.read()
                rst = re.sub('compileSdkVersion (\d+)',compile_sdk_version,file_str)
                rst = re.sub('buildToolsVersion (.*)',build_tool_version,rst)
                rst = re.sub("compile 'com.android.support:appcompat-v7:(.*)",appcompat,rst)
                rst = re.sub("compile 'com.android.support:design:(.*)",design,rst)
                f.seek(0)
                f.write(rst)
                print(app_build_gradle + ' ... DONE!')
    except FileNotFoundError as e:
        print('app_build_gradle not found')
    try:
        with open(local_properties,"r+") as f:
            file_str = f.read()
            rst = re.sub('sdk.dir=(.*)',sdk_dir,file_str)
            f.seek(0)
            f.write(rst)
            print(local_properties + ' ... DONE!')
    except FileNotFoundError as e:
        print('local_properties not found')

if __name__ == "__main__":
    change(sys.argv[1])
