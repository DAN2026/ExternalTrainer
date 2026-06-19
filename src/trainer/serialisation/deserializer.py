import os
import pickle
from typing import Dict, Any, ClassVar, Optional
from trainer.events.signals import request_load_config, on_load_complete


class ConfigDeserializer:
    """
    Service responsible for loading binary settings and broadcasting them via signals.
    """

    __slots__ = ("__file_path", "__cached_data", "__weakref__")

    APP_NAME: ClassVar[str] = "Arkopedia"
    FILE_NAME: ClassVar[str] = "settings.dat"

    def __init__(self) -> None:
        """
        Initializes the service and connects to the global load request signal.
        """
        self.__file_path: str = self.__get_app_path()
        self.__cached_data: Dict[str, Any] = {}

        # Self-register with the signal bus
        request_load_config.connect(self.__handle_load_request)

    def __get_app_path(self) -> str:
        """
        Determines the persistent storage path in Local AppData.
        """
        local_app_data: Optional[str] = os.getenv("LOCALAPPDATA")
        base_folder: str = os.path.join(local_app_data, self.APP_NAME) if local_app_data else "."
        return os.path.join(base_folder, self.FILE_NAME)

    def __handle_load_request(self, sender: Any) -> None:
        """
        Signal handler bridge to trigger the load logic.
        """
        self.load()

    def load(self) -> Dict[str, Any]:
        """
        Reads binary file from disk and broadcasts results via on_load_complete.
        """
        if not os.path.exists(self.__file_path):
            on_load_complete.send(self, binds={})
            return {}

        try:
            with open(self.__file_path, "rb") as f:
                self.__cached_data = pickle.load(f)
                
                # Ensure we handle various pickle structures safely
                if not isinstance(self.__cached_data, dict):
                    self.__cached_data = {}
        except (PermissionError, IOError, EOFError, pickle.PickleError):
            self.__cached_data = {}

        binds: Dict[str, int] = self.__cached_data.get("keybinds", {})
        on_load_complete.send(self, binds=binds)
        
        return self.__cached_data

    def get_bind(self, key: str, default: int) -> int:
        """
        Helper to fetch a single bind value from the current cache.
        """
        binds: Dict[str, int] = self.__cached_data.get("keybinds", {})
        return binds.get(key, default)