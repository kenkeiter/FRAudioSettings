NAME=AudioSettings
VERSION=1.2
IMGNAME=${NAME}-${VERSION}

install:
	rm -rf build dist
	python setup.py py2app
	sudo rm -rf /System/Library/CoreServices/Front\ Row.app/Contents/PlugIns/Audio\ Settings.frappliance
	cp ApplianceIcon.png dist/Audio\ Settings.frappliance/Contents/Resources/
	sudo mv dist/Audio\ Settings.frappliance /System/Library/CoreServices/Front\ Row.app/Contents/PlugIns/
	killall -9 "Front Row"