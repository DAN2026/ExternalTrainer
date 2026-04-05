from abc import ABC, abstractmethod
from typing import Any
from loguru import logger

from trainer.core.memory_connection import MemoryConnection
from trainer.core.registry import TYPE_REGISTRY

type Address = int
type MemoryValue = Any


class BaseValue(ABC):

    def __init__(self, conn: MemoryConnection) -> None:
        
        """
        Initialise with a shared `MemoryConnection`.

        Args:
            conn: An active `MemoryConnection` attached to the target process.
        """

        self.__conn: MemoryConnection = conn


    @property
    @abstractmethod
    def base_offset(self) -> int:
        
        """
        Static offset from the `module base address`.

        Forms the root of the pointer chain:
        module_base + base_offset → first pointer
        """

    @property
    @abstractmethod
    def offsets(self) -> list[int]:
        
        """
        Ordered list of `pointer chain offsets`.

        Each offset is added to the dereferenced address at that step:
        addr = read(module_base + base_offset)
        addr = read(addr + offsets[0])
        ...
        final = addr + offsets[-1]  ← value lives here
        """

    @property
    @abstractmethod
    def value_type(self) -> str:
        
        """
        Type key used to look up read/write methods in `TYPE_REGISTRY`.

        Supported values: `"float"`, `"double"`, `"int"`, `"uint"`,
        `"short"`, `"ushort"`, `"long"`, `"ulong"`, `"longlong"`,
        `"ulonglong"`, `"bool"`, `"char"`, `"uchar"`, `"bytes"`.
        """

    @property
    def _conn(self) -> MemoryConnection:
        
        return self.__conn

    def _resolve(self) -> Address | None:
        
        try:
            addr: Address = self.__conn.pm.read_longlong(
                self.__conn.module_base + self.base_offset
            )
            for offset in self.offsets[:-1]:
                if addr == 0:
                    return None
                addr = self.__conn.pm.read_longlong(addr + offset)
            return addr + self.offsets[-1]
        except Exception as e:
            logger.error(f"{self.__class__.__name__} resolve error: {e}")
            return None

    def get(self) -> MemoryValue | None:
        
        """
        Read the current value from memory.

        Resolves the pointer chain, looks up the correct pymem read
        method from `TYPE_REGISTRY`, and returns the typed value.

        Returns:
            The value cast to its type (e.g. `float`, `int`),
            or `None` if resolution or the read failed.

        Example:
        ```python
            fov.get()  # → 1.0
        ```
        """

        addr: Address | None = self._resolve()

        if addr is None:

            logger.warning(f"{self.__class__.__name__}: unresolvable address")
            return None

        reader, _, _ = TYPE_REGISTRY.get(self.value_type, (None, None, None))

        if not reader:

            logger.error(f"{self.__class__.__name__}: unknown type '{self.value_type}'")
            return None

        try:

            value: MemoryValue = getattr(self.__conn.pm, reader)(addr)

            logger.debug(f"{self.__class__.__name__}.get() → {value}")

            return value

        except Exception as e:

            logger.error(f"{self.__class__.__name__} get error: {e}")

            return None

    def set(self, value: MemoryValue) -> bool:
        
        """
        Write a new value to memory.

        Resolves the pointer chain, looks up the correct pymem write
        method from `TYPE_REGISTRY`, casts and writes the value.

        Args:
            value: The new value to write, cast to the type defined
                   by `value_type` (e.g. `float(value)`).

        Returns:
            `True` if the write succeeded, `False` otherwise.

        Example:
        ```python
            fov.set(1.5)  # → True
        ```
        """

        addr: Address | None = self._resolve()

        if addr is None:
            logger.warning(f"{self.__class__.__name__}: unresolvable address")
            return False

        _, writer, cast = TYPE_REGISTRY.get(self.value_type, (None, None, None))
        if not writer:
            logger.error(f"{self.__class__.__name__}: unknown type '{self.value_type}'")
            return False

        try:
            getattr(self.__conn.pm, writer)(addr, cast(value))
            logger.info(f"{self.__class__.__name__}.set() → {value}")
            return True
        except Exception as e:
            logger.error(f"{self.__class__.__name__} set error: {e}")
            return False
