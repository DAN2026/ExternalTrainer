from typing import ClassVar, Dict, List, Tuple, Callable, Any
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.pages.base import BasePage
from trainer.ui.styles import fonts, themes
from trainer.ui.common.math import Math
from trainer.ui.components.toggle import Toggle
from trainer.memory.game import ShooterGame


class VisualsPage(BasePage):
    """
    Component handling the visual memory modifications and preset INI toggles.
    """
    __slots__ = ("__ARK", "__toggles", "__transitions")

    __DEFAULT_FOV: ClassVar[float] = 1.25
    __HEIGHT: ClassVar[float] = 377.5
    __WIDTH: ClassVar[float] = 425
    
    def __init__(self, ark: ShooterGame) -> None:
        """
        Initializes the visuals component with a shared game memory instance.

        Args:
            ark (ShooterGame): The memory management instance for game values.
        """
        self.__ARK: ShooterGame = ark
        self.__toggles: Dict[str, Toggle] = {}
        self.__transitions: List[Any] = []
        
        self.__apply_normal_ini()
        super().__init__()

    def build(self) -> None:
        """
        Constructs the UI layout, including the toggle columns and FOV slider.
        """
        options: List[str] = [
            "Normal INI", "Hard INI", "Potato INI", "No Water",
            "Fullbright", "Beer / XZ", "No Trees", "Fov",
        ]

        toggles_metadata: List[Tuple[str, str]] = [
            ("normal_ini", "Normal INI"),
            ("hard_ini", "Hard INI"),
            ("potato_ini", "Potato INI"),
            ("no_water", "No Water"),
            ("fullbright", "Fullbright"),
            ("beer_xz", "Beer / XZ"),
            ("no_trees", "No Trees"),
        ]

        with dpg.child_window(
            tag="visual-container", 
            width=self.__WIDTH, 
            height=self.__HEIGHT, 
            border=False, 
            indent=12.5, 
            show=False
        ) as visuals:

            dpg.add_spacer(height=10)

            with dpg.group(tag="visual-group-container", horizontal=True, horizontal_spacing=25, indent=35):

                with dpg.group(tag="visual-group-1"):
                    for option in options:
                        text_item = dpg.add_text(option)
                        fonts.apply(text_item, fonts.font_bold_18)
                        dpg.add_spacer(height=10)

                with dpg.group(tag="visual-group-2"):
                    for key, label in toggles_metadata:
                        self.__toggles[key] = Toggle(
                            parent="visual-group-2",
                            label=label,
                            default_state=False,
                            width=44,
                            height=24,
                            callback=lambda state, k=key: self.__on_toggle_clicked(k, state)
                        )
                        self.__toggles[key].build()
                        dpg.add_spacer(height=10)

                    self.__toggles["normal_ini"].value = True

                    dpg.add_spacer(height=1)
                    dpg.add_slider_float(
                        label="##fov_slider",
                        default_value=self.__ARK.fov.get() or self.__DEFAULT_FOV,
                        min_value=0.0,
                        max_value=2.0,
                        callback=lambda sender, data: self.__apply_fov(sender, data)
                    )

        themes.apply(visuals, themes.container)
        super().build()

    def __on_toggle_clicked(self, clicked_key: str, state: bool) -> None:
        """
        Routes toggle interactions to exclusive or independent handlers.
        """
        ini_presets: Dict[str, Callable] = {
            "normal_ini": self.__apply_normal_ini,
            "hard_ini": self.__apply_hard_ini,
            "potato_ini": self.__apply_potato_ini,
            "no_water": self.__apply_no_water,
        }

        if clicked_key in ini_presets:
            self.__handle_conflicting_toggles(clicked_key, ini_presets)
        else:
            self.__handle_utility_toggles(clicked_key, state)

    def __handle_conflicting_toggles(self, clicked_key: str, presets: Dict[str, Callable]) -> None:
        """
        Manages mutually exclusive toggles within the INI preset group.
        """
        is_active: bool = self.__toggles[clicked_key].value

        if is_active:
            for key in presets:
                if key != clicked_key:
                    self.__toggles[key].value = False
            presets[clicked_key]()
        else:
            self.__toggles["normal_ini"].value = True
            self.__apply_normal_ini()

    def __handle_utility_toggles(self, key: str, state: bool) -> None:
        """
        Handles standalone utility modifications.
        """
        if key == "fullbright":
            logger.info(f"Fullbright toggled: {state}")
        elif key == "beer_xz":
            logger.info(f"Beer / XZ toggled: {state}")
        elif key == "no_trees":
            logger.info(f"No Trees toggled: {state}")

    def __apply_normal_ini(self) -> None:
        """Applies normal visual settings (Value 3)."""
        self.__ARK.ini.set(3)

    def __apply_hard_ini(self) -> None:
        """Applies hard visual settings (Value 1)."""
        self.__ARK.ini.set(1)

    def __apply_potato_ini(self) -> None:
        """Applies low-poly potato visual settings."""
        logger.info("Potato INI activated.")

    def __apply_no_water(self) -> None:
        """Applies the no-water visual setting (Value 6)."""
        self.__ARK.ini.set(6)

    def __apply_fov(self, sender: int | str, app_data: float) -> None:
        """
        Updates the game FOV memory value.
        
        Args:
            sender (int | str): The slider widget tag.
            app_data (float): The new FOV value from the slider.
        """
        self.__ARK.fov.set(app_data)
        logger.info(f"FOV updated by {sender} to {app_data}")

    def tick(self) -> None:
        """
        Processes frame updates for all registered toggle animations.
        """
        for toggle in self.__toggles.values():
            toggle.tick()