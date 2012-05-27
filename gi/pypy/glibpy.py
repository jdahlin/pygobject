import ctypes

_PyGLib_API = None


class GList(ctypes.Structure):
    def to_list(self, ctype):
        l = self
        while l:
            item = ctypes.cast(l.data, ctype)
            if ctype == ctypes.c_char_p:
                item = item.value
            yield item
            if not l.next:
                break
            l = l.next.contents
GList._fields_ = [('data', ctypes.c_void_p),
                  ('next', ctypes.POINTER(GList)),
                  ('prev', ctypes.POINTER(GList))]


class GError(ctypes.Structure):
    pass


class IOChannel(object):
    pass


class Idle(object):
    pass


class MainContext(object):
    pass


class MainLoop(object):
    pass


class OptionContext(object):
    pass


class OptionGroup(object):
    pass


class Pid(object):
    pass


class PollFD(object):
    pass


class Source(object):
    pass


class Timeout(object):
    pass


IO_ERR = 0
IO_FLAG_APPEND = 0
IO_FLAG_GET_MASK = 0
IO_FLAG_IS_READABLE = 0
IO_FLAG_IS_SEEKABLE = 0
IO_FLAG_IS_WRITEABLE = 0
IO_FLAG_MASK = 0
IO_FLAG_NONBLOCK = 0
IO_FLAG_SET_MASK = 0
IO_HUP = 0
IO_IN = 0
IO_NVAL = 0
IO_OUT = 0
IO_PRI = 0
IO_STATUS_AGAIN = 0
IO_STATUS_EOF = 0
IO_STATUS_ERROR = 0
IO_STATUS_NORMAL = 0
OPTION_ERROR = 0
OPTION_ERROR_BAD_VALUE = 0
OPTION_ERROR_FAILED = 0
OPTION_ERROR_UNKNOWN_OPTION = 0
OPTION_FLAG_FILENAME = 0
OPTION_FLAG_HIDDEN = 0
OPTION_FLAG_IN_MAIN = 0
OPTION_FLAG_NOALIAS = 0
OPTION_FLAG_NO_ARG = 0
OPTION_FLAG_OPTIONAL_ARG = 0
OPTION_FLAG_REVERSE = 0
OPTION_REMAINING = 'remaining'
PRIORITY_DEFAULT = 0
PRIORITY_DEFAULT_IDLE = 0
PRIORITY_HIGH = 0
PRIORITY_HIGH_IDLE = 0
PRIORITY_LOW = 0
SPAWN_CHILD_INHERITS_STDIN = 0
SPAWN_DO_NOT_REAP_CHILD = 0
SPAWN_FILE_AND_ARGV_ZERO = 0
SPAWN_LEAVE_DESCRIPTORS_OPEN = 0
SPAWN_SEARCH_PATH = 0
SPAWN_STDERR_TO_DEV_NULL = 0
SPAWN_STDOUT_TO_DEV_NULL = 0
USER_DIRECTORY_DESKTOP = 0
USER_DIRECTORY_DOCUMENTS = 0
USER_DIRECTORY_DOWNLOAD = 0
USER_DIRECTORY_MUSIC = 0
USER_DIRECTORY_PICTURES = 0
USER_DIRECTORY_PUBLIC_SHARE = 0
USER_DIRECTORY_TEMPLATES = 0
USER_DIRECTORY_VIDEOS = 0


# Functions


def child_watch_add(*args):
    print 'child_watch_add: not implemented', args


def filename_display_basename(*args):
    print 'filename_display_basename: not implemented', args


def filename_display_name(*args):
    print 'filename_display_name: not implemented', args


def filename_from_utf8(*args):
    print 'filename_from_utf8: not implemented', args


def find_program_in_path(*args):
    print 'find_program_in_path: not implemented', args


def get_application_name(*args):
    print 'get_application_name: not implemented', args


def get_current_time(*args):
    print 'get_current_time: not implemented', args


def get_prgname(*args):
    print 'get_prgname: not implemented', args


def get_system_config_dirs(*args):
    print 'get_system_config_dirs: not implemented', args


def get_system_data_dirs(*args):
    print 'get_system_data_dirs: not implemented', args


def get_user_cache_dir(*args):
    print 'get_user_cache_dir: not implemented', args


def get_user_config_dir(*args):
    print 'get_user_config_dir: not implemented', args


def get_user_data_dir(*args):
    print 'get_user_data_dir: not implemented', args


def get_user_special_dir(*args):
    print 'get_user_special_dir: not implemented', args


def glib_version(*args):
    print 'glib_version: not implemented', args


def idle_add(*args):
    print 'idle_add: not implemented', args


def io_add_watch(*args):
    print 'io_add_watch: not implemented', args


def main_context_default(*args):
    print 'main_context_default: not implemented', args


def main_depth(*args):
    print 'main_depth: not implemented', args


def markup_escape_text(*args):
    print 'markup_escape_text: not implemented', args


def pyglib_version(*args):
    print 'pyglib_version: not implemented', args


def set_application_name(*args):
    print 'set_application_name: not implemented', args


def set_prgname(*args):
    print 'set_prgname: not implemented', args


def source_remove(*args):
    print 'source_remove: not implemented', args


def spawn_async(*args):
    print 'spawn_async: not implemented', args


def threads_init(*args):
    print 'threads_init: not implemented', args


def timeout_add(*args):
    print 'timeout_add: not implemented', args


def timeout_add_seconds(*args):
    print 'timeout_add_seconds: not implemented', args


def uri_list_extract_uris(*args):
    print 'uri_list_extract_uris: not implemented', args
