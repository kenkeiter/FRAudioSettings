#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#


#import modules required by application
import PyFR.WaitController
import objc

class AppLauncherController(PyFR.WaitController.WaitController):
    def initWithApp_file_(self, text, application, file = None):
        self.app = application
        self.file = file
        PyFR.WaitController.WaitController.initWithText_( self, text )
        return self

    def initWithApp_( self, text, application ):
        self.app = application
        self.file = None
        PyFR.WaitController.WaitController.initWithText_( self, text )
        return self

    def PyFR_start(self):
        self.launchApp( self.app, self.file )

        # FR automatically quits after 20 minutes.  This should disable that behavior...
        #   not tested here, you might need to do this a few seconds into your AppShouldExit callback
        foo=objc.lookUpClass("FRAutoQuitManager")
        foo.sharedManager().setAutoQuitEnabled_(False)


    def FRWasShown(self):
        self.waitDone()
