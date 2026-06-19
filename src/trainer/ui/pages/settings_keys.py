from typing import ClassVar, Dict, List, Any, Union
import dearpygui.dearpygui as dpg
from loguru import logger
from pynput import keyboard

from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes
from trainer.ui.components.keybind_row import KeybindRowComponent
from trainer.ui.components.keybind_button import KeybindButton
from trainer.ui.components.search_bar import SearchBarComponent
from trainer.ui.animations.color import ColorTransition

from trainer.events.signals import (
    on_load_complete, 
    request_load_config, 
    request_save_config,
    request_hotkey_sync,
    get_hotkeys
)


class SettingsKeybindsPage(BasePage):
    """
    Handles hardware input mapping by synchronizing rich pynput objects 
    with persistent string-based configuration storage.
    """

    __slots__ = ("__keybinds", "__transitions", "__keybind_data")

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0
    __ROW_WIDTH: ClassVar[float] = 400.0

    def __init__(self) -> None:
        """
        Initializes the keybind registry and connects lifecycle signals.
        """
        self.__keybinds: Dict[str, KeybindButton] = {}
        self.__transitions: List[ColorTransition] = []
        
        self.__keybind_data: Dict[str, str] = {
            "kb_normal_ini": "Normal INI",
            "kb_hard_ini": "Hard INI",
            "kb_no_water": "No Water",
            "kb_fullbright": "Fullbright",
            "kb_beerxz": "Toggle Beer / XZ",
            "kb_no_environment": "No Environment",
            "kb_open_close_menu": "Open / Close Menu",
            "kb_game_lock" : "Game Lock"
        }
        
        on_load_complete.connect(self.__apply_loaded_binds)
        get_hotkeys.connect(self.__get_keybinds)
        
        super().__init__()

    def build(self) -> None:
        """
        Constructs the UI and triggers the initial configuration load request.
        """
        with dpg.child_window(
            tag="settings-keys",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12.5,
            show=False,
        ) as container:

            SearchBarComponent(
                tag="keybind_search",
                hint="Search keybinds...",
                icon="search",
                width=self.__ROW_WIDTH,
                padding_top=5.0,
                data_map=self.__keybind_data,
                callback=lambda query, count, *args: logger.debug(
                    f"Keybind Search: '{query}' | {count} matches"
                )
            ).build(self.__transitions)
            
            with dpg.group(tag="keybind-list-container"):
                with dpg.theme() as scroll_theme:
                    with dpg.theme_component(dpg.mvChildWindow):
                        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 14.0)
                        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 0.0)
                
                dpg.bind_item_theme(container, scroll_theme)

                for tag, label in self.__keybind_data.items():
                    with dpg.group(tag=f"{tag}_row"):
                        KeybindRowComponent(
                            key=tag,
                            label=label,
                            icon="folder",
                            width=self.__ROW_WIDTH,
                            btn_height=30,      
                            padding_top=2.5,  
                            padding_bottom=0, 
                            callback=lambda k, t=tag: self.__on_keybind_change(t, k),
                            indent=50
                        ).build(self.__keybinds, self.__transitions)

        themes.apply(container, themes.container)
        
        if "kb_open_close_menu" in self.__keybinds:
            self.__keybinds["kb_open_close_menu"].value = keyboard.Key.delete

        if "kb_game_lock" in self.__keybinds:
            self.__keybinds["kb_game_lock"].value = keyboard.Key.insert

        request_load_config.send(self)
        super().build()

    def __apply_loaded_binds(self, sender: Any, binds: Dict[str, Union[str, int]]) -> None:
        """
        Resolves serialized config values back into pynput Key or KeyCode objects.
        """
        if not binds:
            return

        logger.info(f"Synchronizing {len(binds)} binds from configuration")
        
        for action, value in binds.items():
            if action not in self.__keybinds:
                continue

            resolved_key: Any = value

            if isinstance(value, str):
                try:
                    resolved_key = getattr(keyboard.Key, value.lower())
                except AttributeError:
                    resolved_key = keyboard.KeyCode.from_char(value)

            self.__keybinds[action].value = resolved_key

        self.__log_active_mappings()

    def __on_keybind_change(self, action: str, key_obj: Any) -> None:
        """
        Updates the local registry and pushes changes to persistent storage and the watchdog.
        """
        btn = self.__keybinds[action]
        logger.info(f"Action '{action}' re-bound to: {btn.name}")
        
        request_save_config.send(self, registry=self.__keybinds)
        request_hotkey_sync.send(self)

    def tick(self) -> None:
        """
        Refreshes UI animation states.
        """
        for transition in self.__transitions:
            transition.tick()
            
    def __get_keybinds(self, sender: Any = None) -> Dict[str, Any]:
        """
        Returns the registry as a mapping of actions to pynput objects/ids.
        """
        if not self.__keybinds:
            return {}
        return self.keybind_registry
    
    def __log_active_mappings(self) -> None:
        """
        Outputs the current mapping state with human-readable pynput names.
        """
        logger.info("Current Keybind Mappings:")
        for tag, btn in self.__keybinds.items():
            logger.info(f"  [ {tag} ] -> {btn.name}")  

    @property
    def keybind_registry(self) -> Dict[str, Any]:
        """
        Returns the rich objects stored in the KeybindButtons.
        """
        return {
            tag: btn.value 
            for tag, btn in self.__keybinds.items()
        }