from typing import ClassVar, Dict, List, Any
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes, fonts

class DebugPage(BasePage):
    """
    Page responsible for displaying engine internals and memory diagnostic tools.
    """
    __slots__ = ("__transitions", "__registry")

    __HEIGHT: ClassVar[float] = 377.5
    __WIDTH: ClassVar[float] = 425.0

    def __init__(self) -> None:
        """
        Initializes the debug page state.
        """
        self.__transitions: List[Any] = []
        self.__registry: Dict[str, Any] = {}
        super().__init__()

    def build(self) -> None:
        """
        Constructs the debug information layout.
        """
        with dpg.child_window(
            tag="debug-container",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12,
            show=False
        ) as debug:
            
            dpg.add_spacer(height=10)
            
            header = dpg.add_text("Debug Diagnostics")
            fonts.apply(header, fonts.font_bold_18)
            
            dpg.add_spacer(height=5)
            
            dpg.add_text("Engine metrics and memory offsets coming soon...", color=(200, 200, 200))

        themes.apply(debug, themes.container)
        super().build()

    def tick(self) -> None:
        """
        Processes frame updates for debug metrics.
        """
        pass