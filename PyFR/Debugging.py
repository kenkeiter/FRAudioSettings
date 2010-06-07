import traceback
import os
import objc
import Foundation
import PyObjCTools.Debugging

def PyFRExceptionLogger(exception):
    userInfo = exception.userInfo()

    excStr = traceback.format_exception( userInfo[u'__pyobjc_exc_type__'],
                                         userInfo[u'__pyobjc_exc_value__'],
                                         userInfo[u'__pyobjc_exc_traceback__'] )

    for line in excStr:
        for l in line.split('\n'):
            Foundation.NSLog( l )


    # we logged it, so don't log it for us
    return False


PyObjCTools.Debugging.nsLogPythonException = PyFRExceptionLogger

PyObjCTools.Debugging.installPythonExceptionHandler()

#
# call this function to enable logging of all objective-c calls to /tmp/msgSends-<pid> while /tmp/FRLOG file exists
#
objc.loadBundleFunctions(Foundation.__bundle__, globals(),[('instrumentObjcMessageSends', objc._C_VOID + objc._C_NSBOOL)])
class EnableObjcLogger():
    def __init__(self):
        self.timer = Foundation.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_( 0.25, self, "tick:", None, True )
        
    def tick_(self, senders):
        instrumentObjcMessageSends(os.path.isfile("/tmp/FRLOG"))

