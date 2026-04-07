import pymem
import pymem.process
from loguru import logger


class MemoryConnection:
    """
    Single shared handle to the target process.

    Supports lazy attachment — the connection is optional on construction
    and can be re-established at any time via `reconnect()`.

    Example:
```python
        conn = MemoryConnection("ShooterGame.exe")
        if not conn.is_alive:
            conn.reconnect()
        print(hex(conn.module_base))
```
    """

    __pm: pymem.Pymem | None
    __module_base: int | None

    def __init__(self, process_name: str, auto_attach: bool = False) -> None:
        """
        Prepare the connection object, optionally attaching immediately.

        Args:
            process_name: The executable name, e.g. ``"ShooterGame.exe"``.
            auto_attach:  If ``True``, attempt to attach immediately (old
                          behaviour). Defaults to ``False`` so the app can
                          start without the game running.
        """
        self.__process_name = process_name
        self.__pm = None
        self.__module_base = None

        if auto_attach:
            self.__attach()

    def __attach(self) -> bool:
        """
        Open the process handle and resolve the module base address.

        Returns:
            ``True`` on success, ``False`` if the process was not found.
        """
        try:
            pm = pymem.Pymem(self.__process_name)

            module = pymem.process.module_from_name(
                pm.process_handle, self.__process_name
            )

            if module is None:
                logger.warning(f"Module '{self.__process_name}' not found in process.")
                return False

            self.__pm = pm
            self.__module_base = int(module.lpBaseOfDll)

            logger.success(
                f"Attached to '{self.__process_name}' @ {hex(self.__module_base)}"
            )
            return True

        except Exception as e:
            logger.warning(f"Could not attach to '{self.__process_name}': {e}")
            return False


    def reconnect(self) -> bool:
        """
        Attempt to (re-)attach to the target process.

        Safe to call at any time — including when already connected.
        Resets any existing stale handle before trying again.

        Returns:
            ``True`` if the connection was established, ``False`` otherwise.
        """
        if self.__pm is not None:
            try:
                self.__pm.close_process()
            except Exception:
                pass  # Stale handle — ignore
            self.__pm = None
            self.__module_base = None

        logger.info(f"Attempting to reconnect to '{self.__process_name}' …")
        return self.__attach()

    def disconnect(self) -> None:
        """
        Release the process handle and clear the module base.
        """
        if self.__pm is not None:
            try:
                self.__pm.close_process()
            except Exception:
                pass
            self.__pm = None
            self.__module_base = None
            logger.info(f"Disconnected from '{self.__process_name}'.")

    @property
    def pm(self) -> pymem.Pymem:
        """
        The active ``pymem.Pymem`` process handle.

        Raises:
            RuntimeError: If not currently connected.
        """
        if self.__pm is None:
            raise RuntimeError(
                f"Not connected to '{self.__process_name}'. Call reconnect() first."
            )
        return self.__pm

    @property
    def module_base(self) -> int:
        """
        The base address of the process module in memory.

        Raises:
            RuntimeError: If not currently connected.
        """
        if self.__module_base is None:
            raise RuntimeError(
                f"Module base not resolved for '{self.__process_name}'. Call reconnect() first."
            )
        return self.__module_base

    @property
    def is_alive(self) -> bool:
        """``True`` if both the process handle and module base are active."""
        return self.__pm is not None and self.__module_base is not None

    @property
    def process_name(self) -> str:
        """The target executable name."""
        return self.__process_name