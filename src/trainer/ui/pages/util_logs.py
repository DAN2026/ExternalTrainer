from typing import ClassVar, Dict, List, Any
import dearpygui.dearpygui as dpg
from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes
from trainer.ui.components.toggle import Toggle
from trainer.ui.components.toggle_row import ToggleRowComponent
from trainer.ui.animations.color import ColorTransition


class UtilitiesLoggingPage(BasePage):
    """
    Handles system logging display and verbosity toggles.
    """

    __slots__ = ("__toggles", "__transitions")

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0
    __ROW_WIDTH: ClassVar[float] = 400.0

    def __init__(self) -> None:
        self.__toggles: Dict[str, Toggle] = {}
        self.__transitions: List[ColorTransition] = []
        super().__init__()

    def build(self) -> None:
        with dpg.child_window(
            tag="util-logs",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12.5,
            show=False,
        ) as container:
            dpg.add_spacer(height=10)
            with dpg.group(tag="logs-group-container"):
                ToggleRowComponent(
                    "enable_logging", "Enable Logging", "folder",
                    on_true=lambda: print("Logging Enabled"),
                    on_false=lambda: print("Logging Disabled"),
                    width=self.__ROW_WIDTH
                ).build(self.__toggles, self.__transitions)

        themes.apply(container, themes.container)
        super().build()

    def tick(self) -> None:
        for toggle in self.__toggles.values():
            toggle.tick()
        for transition in self.__transitions:
            transition.tick()