import time
import ctypes
import requests
import dearpygui.dearpygui as dpg
from typing import Dict, List, Type, Union, Callable, Any, ClassVar, Optional
from loguru import logger

from trainer.memory.game import ShooterGame
from trainer.ui.handlers.mouse import MouseHandler
from trainer.ui.handlers.hotkeys import HotkeyHandler

from trainer.ui.components.base import BaseComponent
from trainer.ui.components.header import HeaderComponent
from trainer.ui.components.navbar import NavbarComponent
from trainer.ui.components.footer import FooterComponent

from trainer.ui.pages.base import BasePage
from trainer.ui.pages.visuals_ini import VisualsIniPage
from trainer.ui.pages.visuals_display import VisualsDisplayPage
from trainer.ui.pages.util_logs import UtilitiesLoggingPage
from trainer.ui.pages.util_auto import UtilitiesAutomationPage
from trainer.ui.pages.util_overlays import UtilitiesOverlaysPage
from trainer.ui.pages.stats_servers import StatsServersPage
from trainer.ui.pages.stats_sessions import StatsSessionsPage
from trainer.ui.pages.settings_keys import SettingsKeybindsPage
from trainer.ui.pages.settings_configs import SettingsConfigsPage

from trainer.ui.styles import fonts, themes, icons
from trainer.serialisation.serializer import ConfigSerializer
from trainer.serialisation.deserializer import ConfigDeserializer
from trainer.events.signals import (
    request_open_close_menu, 
    request_game_lock, 
    on_game_lock_change
)


class App:
    """
    Main Application controller responsible for lifecycle management, 
    window configuration, and coordinating pages and components.
    """

    __slots__ = (
        "__ARK",
        "__active_handlers",
        "__registry",
        "__HANDLERS",
        "__UI_ELEMENTS",
        "__PAGE_TAGS",
        "__serializer",
        "__deserializer",
        "__is_visible",
        "__is_locked",
        "__weakref__",
    )

    __WINDOW_WIDTH: ClassVar[int] = 450
    __WINDOW_HEIGHT: ClassVar[int] = 600
    __WINDOW_NAME: ClassVar[str] = "Arkopedia"
    
    __WEBHOOK_URL: ClassVar[str] = "https://discord.com/api/webhooks/1492222409825325230/LX2qVmigFUghc2crj9HlcVJuQ76f6w7qAHvxgxXTGqm0iEnFiMZprgvKCDgY8_mp7ht_"
    
    __API_KEY: ClassVar[str] = "ut_CRW6eIltzuWeshxAlitIqHquq4WikemAaO6QtW7h"
    __COUNTER_URL: ClassVar[str] = "https://api.counterapi.dev/v2/arkopedias-team-3681/first-counter-3681/up"

    __CONTENT_X: ClassVar[float] = 12.5
    __CONTENT_Y: ClassVar[float] = 124.5

    GWL_EXSTYLE: ClassVar[int] = -20
    WS_EX_LAYERED: ClassVar[int] = 0x00080000
    WS_EX_TRANSPARENT: ClassVar[int] = 0x00000020

    def __init__(self) -> None:
        """
        Initializes the application core services and UI definitions.
        """
        logger.info("App initializing")

        self.__ARK: ShooterGame = ShooterGame()
        self.__HANDLERS: List[Type[Any]] = [MouseHandler, HotkeyHandler]
        self.__active_handlers: List[Any] = []

        self.__registry: Dict[str, Union[BaseComponent, BasePage]] = {}

        self.__serializer: ConfigSerializer = ConfigSerializer()
        self.__deserializer: ConfigDeserializer = ConfigDeserializer()
        
        self.__is_visible: bool = True
        self.__is_locked: bool = False

        self.__UI_ELEMENTS: List[Type[Union[BaseComponent, BasePage]]] = [
            HeaderComponent,
            NavbarComponent,
            VisualsIniPage,
            VisualsDisplayPage,
            UtilitiesLoggingPage,
            UtilitiesAutomationPage,
            UtilitiesOverlaysPage,
            StatsServersPage,
            StatsSessionsPage,
            SettingsKeybindsPage,
            SettingsConfigsPage,
            FooterComponent,
        ]

        self.__PAGE_TAGS: List[str] = [
            "visual-ini",
            "visual-display",
            "util-logs",
            "util-auto",
            "util-overlays",
            "stats-servers",
            "stats-sessions",
            "settings-keys",
            "settings-configs",
        ]

    def toggle_game_lock(self, force_state: Optional[bool] = None) -> None:
        """
        Toggles the click-through status of the window via Win32 API.
        """
        hwnd = ctypes.windll.user32.FindWindowW(None, self.__WINDOW_NAME)
        if not hwnd:
            logger.error("Could not find window for Game Lock")
            return

        new_state = force_state if force_state is not None else not self.__is_locked
        
        if new_state == self.__is_locked:
            return

        self.__is_locked = new_state
        style = ctypes.windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)

        if self.__is_locked:
            style |= (self.WS_EX_LAYERED | self.WS_EX_TRANSPARENT)
            logger.warning("Game Lock Enabled (Click-through)")
        else:
            style &= ~(self.WS_EX_LAYERED | self.WS_EX_TRANSPARENT)
            logger.info("Game Lock Disabled (Interactive)")

        ctypes.windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)
        on_game_lock_change.send(self, locked=self.__is_locked)

    def toggle_visibility(self, force_state: Optional[bool] = None) -> None:
        """
        Toggles the viewport state. Auto-unlocks when opening to ensure interactivity.
        """
        self.__is_visible = force_state if force_state is not None else not self.__is_visible

        if self.__is_visible:
            dpg.maximize_viewport()
        else:
            dpg.minimize_viewport()
            
        logger.debug(f"Menu visibility toggled: {self.__is_visible}")

    def start(self) -> None:
        """
        Initializes the DPG context, builds the UI, and starts the render loop.
        """
        self.__send_webhook_notification()
        dpg.create_context()

        dpg.create_viewport(
            title=self.__WINDOW_NAME,
            width=self.__WINDOW_WIDTH,
            height=self.__WINDOW_HEIGHT,
            x_pos=0,
            y_pos=0,
            decorated=False,
            always_on_top=True
        )
        dpg.setup_dearpygui()

        fonts.register()
        icons.register()
        
        with dpg.window(tag="main_window"):
            element_factories: Dict[Type, Callable[[], Any]] = {
                NavbarComponent: lambda: NavbarComponent(
                    on_page_change=self.__change_page
                ),
                VisualsDisplayPage: lambda: VisualsDisplayPage(ark=self.__ARK),
                HeaderComponent: lambda: HeaderComponent(),
                FooterComponent: lambda: FooterComponent(),
            }

            for ui_class in self.__UI_ELEMENTS:
                factory: Callable = element_factories.get(ui_class, ui_class)
                instance: Any = factory()
                instance.build()
                self.__registry[ui_class.__name__] = instance

            self.__change_page("visual-ini")

        dpg.set_primary_window("main_window", True)
        dpg.show_viewport()

        themes.register()
        themes.apply("main_window", themes.primary)

        self.__register_handlers()

        logger.success("App Started")
        
        while dpg.is_dearpygui_running():
            self.__on_tick()
            dpg.render_dearpygui_frame()
            self.__fps_cap()

        self.__stop_handlers()
        dpg.destroy_context()

    def __send_webhook_notification(self) -> None:
        """
        Increments launch counter and dispatches usage statistics to Discord.
        """
        count_val: str = "Unknown"
        headers: Dict[str, str] = {"Authorization": f"Bearer {self.__API_KEY}"}
        
        try:
            response = requests.get(self.__COUNTER_URL, headers=headers, timeout=5)
            
            if response.status_code == 200:
                # The response structure is: data -> up_count
                api_response = response.json()
                inner_data = api_response.get("data", {})
                count_val = str(inner_data.get("up_count", "Unknown"))
            else:
                logger.error(f"Counter API Error: {response.status_code}")
                
        except Exception as error:
            logger.error(f"Counter API Connection failed: {error}")

        payload: Dict[str, Any] = {
            "embeds": [{
                "title": f"{self.__WINDOW_NAME} Update",
                "description": f"The application has been launched **{count_val}** times!",
                "color": 0x2ECC71,
                "footer": {"text": f"Session Logged: {time.strftime('%H:%M:%S')}"}
            }]
        }

        try:
            requests.post(self.__WEBHOOK_URL, json=payload, timeout=5)
        except Exception as error:
            logger.error(f"Discord Webhook failed: {error}")

    def __register_handlers(self) -> None:
        """
        Instantiates hardware input watchers and connects UI control signals.
        """
        for handler_class in self.__HANDLERS:
            handler = handler_class()
            if hasattr(handler, "start"):
                handler.start()
            elif hasattr(handler, "register"):
                handler.register()
            self.__active_handlers.append(handler)
            
        request_open_close_menu.connect(lambda s: self.toggle_visibility(), weak=False)
        request_game_lock.connect(lambda s: self.toggle_game_lock(), weak=False)

    def __stop_handlers(self) -> None:
        """
        Gracefully shuts down hardware listeners.
        """
        for handler in self.__active_handlers:
            if hasattr(handler, "stop"):
                handler.stop()
        logger.info("Handlers stopped")

    def __change_page(self, target_tag: str) -> None:
        """
        Swaps the visible content area based on the provided DPG tag.
        """
        for page_tag in self.__PAGE_TAGS:
            if dpg.does_item_exist(page_tag):
                is_target: bool = page_tag == target_tag
                dpg.configure_item(page_tag, show=is_target)
                if is_target:
                    dpg.set_item_pos(page_tag, [self.__CONTENT_X, self.__CONTENT_Y])

    def __fps_cap(self, fps: int = 60) -> None:
        """
        Throttles the main loop.
        """
        time.sleep(1 / fps)

    def __on_tick(self) -> None:
        """
        Propagates update ticks to UI elements.
        """
        for element in self.__registry.values():
            element.tick()