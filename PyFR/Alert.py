#import modules required by application
import objc
import Foundation
import AppKit

from BackRow import *

def Alert(controller,msg):
    alert = BRAlertController.alertOfType_titled_primaryText_secondaryText_( 0, "Alert", msg, "Press menu to go back")
    return controller.stack().pushController_(alert)
