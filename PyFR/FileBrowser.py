import objc
import Foundation
import AppKit

from BackRow import *
from Utilities import ControllerUtilities

from DynamicMenuController import *

class FileBrowserController(DynamicMenuController):
    def initWithDirectory_(self, directory ):

        self.directory = directory

        manager = Foundation.NSFileManager.defaultManager()

        # build a bunch of menu items for the directory.
        files = manager.directoryContentsAtPath_( self.directory )

        items = []

        for f in files:
            if f[0] == '.':
                continue

            isDir = manager.fileExistsAtPath_isDirectory_( self.directory + "/" + f, None )[1]

            item = DynamicMenuItem(f, self.__clicked, f, folder=isDir )
            items.append(item)


        DynamicMenuController.initWithMenu_( self, DynamicMenu( self.directory, items ) )
        return self

    def __clicked(self, menuItem):
        selectedFile = self.directory + '/' + menuItem.title

        if menuItem.folder:
            menuController = FileBrowserController.alloc().initWithDirectory_( selectedFile )
            self.stack().pushController_(menuController)
        else:
            self.fileSelected_( selectedFile )


    def fileSelected_(self, selectedFile):
        self.log( selectedFile )


