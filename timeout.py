#!/usr/bin/env python
'''
License
=======

Copyright (c) 2005-2008, David Baird <dbaird@nmt.edu>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of the <ORGANIZATION> nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Executive Summary
=================

This module provides very, very easy multithreading.  With this module,
you will have a hard time *resisting* creating threads - you'll have to
restrain yourself because it is so easy and so much fun.  My friends
and I like to call it "adhoc multithreading."  See ExampleUsage_ for
a demonstration.

Since PyBackground is based on Python's threading module, it will work in
Linux, Mac OS, Windows and anywhere else Python's threading module works.

By the way, if you have too much fun with this module, perhaps that
is a sign you should be using a language such as Erlang or Io instead
of Python.

History
=======

Revision 12 (2008 February 16), David Baird

    Module was renamed from ``background`` to ``pybackground``.

Background
==========

This module was inspired by the Io_ programming language (which in
turn was inspired by other programming languages).  In Io, by merely
putting the '@' (at) sign in front of a method to create an "actor,"
Io will execute that method in a background thread and return a
"transparent future."  A transparent future is a place holder object
that represents the return value of the method.  When you try to actually
access the transparent future, it will block until the method terminates.
But as long as you don't access the future, then you can keep doing
stuff in the foreground while the background threads happily execute.
This "background" module for Python accomplishes a very similar function.
Instead of an '@' symbol, the "background" function is used instead as
described in the next section.  Io, unlike this module, is also capable
of another trick: deadlock detection.

.. _Io: http://www.iolanguage.com/

Technical Considerations
========================

Asynchronous I/O: Threads v. Select
-----------------------------------

This module uses the threading implementation of Python to accomplish
this.  Python makes use of operating system threads rather than managing
its own light-weight cooperative threads.  With NPTL, multithreading
in Linux became a lot more fun, but there are other ways to deal with
high-latency tasks.  One way in particular is the "select" system call
which is not directly addressed by this module.  (But you could use this
module to wrap up something else that used the "select" system call).

Possible Problems with the Proxy
--------------------------------

The transparent future is based on a Proxy.  Proxies can be tricky
to design.  In particular, some private methods (methods written like
``__foobar__(...)``) might not be proxied properly.  If you have a
problem, let me know and/or send me a patch and I will check it out.

Deadlocks
---------

This module has no ability (yet) to resolve certain cases of deadlocks;
A deadlock is created when two modules are waiting on each other before
they can complete - but they will never complete!  That is a deadlock.

Global Interpreter Lock (GIL)
-----------------------------

Pybackground is based on Python's threading.  Therefore, it is still
subject to the GIL.  If there is a way around this, can someone ping
me with an email?  I will then rewrite PyBackground so that it can
interoperate with other threading implementations.

.. ExampleUsage_
.. _ExampleUsage:

Example Usage
=============

No Timeouts
-----------

Here is an example of how to use the background module::

    import time
    from pybackground import background

    def very_slow_task(arg):
       # do something slow like download a webpage
       # (or sleep for 5 seconds)
       time.sleep(5)
       return arg

    t0 = time.time()
    # Instead of direcly calling very_slow_task(1), do this:
    x = background(very_slow_task)(1)
    y = background(very_slow_task)(2)
    z = background(very_slow_task)(3)

    print z, y, x # >>> (wait 5 seconds then print) 3 2 1
    print time.time() - t0 # >>> 5.00204801559

You can also use this as a Python decorator::

    import time
    from pybackground import background

    @background
    def very_slow_task(arg):
       # do something slow like download a webpage
       # (or sleep for 5 seconds)
       time.sleep(5)
       return arg

    t0 = time.time()
    x = very_slow_task(1)
    y = very_slow_task(2)
    z = very_slow_task(3)
    print z, y, x # >>> 3 2 1
    print time.time() - t0 # >>> 5.00449609756

This also works with classes::

    import time
    from pybackground import background

    class SomeClass(object):
        def method(self, arg):
            time.sleep(5)
            return arg

    my_object = SomeClass()
    x = background(my_object.method)(1)
    y = background(my_object.method)(2)
    z = background(my_object.method)(3)
    print z, y, x

    class SomeOtherClass(object):
        @background
        def method(self, arg):
            time.sleep(5)
            return arg

    my_other_object = SomeOtherClass()

    x = my_other_object.method(1)
    y = my_other_object.method(2)
    z = my_other_object.method(3)
    print z, y, x

Timeouts
--------

.. WARNING::

    The timeout feature currently lacks the ability to kill processes.
    So, it is possible that even though a background processes timed-out
    that it might still be running and consuming system resources.
    Timeouts are currently implemented by passing a time parameter to the
    ``join`` method of threading.Thread objects.

Here is an example of using timeouts::

    import time
    from pybackground import background, Timeout

    def very_slow_task(arg):
       # do something slow like download a webpage
       # (or sleep for 5 seconds)
       time.sleep(5)
       return arg

    t0 = time.time()
    # This will cause a timeout after 1 second:
    x = background(very_slow_task, timeout=1.0)('foobar1')
    # This will cause a timeout after 6 seconds:
    y = background(very_slow_task, timeout=6.0)('foobar2')

    print x == Timeout     # >>> True
    print x, y             # >>> Timeout foobar2
    print time.time() - t0 # >>> 4.97759008408

Credits
=======

http://storytotell.org/ - this is the guy who introduces me to many neat
languages including, you guessed it, Io.

http://auriga.wearlab.de/~alb/python/ - has some neat Python scripts
including "dataflow.py" which essentially does the same thing as this
module.

http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/84317 -
"Easy threading with Futures" circa 2002, by David Perry
'''

import threading
import time

# FIXME: there are a lot more methods that need to be listed here:
#_str = intern('__str__')
#_repr = intern('__repr__')
#_add = intern('__add__')
#_sub = intern('__sub__')
#_mul = intern('__mul__')
#_div = intern('__div__')
#_eq = intern('__eq__')
_call = intern('__call__')

class TimeoutClass(object):
    def __eq__(self, other):
        if self.__class__ == other.__class__: return True
        return False
    def __str__(self):
        return 'Timeout'

Timeout = TimeoutClass()

class NullTimeoutStrategy(object):
    def __init__(self, timeout):
        self._timeout = timeout
        self._time_exceeded = False
        self._t0 = None
        self._tf = None
    def start_timer(self):
        self._t0 = time.time()
    def stop_timer(self):
        self._tf = time.time()
    def time_remaining(self):
        # XXX: refactor for consitency:
        if self._t0 is None:
            return self._timeout
        elif self._tf:
            dt = self._tf - self._t0
        else:
            dt = time.time() - self._t0

        if dt > self._timeout:
            return 0
        else:
            return self._timeout - dt
    def time_exceeded(self):
        return self.time_remaining() <= 0

class SignalTimeoutStrategy(NullTimeoutStrategy):
    # FIXME: Python has some restrictions concerning the use of both
    #        threads **and** signals.
    #        http://docs.python.org/lib/module-signal.html
    def __init__(self, timeout):
        import signal
        self.alarm = signal.alarm
        signal.signal(signal.SIGALRM, self.handler)
        self._timeout = timeout
        self._time_exceeded = False
    def handler(self, frame):
        self._time_exceeded = True
    def start_timer(self):
        self.alarm(self._timeout)
    def stop_timer(self):
        self.alarm(0)
    def time_exceeded(self):
        return self._time_exceeded

class Proxy(object):
    def __init__(self, target=None, gettargethook=None, getattrhook=None):
        self.__target__ = target
        self.__gettargethook__ = gettargethook
        self.__getattrhook__ = getattrhook
    def __gettarget__(self):
        target = self.__target__
        if self.__gettargethook__:
            target = self.__gettargethook__()
        return target
    def __targetgetattr__(self, key):
        # Almost all accesses to the target object must be funnelled through
        # this function
        target = self.__gettarget__()
        value = getattr(target, key)
        if self.__getattrhook__:
            value = self.__getattrhook__(key, value)
        # ERROR: getattr(self.target, '__str__')() is not the same as
        #        self._target.__str__() (Actually... maybe it is?)
        return value
    def __getattr__(self, key):
        if key in self.__dict__: return self.__dict__[key]
        else: return self.__targetgetattr__(key)
    # FIXME: what about __radd__ and friends?
    def __str__(self):        return str(self.__gettarget__())
    def __repr__(self):       return repr(self.__gettarget__())
    def __add__(self, other): return self.__gettarget__() + other
    def __sub__(self, other): return self.__gettarget__() - other
    def __mul__(self, other): return self.__gettarget__() * other
    def __div__(self, other): return self.__gettarget__() / other
    def __eq__(self, other):  return self.__gettarget__() == other
    def __call__(self, *args, **kwargs):
        return self.__targetgetattr__(_call)(*args, **kwargs)

class OldBackgroundThread(threading.Thread):
    class Waiting(object): pass
    def __init__(self, method, timeout, timeout_strategy, *args, **kwargs):
        threading.Thread.__init__(self)
        self._method = method
        self._args = args
        self._kwargs = kwargs
        self._return_value = OldBackgroundThread.Waiting
        self._timeout = timeout
        self.__timeout_strategy = timeout_strategy
        self._timeout_strategy = None

    def run(self):
        if self._timeout:
            self._timeout_strategy = self.__timeout_strategy(self._timeout)
            self._timeout_strategy.start_timer()

        ret = self._method(*self._args, **self._kwargs)

        if self._timeout:
            self._timeout_strategy.stop_timer()

        if self._timeout and self._timeout_strategy.time_exceeded():
            self._return_value = Timeout
        else:
            self._return_value = ret

    def get_return_value(self):
        if self._return_value is OldBackgroundThread.Waiting:
            if self._timeout:
                # FIXME: What if we fail to join (i.e. Timeout)?
                #        Does we just let the thread just keep running
                #        forever?
                if self._timeout_strategy:
                    self.join(self._timeout_strategy.time_remaining())
                    if self._return_value is OldBackgroundThread.Waiting:
                        self._return_value = Timeout
                else:
                    self.join(self._timeout)
                    if self._return_value is OldBackgroundThread.Waiting:
                        self._return_value = Timeout
            else:
                self.join()
        return self._return_value

class NewBackgroundThread(object):

    class Waiting(object): pass

    def __init__(self, method, timeout, timeout_strategy, *args, **kwargs):
        self._method = method
        self._args = args
        self._kwargs = kwargs
        self._return_value = NewBackgroundThread.Waiting
        self._timeout = timeout
        self.__timeout_strategy = timeout_strategy
        self._timeout_strategy = None
        self._thread = None

    def set_thread_object(self, thread_object):
        self._thread = thread_object

    def run(self):
        if self._timeout:
            self._timeout_strategy = self.__timeout_strategy(self._timeout)
            self._timeout_strategy.start_timer()

        ret = self._method(*self._args, **self._kwargs)

        if self._timeout:
            self._timeout_strategy.stop_timer()

        if self._timeout and self._timeout_strategy.time_exceeded():
            self._return_value = Timeout
        else:
            self._return_value = ret

    def get_return_value(self):
        if self._return_value is NewBackgroundThread.Waiting:
            if self._timeout:
                # FIXME: What if we fail to join (i.e. Timeout)?
                #        Does we just let the thread just keep running
                #        forever?
                if self._timeout_strategy:
                    self._thread.join(self._timeout_strategy.time_remaining())
                    if self._return_value is NewBackgroundThread.Waiting:
                        self._return_value = Timeout
                else:
                    self._thread.join(self._timeout)
                    if self._return_value is NewBackgroundThread.Waiting:
                        self._return_value = Timeout
            else:
                self._thread.join()
        return self._return_value

class TransparentFuture(Proxy):
    def __init__(self, background_thread):
        Proxy.__init__(self, gettargethook=background_thread.get_return_value)

def oldbackground(method, timeout=None, timeout_strategy=NullTimeoutStrategy):
    def wrapper(*args, **kwargs):
        x = OldBackgroundThread(method, timeout, timeout_strategy, *args, **kwargs)
        x.start()
        return TransparentFuture(x)
    return wrapper

def newbackground(method,
                  timeout=None,
                  timeout_strategy=NullTimeoutStrategy,
                  thread_strategy=threading.Thread):
    '''
    Converts a method/function into a version which will be spawned in
    the background using a threading API of your choice (set with the
    ``thread_strategy`` parameter).

    ``thread_strategy`` can be one of:
    
    - ``threading.Thread`` (subject to the GIL)
    - ``processing.Process`` (not subject to the GIL)

    The ``thread_strategy`` must support the following interface:

    - ``__call__(target, args)`` which returns an object that supports::

        - ``join()``
    '''
    def wrapper(*args, **kwargs):
        x = NewBackgroundThread(method, timeout, timeout_strategy, *args, **kwargs)
        t = thread_strategy(target=x.run)
        x.set_thread_object(t)
        t.start()
        return TransparentFuture(x)
    return wrapper

background = newbackground