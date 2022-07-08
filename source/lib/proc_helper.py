"""
// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
"""

"""
Helper module for interacting with Processes
"""

import os
from .msg_helper import msg_helper as msghelper
from .catalog_helper import catalog_helper as catohelper

class proc_helper():
    def __init__(self):
        """Init attributes for info collection"""
        self.username = os.getlogin()
        if self.username != "ImageBuilderAdmin":
            msghelper.warn(text="You are not running as ImageBuilderAdmin!")
    
    def get_procs (self):
        oscmd = "ps -u {}".format(self.username) 
        procs = os.system(oscmd)
        return procs

    def get_procnames (self):
        oscmd2 = "ps -u %s -o cmd|sort|uniq|sed 's/\s.*$//'|sed 's/.*\///'|sort|uniq" % (self.username)
        procNames = os.popen(oscmd2).readlines()
        procnames = []
        ignoreList = ('.sh','.conf','bash','AS2IB')
        for line in procNames:
            cleaned = line.strip()
            if not cleaned.endswith(ignoreList):
                procnames.append(cleaned)
        
        return procnames
    
    def get_firstproc (self, procname):
        """Get first id of first proc with a given name"""
        oscmd3 = "ps -C %s -o pid= |sort |head -n 1" % (procname)
        pid = os.popen(oscmd3).read()
        return pid.strip()

    def get_procfiles (self, procid):
        """get files for a given procnew defs"""
        oscmd4 = "lsof -p $(pstree -p %s | grep -o '([0-9]\+)' | grep -o '[0-9]\+' | tr '\\012' ,)|grep REG | sed -n '1!p' | awk '{print $9}'|awk 'NF'" % (procid)
        try:
            filelist = os.popen(oscmd4).read()
        except:  
            filelist = None
        
        if filelist == None:
            msghelper.warn(text="No associated files found for this process.")

        return filelist
    
    def get_proclocation(self, procid):
        procLocator = "ls -l /proc/%s/exe" % (procid)
        procLocation = os.popen(procLocator).read()
        return procLocation

    def write_manifest (self, manifest, localManifest, force):
        """write manifest file to /tmp"""
        if not catohelper.check_manifest(self, manifestLocation = localManifest):
            manifestFile = open(localManifest, "x")
            manifestFile.write(manifest)
            manifestFile.close
            return True
        else:
            if force == True:
                with open(localManifest, 'w') as manifestFile:
                    manifestFile.write(manifest)
            else:
                return False

