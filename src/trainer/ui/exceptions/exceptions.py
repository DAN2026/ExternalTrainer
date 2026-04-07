class DPGItemNotFoundError(Exception):
    """Raised when an interaction is attempted on a non-existent DPG tag."""
    pass

class GameProcessNotFoundError(Exception):
    """Raised when the target `ShooterGame` process is not found or has terminated."""
    pass

class MemoryAccessViolationError(Exception):
    """Raised when a read/write operation fails on a specific `memory_address`."""
    pass

class GameValueOutOfRangeError(Exception):
    """Raised when a value (e.g., `fov`) exceeds the game's hardcoded limits."""
    pass

class SharedMemoryInstanceError(Exception):
    """Raised when a `BasePage` attempts to access `self.__ARK` before initialization."""
    pass

class StyleInitializationError(Exception):
    """Raised when a `themes` or `fonts` resource fails to load into the DPG registry."""
    pass

class DuplicateTagError(Exception):
    """Raised when attempting to build a component with an existing `dpg_tag`."""
    pass