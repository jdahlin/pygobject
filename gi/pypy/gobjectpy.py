import ctypes
from ctypes.util import find_library

_lib = ctypes.CDLL(find_library('gobject-2.0.so'))
_lib.g_type_init.argtypes = []
_lib.g_type_init()

# FIXME: initialize these properly
G_MINFLOAT = 0
G_MAXFLOAT = 0
G_MINDOUBLE = 0
G_MAXDOUBLE = 0
G_MINSHORT = 0
G_MAXSHORT = 0
G_MAXUSHORT = 0
G_MININT = 0
G_MAXINT = 0
G_MAXUINT = 0
G_MINLONG = 0
G_MAXLONG = 0
G_MAXULONG = 0
G_MININT8 = 0
G_MAXINT8 = 0
G_MAXUINT8 = 0
G_MININT16 = 0
G_MAXINT16 = 0
G_MAXUINT16 = 0
G_MININT32 = 0
G_MAXINT32 = 0
G_MAXUINT32 = 0
G_MININT64 = 0
G_MAXINT64 = 0
G_MAXUINT64 = 0
G_MAXSIZE = 0
G_MAXSSIZE = 0
G_MINOFFSET = 0
G_MAXOFFSET = 0

PARAM_CONSTRUCT = 0
PARAM_CONSTRUCT_ONLY = 0
PARAM_LAX_VALIDATION = 0
PARAM_READABLE = 0
PARAM_READWRITE = 0
PARAM_WRITABLE = 0
SIGNAL_ACTION = 0
SIGNAL_DETAILED = 0
SIGNAL_NO_HOOKS = 0
SIGNAL_NO_RECURSE = 0
SIGNAL_RUN_CLEANUP = 0
SIGNAL_RUN_FIRST = 0
SIGNAL_RUN_LAST = 0
TYPE_GSTRING = 0
TYPE_INVALID = 0
TYPE_BOOLEAN = 5 << 2
TYPE_ENUM = 12 << 2
TYPE_FLAGS = 13 << 2
TYPE_STRING = 16 << 2

TYPE_FLAG_ABSTRACT = (1 << 4)
TYPE_FLAG_VALUE_ABSTRACT = (1 << 5)


class GType(object):
    c = ctypes.c_size_t

    def __init__(self, value):
        self.value = value
        self.pytype = None

    def __int__(self):
        return self.value

    def __repr__(self):
        return '<GType %s (%d)>' % (self.name, int(self))

    _lib.g_type_is_a.argtypes = [ctypes.c_int, ctypes.c_int]
    _lib.g_type_is_a.restype = ctypes.c_int

    def is_a(self, gtype):
        return bool(_lib.g_type_is_a(int(self), int(gtype)))

    @property
    def name(self):
        return _lib.g_type_name(self.value) or 'invalid'

    @classmethod
    def from_name(cls, type_name):
        return type_from_name(type_name)

    _lib.g_type_fundamental.argtypes = [ctypes.c_int]
    _lib.g_type_fundamental.restype = ctypes.c_int

    @property
    def fundamental(self):
        return GType(_lib.g_type_fundamental(self.value))

    _lib.g_type_test_flags.argtypes = [ctypes.c_int, ctypes.c_int]
    _lib.g_type_test_flags.restype = ctypes.c_int

    def is_abstract(self):
        return _lib.g_type_test_flags(int(self),
                                      TYPE_FLAG_ABSTRACT)

    _lib.g_type_class_ref.argtypes = [ctypes.c_int]
    _lib.g_type_class_ref.restype = ctypes.c_void_p

    def ref(self):
        return _lib.g_type_class_ref(int(self))

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.value == other.value

class GBoxed(object):
    pass


class GEnum(object):
    def __init__(self, value):
        self.value = value

    def __int__(self):
        return self.value


class GFlags(object):
    def __init__(self, value):
        self.value = value

    def __or__(self, other):
        return self.value | other.value


class GInterface(object):
    pass


class GValue(ctypes.Structure):
    class GValueData(ctypes.Union):
        _fields_ = [('v_int', ctypes.c_int),
                    ('v_uint', ctypes.c_uint),
                    # FIXME: long/int64/float
                    ('v_double', ctypes.c_double),
                    ('v_pointer', ctypes.c_void_p),
                    ]

    _fields_ = [('g_type', ctypes.c_long),  # GType
                ('data', GValueData * 2)]

    def set(self, py_value):
        if self.g_type == TYPE_BOOLEAN:
            self.set_boolean(py_value)
        elif self.g_type == TYPE_STRING:
            self.set_string(py_value)
        elif GType(self.g_type).is_a(TYPE_ENUM):
            self.set_enum(py_value)
        else:
            raise NotImplementedError((self.g_type, GType(self.g_type).name))

    def set_boolean(self, value):
        _lib.g_value_set_boolean(self, int(value))

    def set_string(self, value):
        _lib.g_value_set_string(self, str(value))

    def set_enum(self, value):
        _lib.g_value_set_enum(self, int(value))

_lib.g_value_init.argtypes = [ctypes.POINTER(GValue), ctypes.c_int]
_lib.g_value_init.restype = ctypes.POINTER(GValue)

_lib.g_value_set_boolean.argtypes = [ctypes.POINTER(GValue), ctypes.c_int]
_lib.g_value_set_enum.argtypes = [ctypes.POINTER(GValue), ctypes.c_int]
_lib.g_value_set_string.argtypes = [ctypes.POINTER(GValue), ctypes.c_char_p]


class GTypeClass(ctypes.Structure):
    _fields_ = [('g_type', GType.c)]


class GTypeInterface(ctypes.Structure):
    _fields_ = [('g_type', GType.c),
                ('g_type_type', GType.c)]


class GTypeInstance(ctypes.Structure):
    _fields_ = [('g_class', ctypes.POINTER(GTypeClass))]


class GParamSpec(ctypes.Structure):
    _fields_ = [
        ('g_type_instance', GTypeInstance),
        ('name', ctypes.c_char_p),
        ('flags', ctypes.c_long),
        ('value_type', GType.c),
        ('owner_type', GType.c),
        # FIXME: add the remaining private
        ]


class GParameter(ctypes.Structure):
    _fields_ = [('name', ctypes.c_char_p),
                ('value', GValue)]

_lib.g_object_class_find_property.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_lib.g_object_class_find_property.restype = ctypes.POINTER(GParamSpec)


class CGObject(ctypes.Structure):
    _fields_ = [
        ('g_type_instance', GTypeInstance),
        ('ref_count', ctypes.c_uint),
        ('qdata', ctypes.c_void_p)  # GData
        ]

    @property
    def g_type(self):
        return self.class_.contents.g_type

    @property
    def type_name(self):
        return GType(self.class_.contents.g_type).name

    @property
    def class_(self):
        return self.g_type_instance.g_class


class GObject(object):
    c = ctypes.POINTER(CGObject)

    def __init__(self, **kwargs):
        self.obj = None
        gtype = self.__gtype__
        if gtype.is_abstract():
            raise TypeError(
                "Cannot create instance of abstract "
                "(non-instantiable type %r" % (gtype.name))

        class_ = gtype.ref()
        if class_ is None:
            raise TypeError(
                "could not get a reference to type class")

        if self.obj is None:
            # pygobject_prepare_construct_properties
            # g_static_private_set(self)
            n_params = len(kwargs)
            params = (GParameter * n_params)()
            for n, prop_name in enumerate(kwargs):
                # g_object_class_find_property
                # g_value_init
                # pyg_param_gvalue_from_pygobject
                pspec = _lib.g_object_class_find_property(class_, prop_name)
                if not pspec:
                    raise TypeError(
                        "object of type %r does not have property %r" % (
                        gtype.name, prop_name))
                g_value = GValue(pspec.contents.value_type)
                g_value.set(kwargs[prop_name])
                params[n].name = prop_name[:]
                params[n].value = g_value

            self.obj = _lib.g_object_newv(int(gtype), n_params, params)
            # g_object_newv(gtype, n_parameters, parameters)
            # pygobject_sink
            # g_static_private_set(None)
        else:
            # g_object_set_property
            pass

    def get_property(self, prop_name):
        pspec = _lib.g_object_class_find_property(
            self.obj.contents.class_, prop_name)
        if not pspec:
            raise TypeError("object of type %r does not have property %r" % (
                self.obj.contents.type_name, prop_name))
        g_value = GValue(pspec.contents.value_type)
        _lib.g_object_get_property(self.obj, prop_name, g_value)


    def connect(self, signal_name, func, *args):
        if not callable(func):
            raise TypeError("func must be callable")

        g_type = self.obj.contents.g_type
        signal_id = ctypes.c_uint()
        detail_id = ctypes.c_long()
        if not _lib.g_signal_parse_name(signal_name, g_type,
                                        ctypes.byref(signal_id),
                                        ctypes.byref(detail_id),
                                        False):
            raise TypeError('%s: unknown signal name: %s' % (
                repr(self), signal_name))

        from gi.pypy.gipy import Repository
        repo = Repository.get_default()
        info = repo.find_by_gtype(g_type)
        signal_info = info.get_signal_by_name(signal_name)
        print signal_info

        # g_closure_new_simple
        # g_closure_add_invalidate_notifier
        # g_closure_set_marshal


_lib.g_object_newv.argtypes = [GType.c,
                               ctypes.c_int, ctypes.POINTER(GParameter)]
_lib.g_object_newv.restype = GObject.c
_lib.g_object_get_property.argtypes = [GObject.c,
                                       ctypes.c_char_p,
                                       ctypes.POINTER(GValue)]
_lib.g_signal_parse_name.argtypes = [ctypes.c_char_p,
                                     GType.c,
                                     ctypes.POINTER(ctypes.c_uint),
                                     ctypes.POINTER(ctypes.c_long),
                                     ctypes.c_int]
_lib.g_signal_parse_name.restype = ctypes.c_int



class GObjectWeakRef(object):
    pass


class GParamSpec(object):
    pass


class GPointer(object):
    pass


class Warning(object):
    pass


_PyGObject_API = None


def add_emission_hook(*args):
    print 'add_emission_hook: not impl', args


def features(*args):
    print 'features: not impl', args


def list_properties(*args):
    print 'list_properties: not impl', args


def new(*args):
    print 'new: not impl', args


def pygobject_version(*args):
    print 'pygobject_version: not impl', args


def remove_emission_hook(*args):
    print 'remove_emission_hook: not impl', args


def signal_accumulator_true_handled(*args):
    print 'signal_accumulator_true_handled: not impl', args


def signal_list_ids(*args):
    print 'signal_list_ids: not impl', args


def signal_list_names(*args):
    print 'signal_list_names: not impl', args


def signal_lookup(*args):
    print 'signal_lookup: not impl', args


def signal_name(*args):
    print 'signal_name: not impl', args


def signal_new(*args):
    print 'signal_new: not impl', args


def signal_query(*args):
    print 'signal_query: not impl', args


def threads_init(*args):
    print 'threads_init: not impl', args


def type_children(*args):
    print 'type_children: not impl', args


_lib.g_type_from_name.argtypes = [ctypes.c_char_p]


def type_from_name(type_name):
    retval = _lib.g_type_from_name(type_name)
    return GType(retval)


def type_interfaces(*args):
    print 'type_interfaces: not impl', args


_lib.g_type_is_a.argtypes = [GType.c, GType.c]
_lib.g_type_is_a.restype = ctypes.c_long


def type_is_a(a, b):
    return bool(_lib.g_type_is_a(int(a), int(b)))

_lib.g_type_name.argtypes = [GType.c]
_lib.g_type_name.restype = ctypes.c_char_p


def type_name(*args):
    print 'type_name: not impl', args


def type_parent(*args):
    print 'type_parent: not impl', args


def type_register(*args):
    print 'type_register: not impl', args


def _install_metaclass(obj):
    GObject.__meta__ = obj
