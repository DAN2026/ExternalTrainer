import time
import dearpygui.dearpygui as dpg
from typing import Tuple, Union, Optional, Dict


class FadeTransition:
    """
    Manages alpha transitions and individual item themes for independent hovering.
    """

    __slots__ = (
        "__target",
        "__duration",
        "__t",
        "__last",
        "__theme",
        "__item_themes",
        "__blue_accent",
        "__fg_rgb",
        "__bg_rgb",
    )

    def __init__(
        self,
        target: Union[str, int],
        bg_rgb: Tuple[int, int, int],
        fg_rgb: Tuple[int, int, int],
        duration: float = 0.15,
        base_theme: Optional[int] = None,
    ) -> None:
        """
        Initializes transition states and window-level theme.
        """
        self.__target: Union[str, int] = target
        self.__duration: float = duration
        self.__t: float = 0.0
        self.__last: float = time.time()
        self.__fg_rgb: Tuple[int, int, int] = fg_rgb
        self.__bg_rgb: Tuple[int, int, int] = bg_rgb
        self.__blue_accent: Tuple[int, int, int] = (1, 180, 240)
        self.__item_themes: Dict[str, int] = {}

        self.__theme: int = base_theme if base_theme and dpg.does_item_exist(base_theme) else dpg.add_theme()
        
        with dpg.theme_component(dpg.mvAll, parent=self.__theme):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (*bg_rgb, 0), tag=f"{self.__target}_win_bg")
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))

        dpg.bind_item_theme(self.__target, self.__theme)

    def add_hover_handler(self, item_tag: str) -> None:
        """
        Creates a unique theme per button to isolate text color from the rest of the UI.
        """
        theme: int = dpg.add_theme()
        with dpg.theme_component(dpg.mvButton, parent=theme):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (*self.__fg_rgb, 0), tag=f"{item_tag}_txt")

        self.__item_themes[item_tag] = theme
        dpg.bind_item_theme(item_tag, theme)

        with dpg.item_handler_registry() as registry:
            dpg.add_item_hover_handler(
                callback=lambda: dpg.set_value(f"{item_tag}_txt", (*self.__blue_accent, int(255 * self.__t)))
            )
            dpg.add_item_visible_handler(
                callback=lambda: dpg.set_value(f"{item_tag}_txt", (*self.__fg_rgb, int(255 * self.__t))) 
                if not dpg.is_item_hovered(item_tag) else None
            )
        dpg.bind_item_handler_registry(item_tag, registry)

    def tick(self, active: bool) -> None:
        """
        Interpolates alpha values and updates individual button text colors.
        """
        now: float = time.time()
        delta: float = now - self.__last
        self.__last = now

        direction: int = 1 if active else -1
        if (direction == 1 and self.__t >= 1.0) or (direction == -1 and self.__t <= 0.0):
            return

        self.__t = max(0.0, min(1.0, self.__t + direction * (delta / self.__duration)))
        alpha: int = int(255 * self.__t)

        dpg.set_value(f"{self.__target}_win_bg", (*self.__bg_rgb, alpha))

        for item_tag in self.__item_themes:
            color = self.__blue_accent if dpg.is_item_hovered(item_tag) else self.__fg_rgb
            dpg.set_value(f"{item_tag}_txt", (*color, alpha))

    @property
    def progress(self) -> float:
        """
        Current animation progress 0.0 to 1.0.
        """
        return self.__t