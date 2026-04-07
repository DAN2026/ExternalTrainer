from typing import ClassVar, List, Any
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes, fonts

class LogsPage(BasePage):
    """
    Page responsible for displaying real-time application and injection logs.
    """
    __slots__ = ("__log_buffer",)

    __HEIGHT: ClassVar[float] = 377.5
    __WIDTH: ClassVar[float] = 425.0

    def __init__(self) -> None:
        """
        Initializes the log monitoring page.
        """
        self.__log_buffer: List[str] = []
        super().__init__()

    def build(self) -> None:
        """
        Constructs the log viewer terminal layout.
        """
        with dpg.child_window(
            tag="logs-container",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12,
            show=False
        ) as logs:
            
            dpg.add_spacer(height=10)
            
            header = dpg.add_text("Application Logs")
            fonts.apply(header, fonts.font_bold_18)
            
            with dpg.child_window(height=-1, border=True):
                dpg.add_text("Listening for events...", color=(150, 150, 150))

        themes.apply(logs, themes.container)
        super().build()

    def tick(self) -> None:
        """
        Updates the log buffer each frame.
        """
        pass