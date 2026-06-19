import os
import pickle
from typing import Dict, Any, Optional, ClassVar
from trainer.events.signals import request_save_config, on_save_success, on_save_failure


class ConfigSerializer:
    """
    Handles atomic binary serialization to the local AppData directory
    by listening for global save request signals.
    """

    __slots__ = ("__file_path", "__weakref__")

    APP_NAME: ClassVar[str] = "Arkopedia"
    FILE_NAME: ClassVar[str] = "settings.dat"

    def __init__(self) -> None:
        """
        Initializes pathing and connects to the global save signal.
        """
        self.__file_path: str = self.__get_app_path()
        
        # Self-register with the signal bus
        request_save_config.connect(self.__handle_save_request)

    def __get_app_path(self) -> str:
        """
        Constructs a path in %LOCALAPPDATA%.
        """
        local_app_data: Optional[str] = os.getenv("LOCALAPPDATA")
        base_folder: str = os.path.join(local_app_data, self.APP_NAME) if local_app_data else "."

        if not os.path.exists(base_folder):
            try:
                os.makedirs(base_folder, exist_ok=True)
            except OSError:
                base_folder = "."

        return os.path.join(base_folder, self.FILE_NAME)

    def __handle_save_request(self, sender: Any, registry: Dict[str, Any]) -> None:
        """
        Bridge method to trigger saving when a signal is received.
        """
        self.save(registry)

    def save(self, registry: Dict[str, Any], extras: Optional[Dict[str, Any]] = None) -> bool:
        """
        Saves registry state to the persistent AppData location atomically.
        """
        payload: Dict[str, Any] = {
            "keybinds": {key: btn.value for key, btn in registry.items()}
        }

        if extras:
            payload.update(extras)

        temp_path: str = f"{self.__file_path}.tmp"

        try:
            with open(temp_path, "wb") as f:
                pickle.dump(payload, f)

            # Atomic swap
            if os.path.exists(self.__file_path):
                os.remove(self.__file_path)

            os.rename(temp_path, self.__file_path)
            
            on_save_success.send(self, payload=payload)
            return True

        except (PermissionError, IOError, OSError, pickle.PickleError) as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            
            on_save_failure.send(self, error=e)
            return False