from __future__ import absolute_import
import sys
if __package__:
    from .subB import *
else:
    import subB

print('Hello from submodule A ' + sys.version)
