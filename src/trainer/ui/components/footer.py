import threading
import webbrowser
from typing import ClassVar, Callable, Optional, List, Union
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.memory.game import ShooterGame
from trainer.ui.components.base import BaseComponent
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.vertical_seperator import VerticalSeparatorComponent
from trainer.ui.components.reconnect import ReconnectButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.styles import themes, fonts


class FooterComponent(BaseComponent):
    """
    Component responsible for rendering and handling interactions for the footer UI.

    Manages the status label, navigation icons, and error feedback when 
    process attachment fails.
    """

    __slots__ = (
        "__ark",
        "__icons",
        "__reconnect_btn",
        "__logout_btn",
        "__status_label",
        "__error_label",
        "__seperator",
        "__status",
    )

    __HEIGHT: ClassVar[float] = 55.0
    __ICON_SIZE: ClassVar[float] = 55.0
    __Y_POS: ClassVar[float] = 535.5
    __X_POS: ClassVar[float] = 12.5
    __RECONNECT_DELAY: ClassVar[float] = 0.55
    __ERROR_DURATION: ClassVar[float] = 3.0
    __DISCORD_URL: ClassVar[str] = "https://discord.gg/XXQNVqzm2G"

    def __init__(self, ark: ShooterGame) -> None:
        """
        Initializes the footer component with the game state reference.

        Args:
            ark (ShooterGame): The live game state controller.
        """
        super().__init__()
        self.__ark: ShooterGame = ark
        self.__icons: List[IconButtonComponent] = []
        self.__reconnect_btn: Optional[ReconnectButtonComponent] = None
        self.__logout_btn: Optional[IconButtonComponent] = None
        self.__status_label: Optional[TextComponent] = None
        self.__error_label: Optional[TextComponent] = None
        self.__seperator: Optional[VerticalSeparatorComponent] = None
        self.__status: str = "Connected"

    def build(self) -> None:
        """
        Constructs the footer layout and handles initial positioning.
        """
        self.__add_icon(
            tag="footer-arkopedia-icon",
            icon_name="arkopedia",
            theme=themes.container,
            pos=[self.__X_POS, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            on_click=self.__on_arkopedia_click
        )

        self.__error_label = TextComponent(
            tag="footer_error_text",
            text="Ark Survival Evolved is not open",
            pos=[self.__X_POS + 75, self.__Y_POS + 10],
            width=200,
            height=20,
            y_indent=0,
            show=False,
            font=fonts.font_18,
            theme=themes.footer_error
        )
        self.__error_label.build()

        self.__status_label = TextComponent(
            tag="footer_status_text",
            text=f"Status: {self.__status}",
            pos=[self.__X_POS + 75, self.__Y_POS + 30],
            width=200,
            height=20,
            y_indent=0,
            font=fonts.font_bold_18,
            theme=themes.footer_text
        )
        self.__status_label.build()

        self.__logout_btn = IconButtonComponent(
            tag="footer-logout-icon",
            icon_name="logout",
            theme=themes.container,
            pos=[self.__X_POS + 285, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            icon_size=32.0,
            show=True,
            on_click=self.__on_logout_click,
            x_indent=15,
            y_indent=12.5
        )
        self.__logout_btn.build()

        self.__reconnect_btn = ReconnectButtonComponent(
            tag="footer_reconnect_btn",
            pos=[self.__X_POS + 285, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            theme=themes.container,
            show=False,
            on_click=self.__execute_reconnect_logic
        )
        self.__reconnect_btn.build()

        self.__seperator = VerticalSeparatorComponent(
            tag="footer_seperator",
            pos=[self.__X_POS + 355, self.__Y_POS],
            height=self.__HEIGHT,
            thickness=2.0,
            color=[255, 255, 255, 150]
        )
        self.__seperator.build()

        self.__add_icon(
            tag="footer-discord-icon",
            icon_name="discord",
            theme=themes.discord_icon,
            pos=[382.5, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            on_click=self.__on_discord_click
        )

        self.set_status(self.__ark.is_connected)
        super().build()

    def set_status(self, connected: bool) -> None:
        """
        Updates UI visibility and label text based on connection state.

        Args:
            connected (bool): True if the game process is attached.
        """
        self.__status = "Connected" if connected else "Disconnected"
        
        if self.__status_label:
            self.__status_label.set_text(f"Status: {self.__status}")

        if self.__logout_btn:
            self.__logout_btn.toggle(show=connected)

        if self.__reconnect_btn:
            self.__reconnect_btn.toggle(show=not connected)

    def tick(self) -> None:
        """
        Updates interaction polling and monitors for unexpected game disconnection.
        """
        for icon in self.__icons:
            icon.tick()

        if self.__logout_btn:
            self.__logout_btn.tick()

        if self.__reconnect_btn:
            self.__reconnect_btn.tick()

        if self.__status == "Connected" and not self.__ark.is_connected:
            self.set_status(False)

    def __execute_reconnect_logic(self, tag: str) -> None:
        """
        Attempts to re-attach to the game and triggers temporary error if it fails.

        Args:
            tag (str): The DPG tag of the button that triggered the event.
        """
        logger.debug(f"Attempting game reconnection via `{tag}`...")
        success: bool = self.__ark.reconnect()
        
        if not success and self.__error_label:
            self.__error_label.toggle(show=True)
            threading.Timer(
                self.__ERROR_DURATION, 
                lambda: self.__error_label.toggle(show=False)
            ).start()
        
        threading.Timer(
            self.__RECONNECT_DELAY, 
            lambda: self.set_status(success)
        ).start()

    def __on_logout_click(self, tag: str) -> None:
        """
        Gracefully terminates the Dear PyGui application.

        Args:
            tag (str): The DPG tag of the button that triggered the event.
        """
        logger.info(f"Logout triggered via `{tag}`. Closing application...")
        dpg.stop_dearpygui()

    def __on_discord_click(self, tag: str) -> None:
        """
        Opens the Discord invite link in the user's default web browser.

        Args:
            tag (str): The DPG tag of the button that triggered the event.
        """
        logger.info(f"Opening Discord link via `{tag}`...")
        webbrowser.open(self.__DISCORD_URL)

    def __add_icon(
        self,
        tag: str,
        icon_name: str,
        theme: Union[int, str],
        pos: List[float],
        width: float,
        height: float,
        on_click: Optional[Callable[[str], None]] = None,
    ) -> None:
        """
        Helper to instantiate and register an `IconButtonComponent`.
        """
        icon_btn = IconButtonComponent(
            tag=tag,
            icon_name=icon_name,
            theme=theme,
            pos=pos,
            width=width,
            height=height,
            on_click=on_click
        )
        icon_btn.build()
        self.__icons.append(icon_btn)

    def __on_arkopedia_click(self, tag: str) -> None:
        """Callback for Arkopedia branding."""
        webbrowser.open(self.__DISCORD_URL)