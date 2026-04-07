from trainer.memory.memory_connection import MemoryConnection
from trainer.values.fov import FovValue
from trainer.values.prevviewmode import PrevviewmodeValue
from loguru import logger


class ShooterGame:
    """
    Represents the live game state.

    Values (fov, ini) are ``None`` until a successful connection is made.
    Call ``reconnect()`` to attach at any point after the app has started.
    """

    def __init__(self) -> None:
        self._conn = MemoryConnection("ShooterGame.exe", auto_attach=True)  
        self.fov = FovValue(self._conn)
        self.ini = PrevviewmodeValue(self._conn)


    def reconnect(self) -> bool:
        success = self._conn.reconnect()

        if success:
            logger.success("ShooterGame values initialised.")
        else:
            logger.warning("ShooterGame reconnect failed — values are unavailable.")

        return success

    def disconnect(self) -> None:
        """Cleanly release the process handle."""
        self._conn.disconnect()

    @property
    def is_connected(self) -> bool:
        """``True`` when the game process is attached and values are ready."""
        return self._conn.is_alive