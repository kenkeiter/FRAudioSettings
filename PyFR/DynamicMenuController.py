import objc
import Foundation
import AppKit

from BackRow import *
from Utilities import ControllerUtilities

# in individual menu item with text, a function to be called when activated, and an optionional argument to be passed to the function
class DynamicMenuItem(ControllerUtilities):
      def __init__(self,title,func,arg=None,metadata_func=None,folder=False):
            self.title=title
            self.func=func
            self.arg=arg
            self.metadata_func=metadata_func
            self.folder = folder

      def Activate(self):
            #self.log("In activate for menu item %s" % self.title)
            self.func(self)

      def GetMetadata(self, controller):
            #self.log("In GetMetadata for menu item %s" % self.title)
            if self.metadata_func is not None:
                  return self.metadata_func(controller, self.arg)
            else:
                  return None
            
# simple container class for a menu, elements of the items list may contain menu items or another Menu instance for submenus
class DynamicMenu:
      def __init__(self,page_title,items=[]):
          self.page_title=page_title
          self.items=items
          
      def AddItem(self,item):
          self.items.append(item)

      def GetRightText(self):
            return ""

BRMenuListItemProvider = objc.protocolNamed('BRMenuListItemProvider')
class DynamicMenuDataSource(NSObject, BRMenuListItemProvider,ControllerUtilities):

      def initWithController_Menu_(self, ctrlr, menu):
            self.ctrlr = ctrlr
            self.menu = menu
            return self.init()
      
      def itemCount(self):
            return len(self.menu.items)

      def titleForRow_(self,row):
            if row >= len(self.menu.items):
                  return None
            return self.menu.items[row].title
    
      def itemForRow_(self,row):
            #self.log("Called itemForRow %d" % row)
            if row >= len(self.menu.items):
                  return None

            if self.menu.items[row].folder:
                  result=BRTextMenuItemLayer.folderMenuItem()
            else:
                  result=BRTextMenuItemLayer.menuItem()

            result.setTitle_(self.menu.items[row].title)
            return result

      def itemSelected_(self, row):
            if row >= len(self.menu.items):
                  return 

            self.menu.items[row].Activate()

#  should return a preview controller of some type, perhaps
#  BRMetaDataPreviewController BRMetaDataLayer BRMetaDataControl(seems
#  to work for now, but that is really contained in something I
#  haven't identified yet)
      def previewControlForItem_(self, row):
            if row >= len(self.menu.items):
                  return None
            if self.menu.items[row].folder:
                  return None # fixme: could have metadata func here too!
            else:
                  return self.menu.items[row].GetMetadata(self.ctrlr)


      def RemoveItem(self,item):
            self.items.remove(item)
            self.refreshControllerForModelUpdate()


    # Dont care aboutr these below.
      def heightForRow_(self,row):
            return 0.0

      def rowSelectable_(self, row):
            return True


class DynamicMenuController(BRMediaMenuController,ControllerUtilities):

    def dealloc():
          self.log("Deallocing MenuController %s" % self.title)
          return BRMediaMenuController.dealloc(self)

    def initWithMenu_(self, menu):
          BRMenuController.init(self)
          self.title= menu.page_title 
          self.addLabel_(menu.page_title)
          self.setListTitle_( menu.page_title )
          self.ds = DynamicMenuDataSource.alloc().initWithController_Menu_(self,menu)
          self.list().setDatasource_(self.ds)
          return self

    def willBePushed(self):
          #self.log("Pushing menu page %s,%s" % (self.title,self))
          self.list().reload()
          return BRMenuController.willBePushed(self)

    def willBePopped(self):
          #self.log("popping menu page %s, %s" % (self.title,self))
          return BRMenuController.willBePopped(self)

    def itemSelected_(self, row):
          return self.ds.itemSelected_(row)

    def previewControlForItem_(self, row):
          return self.ds.previewControlForItem_(row)

    def rowSelectable_(self,row):
          return True






