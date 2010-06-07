from PyFR.BackRow import *
import PyFR.AppLauncherController
import PyFR.Appliance 
import PyFR.MenuController
import PyFR.Utilities
import PyFR.Debugging
import PyFR.Alert
import PyFR.OptionDialog

import os, time, string
import objc

import airfoil
from timeout import background

class AudioMenuController(PyFR.MenuController.MenuController):
    
    def make_enableDisableMI(self):
        if airfoil.AudioSourceController.is_running():
            return PyFR.MenuController.MenuItem("Disable Streaming", self.disable, None, 'Small Text')
        return PyFR.MenuController.MenuItem("Enable Streaming", self.enable, None, 'Small Text')
    
    def enable(self):
        self.audio_controller = airfoil.AudioSourceController() # enable on instantiation
        self.root_menu.ds.menu.items[2].layer.setTitle_("Disable Streaming")
    
    def disable(self):
        self.audio_controller.exit()
        self.root_menu.ds.menu.items[2].layer.setTitle_("Enable Streaming")
    
    def make_rootMenu(self):
        self.audio_controller = airfoil.AudioSourceController() # enable on instantiation
        self.root_menu=PyFR.MenuController.Menu("Network Audio Setup",[
            self.make_speakersMenu(),
            #self.make_settingsMenu(),
            self.make_enableDisableMI(),
        ])
        return PyFR.MenuController.MenuController.initWithMenu_(self, self.root_menu)
    
    def make_speakersMenu(self):
        def enableAllSpeakers():
            for speaker in self.audio_controller.speakers:
                speaker.connect()
        speakers_menu = PyFR.MenuController.Menu("Speakers",[])
        for speaker in self.audio_controller.speakers:
            speakers_menu.AddItem(self.make_speakerSubmenu(speaker))
        # todo: add enable all btn
        # speakers_menu.AddItem(PyFR.MenuController.MenuItem(chstr, self.PlayChannel, c, self.GetChannelMetadata, False))
        return speakers_menu
    
    def make_speakerSubmenu(self, speaker_inst):
        
        def enableSpeaker(*args):
            res = speaker_inst.connect()
            speaker_submenu.items[0].layer.setTitle_('Disconnect from "%s"' % speaker_inst.name)
            return res
        
        def disableSpeaker(*args):
            res = speaker_inst.disconnect()
            speaker_submenu.items[0].layer.setTitle_('Connect to "%s"' % speaker_inst.name)
            return res
        
        def toggleSpeaker(*args):
            if speaker_inst.connected:
                speaker_submenu.items[0].layer.setTitle_('Disconnecting...')
                res = background(disableSpeaker, timeout=4.0)()
                if not res:
                    PyFR.Alert.Alert(self, "Failed to disconnect from %s." % speaker_inst.name)
            else:
                speaker_submenu.items[0].layer.setTitle_('Connecting...')
                res = background(enableSpeaker, timeout=4.0)()
                if not res:
                    PyFR.Alert.Alert(self, "Failed to connect to %s. They may be in use!" % speaker_inst.name)
        
        def make_enableDisableSpeakerMI():
            if speaker_inst.connected:
                return PyFR.MenuController.MenuItem('Disconnect from "%s"' % speaker_inst.name, toggleSpeaker)
            return PyFR.MenuController.MenuItem('Connect to "%s"' % speaker_inst.name, toggleSpeaker)
        
        speaker_submenu = PyFR.MenuController.Menu(speaker_inst.name, [
            make_enableDisableSpeakerMI(),
            # todo: add volume control
        ])
        
        return speaker_submenu
        

    def make_settingsMenu(self):
        pass

class RUIPythonAppliance( PyFR.Appliance.Appliance ):

    def getController(self):
        amc = AudioMenuController.alloc()
        amc = amc.make_rootMenu()
        return amc