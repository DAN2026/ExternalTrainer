import pymem
import pymem.process
from loguru import logger


class MemoryConnection:
    
    """
    Single shared handle to the target process.

    Wraps `pymem.Pymem` and resolves the `module base address`
    on construction. One instance is shared across all `BaseValue`
    subclasses to avoid opening multiple handles.

    Example:
    ```python
        conn = MemoryConnection("ShooterGame.exe")
        print(hex(conn.module_base))
    ```
    """

    __pm: pymem.Pymem | None
    __module_base: int | None

    def __init__(self, process_name: str) -> None:
        
        """
        Attach to a running process by name.

        Args:
            process_name: The executable name, e.g. `"ShooterGame.exe"`.

        Raises:
            RuntimeError: If the process cannot be found or attached to.
        """

        self.__pm = None
        self.__module_base = None
        self.__attach(process_name)


    def __attach(self, process_name: str) -> None:
        
        """
        Open the process handle and resolve the `module base address`.

        Strongly private — called once by `__init__`, never externally.

        Args:
            process_name: The executable name to attach to.

        Raises:
            RuntimeError: Wraps any exception raised by `pymem`.
        """

        try:
            self.__pm = pymem.Pymem(process_name)

            module = pymem.process.module_from_name(self.__pm.process_handle, process_name)

            if module is None:
                raise RuntimeError(f"Module '{process_name}' not found.")

            self.__module_base = int(module.lpBaseOfDll)

            logger.success(f"Attached to '{process_name}' @ {hex(self.__module_base)}")

        except Exception as e:
            raise RuntimeError(f"Could not attach to '{process_name}': {e}") from e

    @property
    def pm(self) -> pymem.Pymem:
        
        """
        The active `pymem.Pymem` process handle.

        Raises:
            RuntimeError: If the handle has not been initialised.
        """

        if self.__pm is None:
            raise RuntimeError("No active process handle.")
        return self.__pm

    @property
    def module_base(self) -> int:
        
        """
        The `base address` of the process module in memory.

        Used as the starting point for all pointer chain resolution:
        Raises:
            RuntimeError: If the module base has not been resolved.
        """

        if self.__module_base is None:
            
            raise RuntimeError("Module base not resolved.")
        
        return self.__module_base

    @property
    def is_alive(self) -> bool:
        
        """
        `True` if both the process handle and module base are active.
        """

        return self.__pm is not None and self.__module_base is not None
