from typing import ClassVar, List
import dearpygui.dearpygui as dpg
from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes
from trainer.ui.animations.color import ColorTransition


class SettingsConfigsPage(BasePage):
    """
    Manages loading, saving, and exporting configuration profiles.
    """

    __slots__ = ("__transitions",)

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0

    def __init__(self) -> None:
        self.__transitions: List[ColorTransition] = []
        super().__init__()

    def build(self) -> None:
        with dpg.child_window(
            tag="settings-configs",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12.5,
            show=False,
        ) as container:
            dpg.add_spacer(height=10)
            dpg.add_text("Profile & Config Management")

        themes.apply(container, themes.container)
        super().build()

    def tick(self) -> None:
        for transition in self.__transitions:
            transition.tick()