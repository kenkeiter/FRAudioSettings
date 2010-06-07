import Foundation

from BackRow import *

class Appliance( BRAppliance ):
    # Logging.
    def log(self,s):
        Foundation.NSLog( "%s: %s" % (self.__class__.__name__, str(s) ) )

    sanityCheck = False

    @classmethod
    def initialize(cls):
        name = NSString.alloc().initWithString_( u"com.apple.frontrow.appliance.frontpython" )
        BRFeatureManager.sharedInstance().enableFeatureNamed_( name )

    @classmethod
    def className(cls):

        clsName = NSString.alloc().initWithString_( cls.__name__ )

        backtrace = BRBacktracingException.backtrace()
        range = backtrace.rangeOfString_( "_loadApplianceInfoAtPath:" )

        if range.location == Foundation.NSNotFound and cls.sanityCheck == False:

            range = backtrace.rangeOfString_( "(in BackRow)" )
            cls.sanityCheck = True
        
        if range.location != Foundation.NSNotFound:
            clsName = NSString.alloc().initWithString_( "RUIMoviesAppliance" )

        return clsName

    def applianceController(self):
        return self.getController()

    def applianceControllerWithScene_(self, scene):
        self.scene = scene
        return self.getController()

