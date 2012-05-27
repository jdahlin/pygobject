import ctypes
from ctypes.util import find_library

import glibpy as _glib
import gobjectpy as _gobject

_API = None


_lib = ctypes.CDLL(find_library('girepository-1.0.so'))


(ARRAY_TYPE_C,
 ARRAY_TYPE_ARRAY,
 ARRAY_TYPE_PTR_ARRAY,
 ARRAY_TYPE_BYTE_ARRAY) = range(4)

(DIRECTION_IN,
 DIRECTION_OUT,
 DIRECTION_INOUT) = range(3)

FUNCTION_IS_METHOD = 1 << 0
FUNCTION_IS_CONSTRUCTOR = 1 << 1
FUNCTION_IS_GETTER = 1 << 2
FUNCTION_IS_SETTER = 1 << 3
FUNCTION_WRAPS_VFUNC = 1 << 4
FUNCTION_THROWS = 1 << 5

(INFO_TYPE_INVALID,
 INFO_TYPE_FUNCTION,
 INFO_TYPE_CALLBACK,
 INFO_TYPE_STRUCT,
 INFO_TYPE_BOXED,
 INFO_TYPE_ENUM,
 INFO_TYPE_FLAGS,
 INFO_TYPE_OBJECT,
 INFO_TYPE_INTERFACE,
 INFO_TYPE_CONSTANT,
 INFO_TYPE_INVALID_0,  # 10
 INFO_TYPE_UNION,
 INFO_TYPE_VALUE,
 INFO_TYPE_SIGNAL,
 INFO_TYPE_VFUNC,
 INFO_TYPE_PROPERTY,
 INFO_TYPE_FIELD,
 INFO_TYPE_ARG,
 INFO_TYPE_TYPE,
 INFO_TYPE_UNRESOLVED) = range(20)

(TYPE_TAG_VOID,
 TYPE_TAG_BOOLEAN,
 TYPE_TAG_INT8,
 TYPE_TAG_UINT8,
 TYPE_TAG_INT16,
 TYPE_TAG_UINT16,
 TYPE_TAG_INT32,
 TYPE_TAG_UINT32,
 TYPE_TAG_INT64,
 TYPE_TAG_UINT64,
 TYPE_TAG_FLOAT,  # 10
 TYPE_TAG_DOUBLE,
 TYPE_TAG_GTYPE,
 TYPE_TAG_UTF8,
 TYPE_TAG_FILENAME,
 TYPE_TAG_ARRAY,  # 15
 TYPE_TAG_INTERFACE,
 TYPE_TAG_GLIST,
 TYPE_TAG_GSLIST,
 TYPE_TAG_GHASH,
 TYPE_TAG_ERROR,
 TYPE_TAG_UNICHAR) = range(22)


class BaseInfo(ctypes.Structure):
    def new(self, info):
        info_type = self.get_type()
        if info_type == INFO_TYPE_FUNCTION:
            info = ctypes.cast(info, ctypes.POINTER(FunctionInfo))
        elif info_type == INFO_TYPE_CALLBACK:
            info = ctypes.cast(info, ctypes.POINTER(CallbackInfo))
        elif info_type == INFO_TYPE_STRUCT:
            info = ctypes.cast(info, ctypes.POINTER(StructInfo))
        elif info_type == INFO_TYPE_ENUM:
            info = ctypes.cast(info, ctypes.POINTER(EnumInfo))
        elif info_type == INFO_TYPE_FLAGS:
            info = ctypes.cast(info, ctypes.POINTER(EnumInfo))
        elif info_type == INFO_TYPE_OBJECT:
            info = ctypes.cast(info, ctypes.POINTER(ObjectInfo))
        elif info_type == INFO_TYPE_INTERFACE:
            info = ctypes.cast(info, ctypes.POINTER(InterfaceInfo))
        elif info_type == INFO_TYPE_VALUE:
            info = ctypes.cast(info, ctypes.POINTER(ValueInfo))
        elif info_type == INFO_TYPE_CONSTANT:
            info = ctypes.cast(info, ctypes.POINTER(ConstantInfo))
        elif info_type == INFO_TYPE_UNION:
            info = ctypes.cast(info, ctypes.POINTER(UnionInfo))
        elif info_type == INFO_TYPE_ARG:
            info = ctypes.cast(info, ctypes.POINTER(ArgInfo))
        elif info_type == INFO_TYPE_TYPE:
            info = ctypes.cast(info, ctypes.POINTER(TypeInfo))
        else:
            raise NotImplementedError(info_type)
        return info.contents

    def __repr__(self):
        return '<BaseInfo %s.%s>' % (self.get_namespace(),
                                     self.get_name(), )

    def get_namespace(self):
        return _lib.g_base_info_get_namespace(self)

    def get_name(self):
        return _lib.g_base_info_get_name(self)

    def get_type(self):
        return _lib.g_base_info_get_type(self)

    def get_container(self):
        info = _lib.g_base_info_get_container(self)
        if info:
            return info.contents.new(info)

    def _get_methods(self, info_type):
        if info_type is StructInfo:
            n_infos = _lib.g_struct_info_get_n_methods(self)
        elif info_type is UnionInfo:
            n_infos = _lib.g_union_info_get_n_methods(self)
        else:
            raise AssertionError

        methods = []
        for i in range(n_infos):
            if info_type is StructInfo:
                info = _lib.g_struct_info_get_method(self, i)
            elif info_type is UnionInfo:
                info = _lib.g_union_info_get_method(self, i)
            else:
                raise AssertionError
            methods.append(info.contents.new(info))

        return tuple(methods)

_lib.g_struct_info_get_n_methods.argtypes = [ctypes.POINTER(BaseInfo)]
_lib.g_struct_info_get_n_methods.restype = ctypes.c_int

_lib.g_struct_info_get_method.argtypes = [
    ctypes.POINTER(BaseInfo), ctypes.c_int]
_lib.g_struct_info_get_method.restype = ctypes.POINTER(BaseInfo)

_lib.g_base_info_get_type.argtypes = [ctypes.POINTER(BaseInfo)]
_lib.g_base_info_get_type.restype = ctypes.c_int

_lib.g_base_info_get_name.argtypes = [ctypes.POINTER(BaseInfo)]
_lib.g_base_info_get_name.restype = ctypes.c_char_p

_lib.g_base_info_get_namespace.argtypes = [ctypes.POINTER(BaseInfo)]
_lib.g_base_info_get_namespace.restype = ctypes.c_char_p

_lib.g_base_info_get_container.argtypes = [ctypes.POINTER(BaseInfo)]
_lib.g_base_info_get_container.restype = ctypes.POINTER(BaseInfo)


class CallableInfo(BaseInfo):
    _lib.g_callable_info_get_n_args.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_callable_info_get_n_args.restype = ctypes.c_int

    _lib.g_callable_info_get_arg.argtypes = [
        ctypes.POINTER(BaseInfo), ctypes.c_int]
    _lib.g_callable_info_get_arg.restype = ctypes.POINTER(BaseInfo)

    def get_arguments(self):
        n_args = _lib.g_callable_info_get_n_args(self)
        args = []
        for i in range(n_args):
            info = _lib.g_callable_info_get_arg(self, i)
            args.append(info.contents.new(info))
        return args


class ArgInfo(BaseInfo):
    _lib.g_arg_info_get_direction.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_arg_info_get_direction.restype = ctypes.c_int

    def get_direction(self):
        return _lib.g_arg_info_get_direction(self)

    def is_return_value(self):
        pass

    def is_optional(self):
        pass

    def is_caller_allocates(self):
        pass

    def may_be_null(self):
        pass

    def is_skip(self):
        pass

    def get_ownership_transfer(self):
        pass

    def get_scope(self):
        pass

    def get_closure(self):
        pass

    def get_destroy(self):
        pass

    _lib.g_arg_info_get_type.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_arg_info_get_type.restype = ctypes.POINTER(BaseInfo)

    def get_type(self):
        info = _lib.g_arg_info_get_type(self)
        return info.contents.new(info)

    def load_typeself(self):
        pass


class FunctionInfo(CallableInfo):
    def invoke(self, *in_args):
        ns = self.get_namespace()
        symbol = self.get_symbol()
        repo = Repository.get_default()
        for lib_path in repo.get_shared_library(ns).split(','):
            lib = ctypes.CDLL(find_library(lib_path))
            func = getattr(lib, symbol)
            break

        func.argtypes = []

        def remove_array_length_args(arg_infos):
            return_infos = arg_infos[:]
            for n, arg_info in enumerate(arg_infos):
                type_info = arg_info.get_type()
                if type_info.get_tag() != TYPE_TAG_ARRAY:
                    continue
                array_length_arg = type_info.get_array_length()
                if array_length_arg == -1:
                    continue
                del return_infos[array_length_arg]
            return return_infos

        call_args = []
        out_args = []

        arg_infos = self.get_arguments()

        # Prepare argtypes / restype
        for n, arg_info in enumerate(arg_infos):
            type_info = arg_info.get_type()
            #print n, arg_info, type_info
            if type_info.get_tag() == TYPE_TAG_ARRAY:
                ctype = ctypes.POINTER(type_info.get_param_type(0).get_ctype())
            else:
                ctype = type_info.get_ctype()

            if arg_info.get_direction() == DIRECTION_INOUT:
                ctype = ctypes.POINTER(ctype)
            func.argtypes.append(ctype)

        if self.is_method():
            obj = in_args[0].obj
            in_args = in_args[1:]
        else:
            obj = None

        for n, arg_info in enumerate(remove_array_length_args(arg_infos)):
            if arg_info.get_direction() == DIRECTION_OUT:
                continue

            python_arg = in_args[n]
            type_info = arg_info.get_type()

            if type_info.get_tag() == TYPE_TAG_ARRAY:
                length = len(python_arg)
                array_length_arg = type_info.get_array_length()
                if array_length_arg != -1:
                    list_arg_info = arg_infos[array_length_arg]
                    list_arg_type_info = list_arg_info.get_type()
                    list_length_arg = list_arg_type_info.get_ctype()(length)
                    if list_arg_info.get_direction() == DIRECTION_INOUT:
                        list_length_arg = ctypes.byref(list_length_arg)
                    call_args.append(list_length_arg)
                    out_args.append(list_length_arg)
                item_ctype = type_info.get_param_type(0).get_ctype()
                item = ctypes.pointer(item_ctype(python_arg[0]))
                ctype = ctypes.byref(item)
            elif type_info.get_tag() == TYPE_TAG_INTERFACE:
                ctype = python_arg.obj
            elif type_info.get_tag() == TYPE_TAG_UTF8:
                ctype = ctypes.c_char_p(python_arg)
            else:
                raise NotImplementedError(type_info.get_tag())
            call_args.append(ctype)
            # FIXME: Return value of inout parameters
            out_args.append([])

        if self.is_method():
            call_args.insert(0, obj)
            func.argtypes.insert(0, ctypes.POINTER(_gobject.CGObject))
        func(*call_args)

        return_args = []
        for out_arg in out_args:
            return_args.append(out_arg)
        return out_args

    _lib.g_function_info_get_symbol.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_function_info_get_symbol.restype = ctypes.c_char_p

    def get_symbol(self):
        return _lib.g_function_info_get_symbol(self)

    _lib.g_function_info_get_flags.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_function_info_get_flags.restype = ctypes.c_int

    def get_flags(self):
        return _lib.g_function_info_get_flags(self)

    def is_constructor(self):
        return False
        # FIXME
        return self.get_flags() & FUNCTION_IS_CONSTRUCTOR

    def is_method(self):
        return self.get_flags() & FUNCTION_IS_METHOD


class RegisteredTypeInfo(BaseInfo):
    def get_g_type(self):
        return _lib.g_registered_type_info_get_g_type(self)


_lib.g_registered_type_info_get_g_type.argtypes = [
    ctypes.POINTER(RegisteredTypeInfo)]
_lib.g_registered_type_info_get_g_type.restype = _gobject.GType


class EnumInfo(RegisteredTypeInfo):
    def is_flags(self):
        return self.get_type() == INFO_TYPE_FLAGS

    def get_values(self):
        n_infos = _lib.g_enum_info_get_n_values(self)
        values = []
        for i in range(n_infos):
            info = _lib.g_enum_info_get_value(self, i)
            values.append(info.contents.new(info))
        return values


_lib.g_enum_info_get_n_values.argtypes = [ctypes.POINTER(BaseInfo)]
_lib.g_enum_info_get_n_values.restype = ctypes.c_int

_lib.g_enum_info_get_value.argtypes = [ctypes.POINTER(BaseInfo), ctypes.c_int]
_lib.g_enum_info_get_value.restype = ctypes.POINTER(BaseInfo)


class ValueInfo(BaseInfo):
    def get_value(self):
        return _lib.g_value_info_get_value(self)

_lib.g_value_info_get_value.argtypes = [ctypes.POINTER(BaseInfo)]
_lib.g_value_info_get_value.restype = ctypes.c_long


class ObjectInfo(RegisteredTypeInfo):
    _lib.g_object_info_get_parent.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_object_info_get_parent.restype = ctypes.POINTER(BaseInfo)

    def get_parent(self):
        info = _lib.g_object_info_get_parent(self)
        if info:
            return info.contents.new(info)

    def get_interfaces(self):
        return []

    _lib.g_object_info_get_n_methods.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_object_info_get_n_methods.restype = ctypes.c_int

    _lib.g_object_info_get_method.argtypes = [
        ctypes.POINTER(BaseInfo), ctypes.c_int]
    _lib.g_object_info_get_method.restype = ctypes.POINTER(BaseInfo)

    def get_methods(self):
        n_infos = _lib.g_object_info_get_n_methods(self)
        methods = []
        for i in range(n_infos):
            info = _lib.g_object_info_get_method(self, i)
            methods.append(info.contents.new(info))
        return methods

    def get_constants(self):
        return []

    def get_vfuncs(self):
        return []

    def get_fields(self):
        return []


class InterfaceInfo(RegisteredTypeInfo):
    def get_parent(self):
        return None

    def get_interfaces(self):
        return []

    def get_methods(self):
        return []

    def get_constants(self):
        return []

    def get_vfuncs(self):
        return []

    def get_fields(self):
        return []


class ConstantInfo(BaseInfo):
    pass


class StructInfo(RegisteredTypeInfo):
    def get_fields(self):
        return []

    def get_methods(self):
        return self._get_methods(StructInfo)


class UnionInfo(RegisteredTypeInfo):
    pass


class CallbackInfo(BaseInfo):
    pass


_lib.g_type_tag_to_string.argtypes = [ctypes.c_int]
_lib.g_type_tag_to_string.restype = ctypes.c_char_p


class TypeInfo(BaseInfo):
    def __repr__(self):
        return '<TypeInfo %r at 0x%x>' % (
            _lib.g_type_tag_to_string(self.get_tag()),
            hash(self))

    _lib.g_type_info_get_tag.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_type_info_get_tag.restype = ctypes.c_int

    def get_tag(self):
        return _lib.g_type_info_get_tag(self)

    _lib.g_type_info_get_array_type.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_type_info_get_array_type.restype = ctypes.c_int

    def get_array_type(self):
        return _lib.g_type_info_get_array_type(self)

    _lib.g_type_info_get_param_type.argtypes = [
        ctypes.POINTER(BaseInfo), ctypes.c_int]
    _lib.g_type_info_get_param_type.restype = ctypes.POINTER(BaseInfo)

    def get_param_type(self, n):
        info = _lib.g_type_info_get_param_type(self, n)
        return info.contents.new(info)

    _lib.g_type_info_get_array_length.argtypes = [ctypes.POINTER(BaseInfo)]
    _lib.g_type_info_get_array_length.restype = ctypes.c_int

    def get_array_length(self):
        return _lib.g_type_info_get_array_length(self)

    def get_ctype(self):
        type_tag = self.get_tag()
        if type_tag == TYPE_TAG_INT32:
            return ctypes.c_int32
        elif type_tag == TYPE_TAG_UTF8:
            return ctypes.c_char_p
        elif type_tag == TYPE_TAG_ARRAY:
            array_type = self.get_array_type()
            if array_type == ARRAY_TYPE_C:
                return self.get_param_type(0).get_ctype()
        elif type_tag == TYPE_TAG_INTERFACE:
            return ctypes.POINTER(_gobject.CGObject)

        raise NotImplementedError(
            'type tag: ' + _lib.g_type_tag_to_string(type_tag))


class Struct(object):
    pass


class Boxed(object):
    pass


class CCallback(object):
    pass


class VFuncInfo(object):
    pass


G_IREPSITORY_LOAD_FLAG_LAZY = 1


class Repository(object):
    _default = None

    _lib.g_irepository_get_default.argtypes = []

    @classmethod
    def get_default(cls):
        if cls._default is None:
            value = _lib.g_irepository_get_default()
            cls._default = cls(value)
        return cls._default

    def __init__(self, value):
        self.value = value

    _lib.g_irepository_enumerate_versions.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p]
    _lib.g_irepository_enumerate_versions.restype = ctypes.POINTER(_glib.GList)

    def enumerate_versions(self, namespace):
        retval = _lib.g_irepository_enumerate_versions(
            self.value, namespace)
        if retval:
            return list(retval.contents.to_list(ctypes.c_char_p))

    _lib.g_irepository_require.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
        ctypes.POINTER(ctypes.POINTER(_glib.GError))]

    def require(self, namespace, version, lazy=False):
        error = ctypes.POINTER(_glib.GError)()
        flags = 0
        if lazy:
            flags &= G_IREPSITORY_LOAD_FLAG_LAZY
        _lib.g_irepository_require(
            self.value, namespace, version, flags, ctypes.byref(error))
        assert not error

    _lib.g_irepository_get_typelib_path.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p]
    _lib.g_irepository_get_typelib_path.restype = ctypes.c_char_p

    def get_typelib_path(self, namespace):
        return _lib.g_irepository_get_typelib_path(self.value, namespace)

    _lib.g_irepository_get_version.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p]
    _lib.g_irepository_get_version.restype = ctypes.c_char_p

    def get_version(self, namespace):
        return _lib.g_irepository_get_version(self.value, namespace)

    _lib.g_irepository_find_by_name.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
    _lib.g_irepository_find_by_name.restype = ctypes.POINTER(BaseInfo)

    def find_by_name(self, namespace, version):
        info = _lib.g_irepository_find_by_name(self.value, namespace, version)
        if info:
            return info.contents.new(info)

    _lib.g_irepository_get_n_infos.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p]
    _lib.g_irepository_get_n_infos.restype = ctypes.c_int

    _lib.g_irepository_get_info.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
    _lib.g_irepository_get_info.restype = ctypes.POINTER(BaseInfo)

    def get_infos(self, namespace):
        n_infos = _lib.g_irepository_get_n_infos(self.value, namespace)
        infos = []
        for i in range(n_infos):
            info = _lib.g_irepository_get_info(self.value, namespace, i)
            infos.append(info.contents.new(info))
        return info

    _lib.g_irepository_get_shared_library.argtypes = [
        ctypes.c_void_p, ctypes.c_char_p]
    _lib.g_irepository_get_shared_library.restype = ctypes.c_char_p

    def get_shared_library(self, namespace):
        return _lib.g_irepository_get_shared_library(self.value, namespace)


def enum_add(gtype):
    return type(gtype.name, (_gobject.GEnum, ), {})


def enum_register_new_gtype_and_add(*args):
    print 'enum_register_new_gtype_and_add', args


def flags_add(gtype):
    return type(gtype.name, (_gobject.GFlags, ), {})


def flags_register_new_gtype_and_add(*args):
    print 'flags_register_new_gtype_and_add', args


def register_interface_info(*args):
    print 'register_interface_info', args


def hook_up_vfunc_implementation(*args):
    print 'hook_up_vfunc_implementation', args


def variant_new_tuple(*args):
    print 'variant_new_tuple', args


def variant_type_from_string(*args):
    print 'variant_type_from_string', args
