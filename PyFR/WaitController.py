from BackRow import *
from Utilities import ControllerUtilities

class WaitController(BRController, ControllerUtilities):

    # This needs to be in here for some bizarro reason. Something about
    # having selectors in non-ObjC'ed classes. Doesn't wanna set them up
    # correctly for some reason. Movin this to the util class will not work.
    launchedAppTick_ = objc.selector( ControllerUtilities.launchedAppTick_, 
                                      signature="v@:@")
    firedMethod_ = objc.selector( ControllerUtilities.firedMethod_, signature="v@:@")


    def __setupText(self, text):
        ''' Set up the text field '''
        attribs = BRThemeInfo.sharedTheme().paragraphTextAttributes()
        self.textController = BRHeaderControl.alloc().init()
        self.textController.setTitle_( text )

        # There's probably a better way to do this,
        masterFrame = BRRenderScene.singleton().size()
        w = masterFrame[0]
        h = masterFrame[1]

        origin = ( 0, (h * 0.5))
        size = ( w, h * 0.25 )

        # Where it goes, and how big
        self.textController.setFrame_( ( origin, size ) )

        self.addControl_(self.textController)

    def __setupSpinner(self):
        self.spinner = BRWaitSpinnerControl.alloc().init()
        self.spinner.controlWasActivated()

        masterFrame = BRRenderScene.singleton().size()

        w = masterFrame[0]
        h = masterFrame[1]

        # Get the preferred size of the spinner
        size = self.spinner.layer().preferredSize()
        origin = ((w/2) - (size[0]/2) , 0 )

        self.spinner.setFrame_( ( origin, size ) )

        self.addControl_(self.spinner)

    def initWithText_(self, text):
        BRController.init(self)
        self.__setupText(text)
        self.__setupSpinner()

        return self

    def wasPushed(self):
        # Make sure to call the parent!
        BRController.wasPushed(self)

        self.PyFR_start()

    def PyFR_start(self):
        # This should get overridden
        pass

    def AboutToHideFR(self):
        self.removeAllControls() 

    def waitDone(self):
        self.stack().popController()
