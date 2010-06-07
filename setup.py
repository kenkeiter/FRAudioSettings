from distutils.core import setup
import py2app

plist = dict(NSPrincipalClass='RUIPythonAppliance',
             CFBundleDevelopmentRegion='English',
             CFBundleExecutable='AudioSettings',
             CFBundleName='Audio Settings',
             CFBundleIdentifier="com.apple.frontrow.appliance.AudioSettings",
             CFBundleInfoDictionaryVersion='6.0',
             CFBundlePackageType='BNDL',
             CFBundleSignature='????',
             CFBundleVersion='1.0',
             FRApplianceIconHorizontalOffset=0.046899999999999997,
             FRApplianceIconKerningFactor=0.10000000000000001,
             FRApplianceIconReflectionOffset=-0.125,
             FRAppliancePreferedOrderValue=-1,
             FRRemoteAppliance=True )


setup(
    plugin = ['AudioSettings.py'],
    data_files=['English.lproj', 'PyFR', 'airfoil.py', 'timeout.py',],
    options=dict(py2app=dict(extension='.frappliance', plist=plist))
 )