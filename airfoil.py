from appscript import app
import os

class Speaker(object):
    
    def __init__(self, app, speaker_inst):
        self._app = app
        self._speaker = speaker_inst
    
    def connect(self):
        try:
            self._app.connect_to(self._speaker)
            return True
        except:
            return False
    
    def disconnect(self):
        try:
            self._app.disconnect_from(self._speaker)
            return True
        except:
            return False
    
    @property
    def ident(self):
        try:
            return self._speaker.id()
        except:
            return False
    
    @property
    def name(self):
        try:
            return self._speaker.name()
        except:
            return False
    
    @property
    def connected(self):
        try:
            return self._speaker.connected()
        except:
            return False
    
    def set_volume(self, volume):
        try:
            if not self._app.linked_volume():
                self._speaker.volume.set(volume)
        except:
            return False
    
    def __repr__(self):
        return '<Speaker id:%s name:%s>' % (self.ident, self.name)
    
    def __str__(self):
        return self.name


class Source(object):
    
    def __init__(self, app, source_inst):
        self._app = app
        self._source = source_inst
    
    @property
    def name(self):
        return self._source.name()
    
    @property
    def ident(self):
        return self._source.id()
        
    def make_active(self):
        self._app.current_audio_source.set(self._source)
    
    def __repr__(self):
        return '<Source id:%s name:%s>' % (self.ident, self.name)


class AudioSourceController(object):
    
    def __init__(self):
        self._app = app('Airfoil')
    
    @classmethod
    def is_running(self):
        return bool(os.popen("ps xc | grep Airfoil").read())
    
    def exit(self):
        self._app.quit()
        del self
    
    # sources
    @property
    def system_sources(self):
        return [Source(self._app, s) for s in self._app.system_sources()]
    
    @property
    def application_sources(self):
        return [Source(self._app, s) for s in self._app.application_sources()]
    
    @property
    def device_sources(self):
        return [Source(self._app, s) for s in self._app.device_sources()]
    
    @property
    def speakers(self):
        return [Speaker(self._app, s) for s in self._app.speakers()]
    
    # volume link
    
    def link_volume(self):
        self._app.linked_volume.set(True)
    
    def unlink_volume(self):
        self._app.linked_volume.set(False)
    
    @property
    def volume_linked(self):
        return self._app.linked_volume()


if __name__ == '__main__':
    
    import time
    
    print('Creating controller...')
    ctrl = AudioSourceController()
    
    print 'Found sources:', ctrl.application_sources
    print('Making first source active.')
    ctrl.application_sources[0].make_active()
    
    print 'Linking volume...',
    ctrl.link_volume()
    print 'Linked.'
    
    for speaker in ctrl.speakers:
        print 'Connecting speaker: %s...' % speaker.name,
        speaker.connect()
        print('Connected.')
        print 'Waiting 10 seconds...',
        time.sleep(10)
        print 'Done.'
        print 'Disconnecting...',
        speaker.disconnect()
        print 'Success.'
    
    print 'Unlinking volume...',
    ctrl.unlink_volume()
    print 'Unlinked.'
    