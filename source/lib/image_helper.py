"""
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
"""

"""
Helper module for interacting with AppStream image commands
"""

import subprocess
import json

class image_helper():
    def __init__(self):
        """Init attributes for info collection"""    

    def validate_image(self, imageName, imageDescr, latestAgent, imageTags):
        if latestAgent is True:
            if imageTags == '':
                oscmdtestimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s" --use-latest-agent-version --dry-run' % (imageName, imageDescr)
            else:
                oscmdtestimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s" --use-latest-agent-version --tags %s --dry-run' % (imageName, imageDescr, imageTags)
        elif latestAgent is False:
            if imageTags == '':
                oscmdtestimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s" --dry-run' % (imageName, imageDescr)
            else:
                oscmdtestimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s" --tags %s --dry-run' % (imageName, imageDescr, imageTags)
        testimage = subprocess.Popen(oscmdtestimage, shell=True, stdout=subprocess.PIPE)
        decodedOuput = ""
        for line in testimage.stdout:
            decodedLine = line.decode('utf-8').strip()
            decodedOuput += decodedLine
        jsonOutput = json.loads(decodedOuput)
        return jsonOutput
    
    def create_image(self, imageName, imageDescr, latestAgent, imageTags):
        if latestAgent is True:
            if imageTags == '':
                oscmdcreateimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s" --use-latest-agent-version' % (imageName, imageDescr)
            else:
                oscmdcreateimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s" --use-latest-agent-version --tags %s' % (imageName, imageDescr, imageTags)
        elif latestAgent is False:
            if imageTags == '':
                oscmdcreateimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s"' % (imageName, imageDescr)
            else:
                oscmdcreateimage = 'sudo /usr/local/appstream/image-assistant/AppStreamImageAssistant create-image --name %s --description "%s" --tags %s' % (imageName, imageDescr, imageTags)
        createimage = subprocess.Popen(oscmdcreateimage, shell=True, stdout=subprocess.PIPE)
        decodedOuput = ""
        for line in createimage.stdout:
            decodedLine = line.decode('utf-8').strip()
            decodedOuput += decodedLine
        jsonOutput = json.loads(decodedOuput)
        return jsonOutput
