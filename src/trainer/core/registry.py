from typing import Callable

type ReadMethod = str
type WriteMethod = str
type CastFn = Callable[[object], object]
type RegistryEntry = tuple[ReadMethod, WriteMethod, CastFn]

TYPE_REGISTRY: dict[str, RegistryEntry] = {
    
    "float":        ("read_float",     "write_float",     float),  
    "double":       ("read_double",    "write_double",    float),  # type: ignore[dict-item]
    "int":          ("read_int",       "write_int",       int),    # type: ignore[dict-item]
    "short":        ("read_short",     "write_short",     int),    # type: ignore[dict-item]
    "long":         ("read_long",      "write_long",      int),    # type: ignore[dict-item]
    "longlong":     ("read_longlong",  "write_longlong",  int),    # type: ignore[dict-item]
    "uint":         ("read_uint",      "write_uint",      int),    # type: ignore[dict-item]
    "ushort":       ("read_ushort",    "write_ushort",    int),    # type: ignore[dict-item]
    "ulong":        ("read_ulong",     "write_ulong",     int),    # type: ignore[dict-item]
    "ulonglong":    ("read_ulonglong", "write_ulonglong", int),    # type: ignore[dict-item]
    "bool":         ("read_bool",      "write_bool",      bool),   # type: ignore[dict-item]
    "char":         ("read_char",      "write_char",      bytes),  # type: ignore[dict-item]
    "uchar":        ("read_uchar",     "write_uchar",     int),    # type: ignore[dict-item]
    "bytes":        ("read_bytes",     "write_bytes",     bytes),  # type: ignore[dict-item]
}