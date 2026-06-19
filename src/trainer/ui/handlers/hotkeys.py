from typing import Any, Dict, Optional, ClassVar, Union
from pynput import keyboard, mouse
from loguru import logger

from trainer.events.signals import (
    request_hotkey_sync,
    get_hotkeys,
    # Menu Signals
    request_open_close_menu,
    request_game_lock,
    # INI Signals
    request_normal_ini,
    request_hard_ini,
    # Feature Signals
    request_toggle_no_water,
    request_toggle_fullbright,
    request_toggle_beer_xz,
    request_toggle_environment,
)
from trainer.ui.handlers.base import BaseHandler


class HotkeyHandler(BaseHandler):
    """
    Unified service for monitoring hardware input and executing
    logic based on registered pynput key objects.
    """

    __slots__ = (
        "__kb_listener",
        "__ms_listener",
        "__is_running",
        "__keybinds",
        "__signal_map",
    )

    MOUSE_MAP: ClassVar[Dict[str, int]] = {
        "left": -1,
        "right": -2,
        "middle": -3,
        "x1": -4,
        "x2": -5,
    }

    def __init__(self) -> None:
        """
        Initializes listeners and maps action tags to their respective signals.
        """
        self.__kb_listener: Optional[keyboard.Listener] = None
        self.__ms_listener: Optional[mouse.Listener] = None
        self.__is_running: bool = False
        self.__keybinds: Dict[str, Any] = {}

        self.__signal_map: Dict[str, Any] = {
            "kb_normal_ini": request_normal_ini,
            "kb_hard_ini": request_hard_ini,
            "kb_no_water": request_toggle_no_water,
            "kb_fullbright": request_toggle_fullbright,
            "kb_beerxz": request_toggle_beer_xz,
            "kb_no_environment": request_toggle_environment,
            "kb_open_close_menu": request_open_close_menu,
            "kb_game_lock" : request_game_lock
        }

        request_hotkey_sync.connect(self.__sync_hotkeys)
        self.__sync_hotkeys()

        super().__init__()

    def __sync_hotkeys(self, sender: Any = None, **kwargs: Any) -> None:
        """
        Updates the internal keybind registry from the UI source of truth.
        """
        payload = get_hotkeys.send(self)

        if payload and len(payload) > 0:
            self.__keybinds = payload[0][1]
            logger.info(f"HotkeyHandler synced: {len(self.__keybinds)} binds active")

    def register(self) -> None:
        """
        Launches the hardware listeners.
        """
        if self.__is_running: return

        self.__kb_listener = keyboard.Listener(on_release=self.__on_key_release)
        self.__ms_listener = mouse.Listener(on_click=self.__on_mouse_click)

        self.__kb_listener.start()
        self.__ms_listener.start()

        self.__is_running = True
        logger.success("Hotkey Watchdog started.")

    def stop(self) -> None:
        """
        Safely terminates hardware hooks.
        """
        self.__is_running = False
        if self.__kb_listener:
            self.__kb_listener.stop()
        if self.__ms_listener:
            self.__ms_listener.stop()
        logger.info("Hotkey Watchdog stopped.")

    def __on_key_release(
        self, key: Union[keyboard.Key, keyboard.KeyCode, None]
    ) -> None:
        """
        Directly passes the pynput key object to the matcher.
        """
        if not self.__is_running or key is None:
            return

        self.__check_matches(key)

    def __on_mouse_click(
        self, x: float, y: float, button: mouse.Button, pressed: bool
    ) -> None:
        """
        Translates mouse clicks into custom IDs and checks for matches.
        """
        if not self.__is_running or pressed:
            return

        vk: int = self.MOUSE_MAP.get(button.name, 0)
        if vk != 0:
            self.__check_matches(vk)

    def __check_matches(self, input_identifier: Any) -> None:
        """
        Compares input against registry and fires the associated signal if matched.
        """
        for action, bound_key in self.__keybinds.items():
            if input_identifier == bound_key:
                logger.warning(f"Hotkey Triggered: {action}")

                sig = self.__signal_map.get(action)
                if sig:
                    sig.send(self)
