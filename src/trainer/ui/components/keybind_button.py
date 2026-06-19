from typing import Callable, Optional, Any, Dict, ClassVar, Union
import dearpygui.dearpygui as dpg
from pynput import keyboard, mouse
from trainer.ui.styles import themes

class KeybindButton:
    """
    UI component that captures and stores pynput Key objects.
    """

    __slots__ = (
        "__tag",
        "__callback",
        "__current_key",
        "__is_listening",
        "__kb_listener",
        "__ms_listener",
        "__padding_top",
        "__padding_bottom",
        "__indent",
        "__height",
        "__weakref__",
    )

    MOUSE_MAP: ClassVar[Dict[str, int]] = {
        "left": -1,
        "right": -2,
        "middle": -3,
        "x1": -4,
        "x2": -5,
    }

    def __init__(
        self,
        tag: str,
        default_key: Any = dpg.mvKey_None,
        callback: Optional[Callable[[Any], None]] = None,
        padding_top: float = 0.0,
        padding_bottom: float = 0.0,
        indent: float = 0.0,
        height: int = 30,
    ) -> None:
        self.__tag = tag
        self.__callback = callback
        self.__current_key = default_key
        self.__is_listening = False
        self.__kb_listener = None
        self.__ms_listener = None
        self.__padding_top = padding_top
        self.__padding_bottom = padding_bottom
        self.__indent = indent
        self.__height = height

    @property
    def value(self) -> Any:
        """
        Returns the actual pynput Key or KeyCode object.
        """
        return self.__current_key

    @value.setter
    def value(self, key_obj: Any) -> None:
        self.update_state(key_obj)

    @property
    def name(self) -> str:
        """
        Extracts the clean string name from the pynput object.
        """
        key = self.__current_key

        if key == dpg.mvKey_None:
            return "None"

        if isinstance(key, int):
            for name, mouse_id in self.MOUSE_MAP.items():
                if key == mouse_id:
                    return name.upper()
            return f"VK_{key}"

        return str(key).replace("Key.", "").replace("'", "").upper()

    def update_state(self, key_obj: Any) -> None:
        self.__current_key = key_obj
        if dpg.does_item_exist(self.__tag):
            dpg.set_item_label(self.__tag, self.name)

    def build(self, width: float = 100) -> None:
        with dpg.group(tag=f"{self.__tag}_container", indent=self.__indent):
            if self.__padding_top > 0:
                dpg.add_spacer(height=self.__padding_top)
            dpg.add_button(
                tag=self.__tag,
                label=self.name,
                width=width,
                height=self.__height,
                callback=self.__start_listening
            )
            themes.apply(self.__tag, themes.keybind_btn)
            if self.__padding_bottom > 0:
                dpg.add_spacer(height=self.__padding_bottom)

    def __start_listening(self, *args: Any, **kwargs: Any) -> None:
        if self.__is_listening:
            return
        self.__is_listening = True
        dpg.set_item_label(self.__tag, "...")
        self.__kb_listener = keyboard.Listener(on_release=self.__on_key_captured)
        self.__ms_listener = mouse.Listener(on_click=self.__on_mouse_captured)
        self.__kb_listener.start()
        self.__ms_listener.start()

    def __on_key_captured(self, key: Any) -> None:
        if not self.__is_listening or key is None:
            return
        
        # Escape to cancel logic
        is_esc = False
        if isinstance(key, keyboard.Key) and key == keyboard.Key.esc:
            is_esc = True
        
        if not is_esc:
            self.update_state(key)
            if self.__callback:
                self.__callback(key)

        self.__stop_listening()

    def __on_mouse_captured(self, x: float, y: float, button: Any, pressed: bool) -> None:
        if not self.__is_listening or pressed:
            return
        vk = self.MOUSE_MAP.get(button.name, 0)
        if vk != 0:
            self.update_state(vk)
            if self.__callback:
                self.__callback(vk)
        self.__stop_listening()

    def __stop_listening(self) -> None:
        self.__is_listening = False
        if self.__kb_listener:
            self.__kb_listener.stop()
        if self.__ms_listener:
            self.__ms_listener.stop()
        if dpg.does_item_exist(self.__tag):
            dpg.set_item_label(self.__tag, self.name)