import threading
import webbrowser
from typing import ClassVar, Callable, Optional, List, Union, Any
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.vertical_seperator import VerticalSeparatorComponent
from trainer.ui.components.reconnect import ReconnectButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.styles import themes, fonts
from trainer.ui.animations.color import ColorTransition
from trainer.events.signals import (
    on_connection_change, 
    request_reconnect, 
    request_shutdown, 
    on_game_lock_change
)


class FooterComponent(BaseComponent):
    """
    Component responsible for rendering and handling interactions for the footer UI.

    Fully decoupled from game logic; communicates via signals for connection states.
    """

    __HEIGHT: ClassVar[float] = 55.0
    __ICON_SIZE: ClassVar[float] = 55.0
    __Y_POS: ClassVar[float] = 535.5
    __X_POS: ClassVar[float] = 12.5
    __RECONNECT_DELAY: ClassVar[float] = 0.55
    __PROMPT_DURATION: ClassVar[float] = 3.0
    __DISCORD_URL: ClassVar[str] = "https://discord.gg/yrFgV5Y3aa"

    __slots__ = (
        "__icons",
        "__reconnect_btn",
        "__logout_btn",
        "__status_label",
        "__prompt_label",
        "__lock_status_label",
        "__seperator",
        "__status",
        "__transitions",
        "__prompt_timer",
        "__reconnect_timer",
    )

    def __init__(self) -> None:
        """
        Initializes the footer and connects the UI communication signals.
        """
        super().__init__()
        self.__icons: List[IconButtonComponent] = []
        self.__reconnect_btn: Optional[ReconnectButtonComponent] = None
        self.__logout_btn: Optional[IconButtonComponent] = None
        self.__status_label: Optional[TextComponent] = None
        self.__prompt_label: Optional[TextComponent] = None
        self.__lock_status_label: Optional[TextComponent] = None
        self.__seperator: Optional[VerticalSeparatorComponent] = None
        self.__status: str = "Disconnected"
        self.__transitions: List[ColorTransition] = []
        self.__prompt_timer: Optional[threading.Timer] = None
        self.__reconnect_timer: Optional[threading.Timer] = None

        on_connection_change.connect(self.__on_connection_signal, weak=False)
        on_game_lock_change.connect(self.__on_lock_signal, weak=False)

    def build(self) -> None:
        """
        Constructs the footer layout and initializes interactive animations.
        """
        self.__add_icon(
            tag="footer-arkopedia-icon",
            icon_name="arkopedia",
            theme=themes.container,
            pos=[self.__X_POS, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            on_click=self.__on_arkopedia_click,
        )

        self.__prompt_label = TextComponent(
            tag="footer_prompt_text",
            text="",
            pos=[self.__X_POS + 75, self.__Y_POS - 7.5],
            width=250,
            height=20,
            y_indent=0,
            show=False,
            font=fonts.font_18,
            theme=themes.footer_error,
        )
        self.__prompt_label.build()

        self.__lock_status_label = TextComponent(
            tag="footer_lock_text",
            text="Menu: Unlocked",
            pos=[self.__X_POS + 75, self.__Y_POS + 10],
            width=200,
            height=20,
            y_indent=0,
            font=fonts.font_bold_18,
            theme=themes.footer_text,
        )
        self.__lock_status_label.build()

        self.__status_label = TextComponent(
            tag="footer_status_text",
            text=f"Status: {self.__status}",
            pos=[self.__X_POS + 75, self.__Y_POS + 30],
            width=200,
            height=20,
            y_indent=0,
            font=fonts.font_bold_18,
            theme=themes.footer_text,
        )
        self.__status_label.build()

        self.__logout_btn = IconButtonComponent(
            tag="footer-logout-icon",
            icon_name="logout",
            theme=themes.container,
            pos=[self.__X_POS + 285, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            icon_size=26.0,
            show=False,
            on_click=self.__on_logout_click,
            x_indent=16,
            y_indent=13.5,
        )
        self.__logout_btn.build()

        self.__reconnect_btn = ReconnectButtonComponent(
            tag="footer_reconnect_btn",
            pos=[self.__X_POS + 285, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            theme=themes.container,
            show=True,
            on_click=self.__execute_reconnect_logic,
        )
        self.__reconnect_btn.build()

        self.__seperator = VerticalSeparatorComponent(
            tag="footer_seperator",
            pos=[self.__X_POS + 355, self.__Y_POS],
            height=self.__HEIGHT,
            thickness=2.0,
            color=[255, 255, 255, 150],
        )
        self.__seperator.build()

        self.__add_icon(
            tag="footer-discord-icon",
            icon_name="discord",
            theme=themes.discord_icon,
            pos=[382.5, self.__Y_POS],
            width=self.__ICON_SIZE,
            height=self.__ICON_SIZE,
            on_click=self.__on_discord_click,
        )

        self.__transitions.append(
            ColorTransition("footer-arkopedia-icon", (20, 20, 20, 255), (0, 28, 28, 255))
        )
        self.__transitions.append(
            ColorTransition("footer-logout-icon", (20, 20, 20, 255), (28, 28, 28, 255))
        )
        self.__transitions.append(
            ColorTransition("footer_reconnect_btn", (20, 20, 20, 255), (28, 28, 28, 255))
        )
        self.__transitions.append(
            ColorTransition("footer-discord-icon", (255, 255, 255, 255), (180, 180, 180, 255))
        )

        super().build()
        request_reconnect.send(self)

    def set_status(self, connected: bool) -> None:
        """
        Updates UI visibility and labels based on signal state.
        """
        self.__status = "Connected" if connected else "Disconnected"

        if self.__status_label:
            self.__status_label.set_text(f"Status: {self.__status}")

        if self.__logout_btn:
            self.__logout_btn.toggle(show=connected)

        if self.__reconnect_btn:
            self.__reconnect_btn.toggle(show=not connected)

        self.__display_connection_prompt(connected)

    def tick(self) -> None:
        """
        Processes animations for interactive elements.
        """
        for transition in self.__transitions:
            transition.tick()

        for icon in self.__icons:
            icon.tick()

        if self.__logout_btn:
            self.__logout_btn.tick()

        if self.__reconnect_btn:
            self.__reconnect_btn.tick()

    def __on_lock_signal(self, sender: Any, locked: bool, **kwargs: Any) -> None:
        """
        Updates the lock status label text and theme when the signal is received.
        """
        if not self.__lock_status_label:
            return

        text: str = "Menu: Locked" if locked else "Menu: Unlocked"
        theme: Any = themes.footer_error if locked else themes.footer_text

        self.__lock_status_label.set_text(text)
        if dpg.does_item_exist(self.__lock_status_label.tag):
            dpg.bind_item_theme(self.__lock_status_label.tag, theme)

    def __on_connection_signal(self, sender: Any, connected: bool, **kwargs: Any) -> None:
        """
        Updates the footer status when a connection signal is received.
        """
        self.set_status(connected)

    def __cancel_prompt_timer(self) -> None:
        """
        Cancels any pending prompt hide timer.
        """
        if self.__prompt_timer and self.__prompt_timer.is_alive():
            self.__prompt_timer.cancel()
        self.__prompt_timer = None

    def __cancel_reconnect_timer(self) -> None:
        """
        Cancels any pending reconnect timer.
        """
        if self.__reconnect_timer and self.__reconnect_timer.is_alive():
            self.__reconnect_timer.cancel()
        self.__reconnect_timer = None

    def __display_connection_prompt(self, success: bool) -> None:
        """
        Displays a temporary success or error message with appropriate styling.
        """
        if not self.__prompt_label:
            return

        self.__cancel_prompt_timer()

        text: str = "Successfully connected to Ark" if success else "Ark Survival Evolved is not open"
        theme: Any = themes.footer_sucess if success else themes.footer_error

        self.__prompt_label.set_text(text)
        dpg.bind_item_theme(self.__prompt_label.tag, theme)
        self.__prompt_label.toggle(show=True)

        self.__prompt_timer = threading.Timer(
            self.__PROMPT_DURATION,
            lambda: self.__prompt_label.toggle(show=False) if self.__prompt_label else None,
        )
        self.__prompt_timer.daemon = True
        self.__prompt_timer.start()

    def __execute_reconnect_logic(self, tag: str) -> None:
        """
        Broadcasts a reconnection request after a short delay to allow animations.
        """
        logger.debug(f"Queuing reconnection request via `{tag}`...")
        self.__cancel_reconnect_timer()
        self.__reconnect_timer = threading.Timer(
            self.__RECONNECT_DELAY, lambda: request_reconnect.send(self)
        )
        self.__reconnect_timer.daemon = True
        self.__reconnect_timer.start()

    def __on_logout_click(self, tag: str) -> None:
        """
        Cancels pending timers, requests a clean shutdown, then stops DPG.
        """
        self.__cancel_prompt_timer()
        self.__cancel_reconnect_timer()
        request_shutdown.send(self)
        dpg.stop_dearpygui()

    def __on_discord_click(self, tag: str) -> None:
        """
        Redirects the user to the Discord URL.
        """
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
        Helper method to build and store icon button components.
        """
        icon_btn: IconButtonComponent = IconButtonComponent(
            tag=tag,
            icon_name=icon_name,
            theme=theme,
            pos=pos,
            width=width,
            height=height,
            on_click=on_click,
        )
        icon_btn.build()
        self.__icons.append(icon_btn)

    def __on_arkopedia_click(self, tag: str) -> None:
        """
        Branding redirect callback.
        """
        webbrowser.open(self.__DISCORD_URL)