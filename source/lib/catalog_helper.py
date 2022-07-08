"""
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
"""

"""
Helper module for interacting with AppStream Catalog commands
"""

import os
import subprocess
from subprocess import Popen
import json
from .msg_helper import msg_helper as msghelper
class catalog_helper():
    def __init__(self):
        """Init attributes for info collection"""    
    
    def get_appcatalog(self):
        try:
            oscmdgetapps = "sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant list-applications"
        except:
            msghelper.error(text="There was an error calling the AppStreamImageAssistant")
        
        apps = subprocess.Popen(oscmdgetapps, shell=True, stdout=subprocess.PIPE)
        decodedOuput = ""
        for line in apps.stdout:
            decodedLine = line.decode('ASCII')
            decodedOuput += decodedLine
        return decodedOuput

    def check_manifest(self, manifestLocation):
        if os.path.exists(manifestLocation):
            return True
        else:
            return False

    def add_application(self, appName, appPath, manifestPath, displayName, workingDir, iconPath, launchParams, currentCatalog): 
        #Check if app already exists
        result = ""
        jsonOutput = json.loads(currentCatalog)
        if "Success" in  jsonOutput["message"]:
            numofapps = len(jsonOutput["applications"])
            if jsonOutput["applications"]:
                for appnum in range(numofapps):
                    if jsonOutput["applications"][appnum]["Name"] == appName:
                        result = "%s is already in your catalog. Change the name or remove the application from your catalog before adding." % (appName)
                        break
        #Check for required params
        if result == "":
            if appName != "" and appPath != "" and manifestPath != "": 
                oscmdaddapp = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant add-application --name %s --absolute-app-path="%s" --absolute-manifest-path %s' % (appName, appPath, manifestPath)
                if displayName != "":
                    oscmdaddapp += ' --display-name="%s"' % (displayName)
                if workingDir != "":
                    oscmdaddapp += ' --working-directory="%s"' % (workingDir)
                if iconPath != "":
                    oscmdaddapp += ' --absolute-icon-path="%s"' % (iconPath)
                if launchParams != "":
                    oscmdaddapp += ' --launch-parameters="%s"' % (launchParams)
                appAddition = subprocess.Popen(oscmdaddapp, shell=True, stdout=subprocess.PIPE)
                decodedOuput = ""
                for line in appAddition.stdout:
                    decodedLine = line.decode('ASCII')
                    decodedOuput += decodedLine
                jsonOutput = json.loads(decodedOuput)
                if "Success" in jsonOutput["message"]:
                    result = True
                else:
                    result = jsonOutput["message"]
                return result
            else:
                return "The provided inputs resulted in an error when adding the application to your catalog."
        else:
            return result

    def remove_application(self, appnames):
        print(appnames[0])
        if len(appnames) > 1:
            for name in appnames:
                oscmdresetcat = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant remove-application --name %s' % (name)
                resetapps = subprocess.Popen(oscmdresetcat, shell=True, stdout=subprocess.PIPE)
                decodedOuput = ""
                for line in resetapps.stdout:
                    decodedLine = line.decode('ASCII')
                    decodedOuput += decodedLine
                jsonOutput = json.loads(decodedOuput)
                if jsonOutput["status"] == 0:
                    removeResult = True
                else:
                    removeResult = jsonOutput
        else:
            oscmdresetcat = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant remove-application --name %s' % (appnames[0])
            resetapps = subprocess.Popen(oscmdresetcat, shell=True, stdout=subprocess.PIPE)
            decodedOuput = ""
            for line in resetapps.stdout:
                decodedLine = line.decode('ASCII')
                decodedOuput += decodedLine
            jsonOutput = json.loads(decodedOuput)
            if jsonOutput["status"] == 0:
                removeResult = True
            else:
                removeResult = jsonOutput["message"]
        return removeResult
