from typing import ClassVar, Optional
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.reconnect import ReconnectButtonComponent
from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes, fonts

class SettingsPage(BasePage):
    """
    Page responsible for application configuration and UI preferences.
    """

    __slots__ = ("__reconnect_btn",)

    __HEIGHT: ClassVar[float] = 377.5
    __WIDTH: ClassVar[float] = 425.0

    def __init__(self) -> None:
        """
        Initializes the `SettingsPage`.
        """
        self.__reconnect_btn: Optional[ReconnectButtonComponent] = None
        super().__init__()

    def build(self) -> None:
        """
        Constructs the layout using the modular `ReconnectButtonComponent`.
        """
        with dpg.child_window(
            tag="settings-container",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12,
            show=False,
        ) as settings:

            dpg.add_spacer(height=10)

            with dpg.group(horizontal=True):
                header = dpg.add_text("App Settings")
                fonts.apply(header, fonts.font_bold_18)

                self.__reconnect_btn = ReconnectButtonComponent(
                    tag="settings_reconnect_btn",
                    theme=themes.container,
                    pos=[360, 5],
                    on_click=self.__execute_reconnect_logic,
                )
                self.__reconnect_btn.build()

            dpg.add_spacer(height=10)
            
            with dpg.group(indent=10):
                dpg.add_text("Settings coming soon...", color=(255, 100, 100))

        themes.apply(settings, themes.container)
        
        super().build()

    def __execute_reconnect_logic(self, tag: str) -> None:
        """
        Executes the routine for establishing a connection.

        Args:
            tag (str): The unique identifier of the calling component.
        """
        logger.debug(f"Initiating application reconnection sequence via `{tag}`...")

    def tick(self) -> None:
        """
        Ticks the self-animating components.
        """
        if self.__reconnect_btn:
            self.__reconnect_btn.tick()