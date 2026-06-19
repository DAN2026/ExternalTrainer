from typing import ClassVar, Dict, List, Tuple, Any
import dearpygui.dearpygui as dpg
from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes
from trainer.ui.components.toggle import Toggle
from trainer.ui.components.toggle_row import ToggleRowComponent
from trainer.ui.components.search_bar import SearchBarComponent
from trainer.ui.animations.color import ColorTransition
from trainer.events.signals import (
    set_ini,
    set_environment,
    set_beer,
    set_fullbright,
    set_no_trees,
    set_scouting,
    set_pretty,
    set_no_structures,
    request_normal_ini,
    request_hard_ini,
    request_toggle_no_water,
    request_toggle_fullbright,
    request_toggle_beer_xz,
    request_toggle_environment
)


class VisualsIniPage(BasePage):
    """
    Handles INI-specific modifications and preset mutual exclusivity.
    """

    __slots__ = ("__toggles", "__transitions", "__ini_data")

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0
    __ROW_WIDTH: ClassVar[float] = 400.0

    def __init__(self) -> None:
        self.__toggles: Dict[str, Toggle] = {}
        self.__transitions: List[ColorTransition] = []
        self.__ini_data: Dict[str, str] = {
            "normal_ini": "Normal INI",
            "hard_ini": "Hard INI",
            "no_water": "No Water",
            "fullbright": "Fullbright",
            "beer_xz": "Beer / XZ",
            "no_environment": "No Environment",
            "no_trees": "No Tree (NA)",
            "scouting": "Scouting (NA)",
            "pretty": "Pretty (NA)",
            "no_structures": "No structures (NA)",
        }
        
        self.__setup_signal_connections()
        super().__init__()

    def build(self) -> None:
        with dpg.child_window(
            tag="visual-ini",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12.5,
            show=False,
        ) as container:
            
            with dpg.theme() as scroll_theme:
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 14.0)
                    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 0.0)
            
            dpg.bind_item_theme(container, scroll_theme)
            
            SearchBarComponent(
                tag="ini_search",
                hint="Search INI settings...",
                icon="search",
                width=self.__ROW_WIDTH,
                padding_top=5.0,
                data_map=self.__ini_data
            ).build(self.__transitions)

            with dpg.group(tag="ini-group-container"):
                configs = {
                    "normal_ini": lambda: ToggleRowComponent("normal_ini", "Normal INI", "folder", callback=lambda s: self.__on_ini_toggle("normal_ini", 3), default_state=True, width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "hard_ini": lambda: ToggleRowComponent("hard_ini", "Hard INI", "folder", callback=lambda s: self.__on_ini_toggle("hard_ini", 1), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "no_water": lambda: ToggleRowComponent("no_water", "No Water", "folder", callback=lambda s: self.__on_ini_toggle("no_water", 6), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "fullbright": lambda: ToggleRowComponent("fullbright", "Fullbright", "folder", on_true=lambda: set_fullbright.send(self, state=True), on_false=lambda: set_fullbright.send(self, state=False), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "beer_xz": lambda: ToggleRowComponent("beer_xz", "Beer / XZ", "folder", on_true=lambda: set_beer.send(self, state=True), on_false=lambda: set_beer.send(self, state=False), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "no_environment": lambda: ToggleRowComponent("no_environment", "No Environment", "folder", on_true=lambda: set_environment.send(self, state=True), on_false=lambda: set_environment.send(self, state=False), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "no_trees": lambda: ToggleRowComponent("no_trees", "No Tree (NA)", "folder", on_true=lambda: set_no_trees.send(self, state=True), on_false=lambda: set_no_trees.send(self, state=False), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "scouting": lambda: ToggleRowComponent("scouting", "Scouting (NA)", "folder", on_true=lambda: set_scouting.send(self, state=True), on_false=lambda: set_scouting.send(self, state=False), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "pretty": lambda: ToggleRowComponent("pretty", "Pretty (NA)", "folder", on_true=lambda: set_pretty.send(self, state=True), on_false=lambda: set_pretty.send(self, state=False), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                    "no_structures": lambda: ToggleRowComponent("no_structures", "No structures (NA)", "folder", on_true=lambda: set_no_structures.send(self, state=True), on_false=lambda: set_no_structures.send(self, state=False), width=self.__ROW_WIDTH).build(self.__toggles, self.__transitions),
                }

                for tag in self.__ini_data:
                    with dpg.group(tag=f"{tag}_row"):
                        configs[tag]()
                
        themes.apply(container, themes.container)
        super().build()

    def __on_ini_toggle(self, clicked_key: str, ini_value: int) -> None:
        presets: Tuple[str, ...] = ("normal_ini", "hard_ini", "no_water")

        if self.__toggles[clicked_key].value:
            for key in presets:
                if key != clicked_key:
                    self.__toggles[key].value = False
            set_ini.send(self, value=ini_value)
        else:
            self.__toggles["normal_ini"].value = True
            set_ini.send(self, value=3)

    def tick(self) -> None:
        for toggle in self.__toggles.values():
            toggle.tick()
        for transition in self.__transitions:
            transition.tick()
            
            
    def __setup_signal_connections(self) -> None:
        """
        Initializes signal connections for hotkey requests.
        """
        request_normal_ini.connect(
            lambda s: self.__handle_ini_request("normal_ini", 3),
            weak=False
        )
        request_hard_ini.connect(
            lambda s: self.__handle_ini_request("hard_ini", 1),
            weak=False
        )
        request_toggle_no_water.connect(
            lambda s: self.__handle_ini_request("no_water", 6),
            weak=False
        )
        request_toggle_fullbright.connect(
            lambda s: self.__handle_toggle_request("fullbright", set_fullbright),
            weak=False
        )
        request_toggle_beer_xz.connect(
            lambda s: self.__handle_toggle_request("beer_xz", set_beer),
            weak=False
        )
        request_toggle_environment.connect(
            lambda s: self.__handle_toggle_request("no_environment", set_environment),
            weak=False
        )

    def __handle_ini_request(self, key: str, value: int) -> None:
        """
        Updates toggle state and triggers INI logic for hotkeys.
        """
        
        print(key)
        
        if key in self.__toggles:
            self.__toggles[key].value = True
            self.__on_ini_toggle(key, value)

    def __handle_toggle_request(self, key: str, signal: Any) -> None:
        """
        Inverts binary toggle state and fires associated signal.
        """
        if key in self.__toggles:
            new_state = not self.__toggles[key].value
            self.__toggles[key].value = new_state
            signal.send(self, state=new_state)