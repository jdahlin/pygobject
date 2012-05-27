import sys

from . import gipy
sys.modules['_gi'] = gipy
sys.modules['gi._gi'] = gipy

from . import glibpy
sys.modules['gi._glib._glib'] = glibpy
sys.modules['_glib'] = glibpy

from . import gobjectpy
sys.modules['gi._gobject._gobject'] = gobjectpy
