import objc
import Foundation
import AppKit

from BackRow import *
from Utilities import ControllerUtilities


# in individual menu item with text, a function to be called when activated, and an optionional argument to be passed to the function
class MenuItem(ControllerUtilities):
      def __init__(self,title,func,arg=None,metadata_func=None, smalltext=False):
            self.title=title
            self.func=func
            self.arg=arg
            self.metadata_func=metadata_func
            self.smalltext=smalltext

      def Activate(self, controller):
            #self.log("In activate for menu item %s" % self.title)
            self.func(controller, self.arg)

      def GetMetadata(self, controller):
            #self.log("In GetMetadata for menu item %s" % self.title)
            if self.metadata_func is not None:
                  return self.metadata_func(controller, self.arg)
            else:
                  return None
            
# simple container class for a menu, elements of the items list may contain menu items or another Menu instance for submenus
class Menu(ControllerUtilities):
      def __init__(self,page_title,items=[],metadata_func=None):
          self.page_title=page_title
          self.items=items
          self.metadata_func=metadata_func
          
      def AddItem(self,item):
          self.items.append(item)

      def GetRightText(self):
            return ""

      def GetMetadata(self, controller):
            #self.log("In GetMetadata for menu %s" % self.page_title)
            if self.metadata_func is not None:
                  return self.metadata_func(controller, self.page_title)
            else:
                  return None


# used to duck-type Menus (to indicate an item is a submenu)
def IsMenu(a):
      return hasattr(a,'page_title')

BRMenuListItemProvider = objc.protocolNamed('BRMenuListItemProvider')
class MenuDataSource(NSObject, BRMenuListItemProvider,ControllerUtilities):
      def init(self):
            return NSObject.init(self)

      def initWithController_Menu_(self, ctrlr, menu):
            self.ctrlr = ctrlr
            self.menu = menu
            return self.init()
      
      def itemCount(self):
            return len(self.menu.items)

      def titleForRow_(self,row):
            if row >= len(self.menu.items):
                  return None
            if IsMenu(self.menu.items[row]):
                  return self.menu.items[row].page_title
            else:
                  return self.menu.items[row].title
    
      def itemForRow_(self,row):
            #self.log("Called itemForRow %d" % row)
            if row >= len(self.menu.items):
                  return None

            if IsMenu(self.menu.items[row]):
                  result=BRTextMenuItemLayer.folderMenuItem()
                  result.setTitle_(self.menu.items[row].page_title)
                  result.setRightJustifiedText_(self.menu.items[row].GetRightText())
            else:
                  if not self.menu.items[row].smalltext:
                        result=BRTextMenuItemLayer.menuItem()
                        result.setTitle_(self.menu.items[row].title)
                  else:
                        result=BRTextMenuItemLayer.alloc().init()
                        result.setTitle_withAttributes_(self.menu.items[row].title,BRThemeInfo.sharedTheme().menuItemSmallTextAttributes())
            self.menu.items[row].layer=result
            return result

      def itemSelected_(self, row):
            if row >= len(self.menu.items):
                  return 
            if IsMenu(self.menu.items[row]):
                  con = MenuController.alloc().initWithMenu_(self.menu.items[row])
                  self.ctrlr.stack().pushController_(con)
            else:
                  self.menu.items[row].Activate(self.ctrlr)

      #  return a preview controller of some type, perhaps BRMetaDataPreviewController
      #  see PyeTV source for example!
      def previewControlForItem_(self, row):
            if row >= len(self.menu.items):
                  return None
            return self.menu.items[row].GetMetadata(self.ctrlr)

      def RemoveItem(self,item):
            self.items.remove(item)
            self.refreshControllerForModelUpdate()


    # Dont care about these below.
      def heightForRow_(self,row):
            return 0.0

      def rowSelectable_(self, row):
            return True


class MenuController(BRMediaMenuController,ControllerUtilities):

    def dealloc():
          self.log("Deallocing MenuController %s" % self.title)
          return BRMediaMenuController.dealloc(self)

    def initWithMenu_(self, menu):
          BRMenuController.init(self)
          self.title= menu.page_title 
          self.addLabel_(menu.page_title)
          self.setListTitle_( menu.page_title )
          self.ds = MenuDataSource.alloc().initWithController_Menu_(self,menu)
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





