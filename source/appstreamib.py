"""
/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
"""

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import askyesno
import pygubu
from pygubu.builder import tkstdwidgets, ttkstdwidgets
from pygubu.builder.widgets import scrollbarhelper, tkscrollbarhelper
import json
import os
import sys
import webbrowser

# Load helper Libs
from lib.proc_helper import proc_helper as prochelper
from lib.catalog_helper import catalog_helper as catohelper
from lib.msg_helper import msg_helper as msghelper
from lib.image_helper import image_helper as imagehelper

procs = prochelper()
class MyApplication(pygubu.TkApplication):
    # Functions
    def _create_ui(self):
        # Create a builder
        self.builder = builder = pygubu.Builder()
        #Load an ui file
        runningPath = os.path.dirname(os.path.realpath(__file__))
        self.uiFileLoc = "%s/appstreamib.xml" % runningPath
        builder.add_from_file(self.uiFileLoc)

        # Create the widget using self.master as parent
        self.mainwindow = builder.get_object('mainwindow', self.master)

        # Set main menu
        self.mainmenu = menu = builder.get_object('mainmenu', self.master)
        self.set_menu(menu)

        # Configure callbacks
        builder.connect_callbacks(self)

        # Load Elements 
        self.comboProcs = builder.get_object('comboProcs')
        self.textFiles = builder.get_object('textFiles')
        self.buttonProcs = builder.get_object('buttonProcs')
        self.entryManifest = builder.get_object('entryManifest')
        self.entryImageName = builder.get_object('entryImageName')
        self.entryDescr = builder.get_object('entryDescr')
        self.checkUpdateAgent = builder.get_object('checkUpdateAgent')
        self.entryTags = builder.get_object('entryTags')
        self.entryGrep = builder.get_object('entryGrep')
        self.grepVar = builder.get_variable('grepString')
        self.grepVar.trace("w", lambda name, index,mode, var=self.grepVar: self.grepChanged())
        self.checkState = builder.get_variable('checkState')
        self.viewApps = builder.get_object('buttonView')
        self.buttonRemApp = builder.get_object('buttonRemApp')
        self.treeCatalog = builder.get_object('treeCatalog')

        # Load App container to store app values
        self.manifestLocal = None

        # Horizontal Scrollbar
        self.xscrollbar = builder.get_object('scrollbar1')
        self.treeCatalog['xscrollcommand'] = self.xscrollbar.set
        self.xscrollbar['command'] = self.treeCatalog.xview

        # Vertical Scrollbar
        self.yscrollbar = builder.get_object('scrollbar2')
        self.treeCatalog['yscrollcommand'] = self.yscrollbar.set
        self.yscrollbar['command'] = self.treeCatalog.yview

    def grepChanged(self):
        """Function triggered when filter dialog is changed. Determines the change and updates combo to contain only matching items."""
        gprocs = filter(lambda gString: self.grepVar.get() in gString, self.proclist )
        fList = (list(gprocs))
        self.comboProcs.config(values = fList)
        self.comboProcs.set(fList[0])

    def addToCatalog(self, isNew, filePath=None):
        """Secondary window to add define an application and add to the catalog."""
        self.textFiles.delete(1.0, tk.END)
        if catohelper.check_manifest(self,self.manifestLocal):
            # Create Window for app specific data
            builder2 = pygubu.Builder()
            builder2.add_from_file(self.uiFileLoc)
            self.mainWin2 = tk.Toplevel(self.mainwindow)
            appWin = builder2.get_object('AppWin', self.mainWin2)
            
            # Set callbacks so main function can react to buttons
            callbacks = {
                'on_buttonAddApp_clicked': self.on_buttonAddApp_clicked, 
                'on_buttonResetApp_clicked': self.on_buttonResetApp_clicked, 
                'on_buttonAppBrowse_clicked': self.on_buttonAppBrowse_clicked, 
                'on_buttonIconBrowse_clicked': self.on_buttonIconBrowse_clicked, 
                'on_buttonManifestBrowse_clicked': self.on_buttonManifestBrowse_clicked
                }
            
            builder2.connect_callbacks(callbacks)

            # Find elements in XML
            self.entryAppName = builder2.get_object('entryAppName')
            self.entryAppPath = builder2.get_object('entryAppPath')
            self.entryDisplayName = builder2.get_object('entryDisplayName')
            self.entryIconPath = builder2.get_object('entryIconPath')
            self.entryWorkingDir = builder2.get_object('entryWorkingDir')
            self.entryLaunchParams = builder2.get_object('entryLaunchParams')
            self.entryManifestPath = builder2.get_object('entryManifestPath')

            if isNew is True:
                # Find proc location
                appName = self.comboProcs.get()
                procLocation = prochelper.get_proclocation(self, procs.get_firstproc(self.comboProcs.get()))
                procLocation = procLocation.split(' -> ')
                procLocation = procLocation[1].strip()

                # Set Initial entry inputs
                self.entryAppName.insert(0,appName)
                self.entryAppPath.insert(0,procLocation)
                self.entryDisplayName.insert(0,appName)
                self.entryManifestPath.insert(0,self.manifestLocal)
            
            else:
                # Clear App Dialog Contents
                self.entryAppName.delete(0,tk.END)
                self.entryAppPath.delete(0,tk.END)
                self.entryDisplayName.delete(0,tk.END)
                self.entryWorkingDir.delete(0,tk.END)
                self.entryManifestPath.delete(0,tk.END)

                # Get App Name and location
                appname = filePath.split('/')[-1].rsplit('-',1)[0]

                procCmd = "which %s" % (appname)
                procLocation = os.popen(procCmd).readlines()[0].strip()

                # Set App Dialog Contents
                self.entryAppName.insert(0,appname)
                self.entryAppPath.insert(0,procLocation)
                self.entryDisplayName.insert(0,appname) 
                self.entryManifestPath.insert(0,filePath)

        else:
            msghelper.warn(text="No manifest found for selected app. Please create one first.")

    # Menu Elements    
    def on_mfile_item_clicked(self, itemid):
        """Quit App Menu Item"""
        if itemid == 'mfile_quit':
            self.quit();

    def on_about_clicked(self):
        """Display About App Information"""
        webbrowser.open('https://github.com/aws-samples/appstream2-linux-imaging-assistant', new=1)

    # Main Window
    def on_buttonProcs_clicked(self):
        """Get list of running processes and update Combobox"""
        # Get a list of procnames
        self.proclist = procs.get_procnames()
        # Set comboProcs contents to list 
        self.comboProcs.config(values = self.proclist)
        # Select the first proc name in comboProcs
        self.comboProcs.set(self.proclist[0])

    def on_buttonFiles_clicked(self):
        """Determine all releated processes to selected and collect files in use. Results also displayed in text box."""
        pname = self.comboProcs.get()
        lowpid = procs.get_firstproc(procname = pname)
        fileList = procs.get_procfiles(procid = lowpid)
        self.textFiles.delete(1.0, tk.END)
        self.textFiles.insert(tk.END, fileList)
        return fileList

    def on_buttonManifest_clicked(self):
        """Create manifest entry for a new application. This will launch a secondary window for app details."""
        msghelper.info(text = "manifest will be written to {}".format(self.entryManifest.get()))
        self.manifestLocal = "%s/%s-manifest.txt" % (self.entryManifest.get(), self.comboProcs.get())
        createResult = procs.write_manifest(manifest = self.on_buttonFiles_clicked(), localManifest = self.manifestLocal, force=False)
        if not createResult:
            overwrite = askyesno('Overwite Manifest?', 'The specified manifest path (%s) already exists. Would you like to overwrite?' % (self.manifestLocal))
            if overwrite is True:
                overwriteResult = procs.write_manifest(manifest = self.on_buttonFiles_clicked(), localManifest = self.manifestLocal, force=True)
                self.addToCatalog(isNew=True)
            else:
                self.textFiles.delete(1.0, tk.END)
                self.textFiles.insert(tk.END, "The application manifest already exists in %s. Remove the file and try again." % (self.entryManifest.get()))
        else:
            self.addToCatalog(isNew=True)

    def on_buttonRemApp_clicked(self):
        """Clears selected app"""
        self.textFiles.delete(1.0, tk.END)
        removeResult = ""
        appNames = []
        selectedApp = self.treeCatalog.selection()
        selectedApp = int(selectedApp[0])
        jsonOutput = json.loads(catohelper.get_appcatalog(self))
        if "Success" in  jsonOutput["message"]:
            if jsonOutput["applications"]:
                appNames.append(jsonOutput["applications"][selectedApp]["Name"])
                removeResult = catohelper.remove_application(self, appnames=appNames)
                print(removeResult)
                if removeResult is True:
                    msghelper.info(text="%s has been successfully removed." % (jsonOutput["applications"][selectedApp]["Name"]))                   
                else:
                    msghelper.error(text="An error has occurred when removing %s from your catalog." % (jsonOutput["applications"][selectedApp]["Name"]))
                    self.textFiles.insert(tk.END, "%s" % removeResult)
            else:
                msghelper.error(text="An error has occurred when listing your applications.")
        self.on_buttonView_clicked()

    def on_buttonReset_clicked(self):
        """Clears all applications from the App Catalog"""
        jsonOutput = json.loads(catohelper.get_appcatalog(self))
        if "Success" in  jsonOutput["message"]:
            numofapps = len(jsonOutput["applications"])
            appnames = []
            for appnum in range(numofapps):
                appnames.append(jsonOutput["applications"][appnum]["Name"])
            resetResult = catohelper.remove_application(self, appnames)
            if resetResult is True:
                msghelper.info(text="You have successfully reset your catalog")
                self.textFiles.insert(tk.END, "You have successfully reset your application catalog.")
            else: 
                msghelper.error(text="An error has occurred when resetting your application catalog. See Output tab for more information.")
                self.textFiles.insert(tk.END, "%s" % resetResult)
        else:
            msghelper.error(text="An error has occurred when listing your applications.")
    
    def on_buttonImage_clicked(self):
        """Initiates the create image process."""
        self.textFiles.delete(1.0, tk.END)
        imageName = self.entryImageName.get()
        imageDescr = self.entryDescr.get()
        imageTags = self.entryTags.get()
        if 'selected' in self.checkUpdateAgent.state():
            latestAgent = True
        elif 'alternate' in self.checkUpdateAgent.state():
            latestAgent = False
        imageValidation = imagehelper.validate_image(self, imageName, imageDescr, latestAgent, imageTags)
        print(imageValidation)
        self.textFiles.insert(tk.END, '%s' % (imageValidation))
        if imageValidation["status"] == 0:
            createResult = imagehelper.create_image(self, imageName, imageDescr, latestAgent, imageTags)
            msghelper.info(text="The creation of your %s image has been successfully initiated." % (imageName))
            self.textFiles.delete(1.0, tk.END)
            self.textFiles.insert(tk.END, '%s' % (createResult))
        else:
            msghelper.error(text="An error has occurred while validating your image. See textbox for error details.")
            self.textFiles.delete(1.0, tk.END)
            self.textFiles.insert(tk.END, '%s' % (imageValidation))

    def on_buttonView_clicked(self):
        """Display the current Application Catalog in the Output textbox."""
        if len(self.treeCatalog.get_children()) != 0:
            for item in self.treeCatalog.get_children():
                self.treeCatalog.delete(item)
        jsonOutput = json.loads(catohelper.get_appcatalog(self))
        if "Success" in  jsonOutput["message"]:
            numofapps = len(jsonOutput["applications"])
            displayName = ""
            if jsonOutput["applications"]:
                for appnum in range(numofapps):
                    if "DisplayName" in jsonOutput["applications"][appnum]:
                        displayName = jsonOutput["applications"][appnum]["DisplayName"]
                    if 'LaunchParameters' in jsonOutput["applications"][appnum]:
                        if 'WorkingDirectory' in jsonOutput["applications"][appnum]:
                            self.treeCatalog.insert(parent='', index=appnum, iid=appnum, text='', values=("%s" % (displayName),"%s" % (jsonOutput["applications"][appnum]["AbsoluteIconPath"]),"%s" % (jsonOutput["applications"][appnum]["AbsoluteManifestPath"]), "%s" % (jsonOutput["applications"][appnum]["LaunchParameters"]), "%s" % (jsonOutput["applications"][appnum]["WorkingDirectory"])))
                        else:
                            self.treeCatalog.insert(parent='', index=appnum, iid=appnum, text='', values=("%s" % (displayName),"%s" % (jsonOutput["applications"][appnum]["AbsoluteIconPath"]),"%s" % (jsonOutput["applications"][appnum]["AbsoluteManifestPath"]), "%s" % (jsonOutput["applications"][appnum]["LaunchParameters"])))
                    elif 'WorkingDirectory' in jsonOutput["applications"][appnum]:
                        self.treeCatalog.insert(parent='', index=appnum, iid=appnum, text='', values=("%s" % (displayName),"%s" % (jsonOutput["applications"][appnum]["AbsoluteIconPath"]),"%s" % (jsonOutput["applications"][appnum]["AbsoluteManifestPath"]),"%s" % (jsonOutput["applications"][appnum]["WorkingDirectory"])))
                    else:
                        self.treeCatalog.insert(parent='', index=appnum, iid=appnum, text='', values=("%s" % (displayName),"%s" % (jsonOutput["applications"][appnum]["AbsoluteIconPath"]),"%s" % (jsonOutput["applications"][appnum]["AbsoluteManifestPath"])))
            else:
                msghelper.info(text="Your application catalog is currently empty.")
        else:
            msghelper.error(text="An error has occurred when listing your applications. See Output tab")
            self.textFiles.insert(tk.END, jsonOutput["message"])

    def on_buttonImportManifest_clicked(self):
        """Opens a file browse dialog to select a previously saved manifest. This will launch an Application add window populated from the file."""
        
        filePath = fd.askopenfilename(
            title="Open A Manifest file",
            initialdir=self.entryManifest.get(),
            filetypes=(
                ('text files', '*.txt'),
                ('All files', '*.*')
            )
        )
        #update Manifest location field in main window
        self.manifestLocal = filePath
        updatePath = os.path.split(self.manifestLocal)
        self.entryManifest.delete(0, tk.END)
        self.entryManifest.insert(tk.END, updatePath[0])

        # Launch App Dialog
        self.addToCatalog(isNew=False, filePath=filePath)

    def on_buttonManifestLoc_clicked(self):
        """Opens system's native file browser to the location specified for manifest files."""
        os.system("gio open " + self.entryManifest.get())

    # App Window Buttons
    def on_buttonAddApp_clicked(self):
        """Adds the current application to the catalog"""
        currentApps = catohelper.get_appcatalog(self)
        appAddition = catohelper.add_application(self, appName=self.entryAppName.get(), appPath=self.entryAppPath.get(), manifestPath=self.manifestLocal, displayName=self.entryDisplayName.get(), workingDir=self.entryWorkingDir.get(), iconPath=self.entryIconPath.get(), launchParams=self.entryLaunchParams.get(), currentCatalog=currentApps) # should manifestlocal be a get?
        appAddition = True
        if appAddition is True:          
            msghelper.info(text="%s was successfully added to your catalog." % (self.entryAppName.get()))
            # Display current App catalog in Output.
            self.on_buttonView_clicked()
            # Close window
            self.mainWin2.destroy()
        else:
            msghelper.error(text="%s" % (appAddition))

    def on_buttonAppBrowse_clicked(self):
        """Launch file browser to set application path. This overrides the pre-set value in the App Path field."""
        filename = fd.askopenfilename()
        self.entryAppPath.delete(0,tk.END)
        self.entryAppPath.insert(0,filename)

    def on_buttonResetApp_clicked(self):
        """Resets all fields in the app dialog to the initial values."""
        # Clear App Dialog Contents
        self.entryAppName.delete(0,tk.END)
        self.entryAppPath.delete(0,tk.END)
        self.entryDisplayName.delete(0,tk.END)
        self.entryWorkingDir.delete(0,tk.END)
        self.entryManifestPath.delete(0,tk.END)

        appname = self.comboProcs.get()
        firstProc = prochelper.get_firstproc(self, procname=appname)
        procLocation = prochelper.get_proclocation(self, procid=firstProc)
        procLocation = procLocation.split(' -> ')
        procLocation = procLocation[1].rsplit('/', 1)[0].strip()

        # Set App Dialog Contents
        self.entryAppName.insert(0,appname)
        self.entryAppPath.insert(0,procLocation)
        self.entryDisplayName.insert(0,appname) 
        self.entryManifestPath.insert(0,procLocation)

    def on_buttonManifestBrowse_clicked(self):
        """Open file browser to set manifest path location."""
        filename = fd.askopenfilename()
        self.entryManifestPath.delete(0,tk.END)
        self.entryManifestPath.insert(0,filename)

    def on_buttonIconBrowse_clicked(self):
        """Open file browser to select icon file."""
        filename = fd.askopenfilename()
        self.entryIconPath.delete(0,tk.END)
        self.entryIconPath.insert(0,filename)
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('AppStream 2.0 Linux Image Assistant')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = MyApplication(root)
    # Load Proc Combobox ahead of launch
    app.buttonProcs.invoke()
    # Set Checkbox to checked at start
    app.checkState.set(1)
    # Populate Output with current app catalog at launch
    try:
        app.viewApps.invoke()
    except:
        print("Existing Catalog not found")
    # Run app
    app.run()

