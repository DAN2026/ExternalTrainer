from typing import Dict, List, Type, Union, Callable, Any
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.memory.game import ShooterGame
from trainer.ui.handlers.base import BaseHandler
from trainer.ui.handlers.mouse import MouseHandler

from trainer.ui.components.base import BaseComponent
from trainer.ui.components.header import HeaderComponent
from trainer.ui.components.navbar import NavbarComponent
from trainer.ui.components.footer import FooterComponent

from trainer.ui.pages.base import BasePage
from trainer.ui.pages.visuals import VisualsPage
from trainer.ui.pages.debug import DebugPage
from trainer.ui.pages.logs import LogsPage
from trainer.ui.pages.settings import SettingsPage

from trainer.ui.styles import fonts, themes, icons

class App:
    """
    Main Application controller responsible for lifecycle management, 
    window configuration, and coordinating pages and components.
    """
    __slots__ = (
        "__ARK", "__active_handlers", "__registry", 
        "__HANDLERS", "__UI_ELEMENTS", "__PAGE_TAGS"
    )

    __WINDOW_WIDTH: int = 450
    __WINDOW_HEIGHT: int = 600
    __WINDOW_NAME: str = "Arkopedia"
    
    __CONTENT_X: float = 12.5
    __CONTENT_Y: float = 148.5 

    def __init__(self) -> None:
        """
        Initializes the application core services and UI definitions.
        """
        logger.info("App initializing")
        
        self.__ARK: ShooterGame = ShooterGame()
        self.__HANDLERS: List[Type[BaseHandler]] = [MouseHandler]
        self.__active_handlers: List[BaseHandler] = []
        
        self.__registry: Dict[str, Union[BaseComponent, BasePage]] = {}

        self.__UI_ELEMENTS: List[Type[Union[BaseComponent, BasePage]]] = [
            HeaderComponent,
            NavbarComponent,
            VisualsPage,
            DebugPage,
            LogsPage,
            SettingsPage,
            FooterComponent
        ]

        self.__PAGE_TAGS: List[str] = [
            "visual-container", 
            "logs-container", 
            "debug-container", 
            "settings-container"
        ]

    def __register_handlers(self) -> None:
        """
        Instantiates and registers input handlers.
        """
        for handler_class in self.__HANDLERS:
            handler = handler_class()
            handler.register() 
            self.__active_handlers.append(handler)
            
        logger.success(f"Registered handlers: {len(self.__active_handlers)}")

    def __change_page(self, target_tag: str) -> None:
        """
        Swaps the visible content area based on the provided DPG tag.

        Args:
            target_tag (str): The tag of the child window to display.
        """
        for page_tag in self.__PAGE_TAGS:
            if dpg.does_item_exist(page_tag):
                is_target = (page_tag == target_tag)
                dpg.configure_item(page_tag, show=is_target)
                
                if is_target:
                    dpg.set_item_pos(page_tag, [self.__CONTENT_X, self.__CONTENT_Y])

    def __on_tick(self) -> None:
        """
        Propagates the tick update to all active UI elements.
        """
        for element in self.__registry.values():
            element.tick()

    def start(self) -> None:
        """
        Initializes the DPG context, builds the UI, and starts the render loop.
        """
        dpg.create_context()
        
        dpg.create_viewport(
            title=self.__WINDOW_NAME, 
            width=self.__WINDOW_WIDTH, 
            height=self.__WINDOW_HEIGHT, 
            decorated=False
        )
        dpg.setup_dearpygui()

        fonts.register() 
        icons.register()

        with dpg.window(tag="main_window"):
            
            # Logic for dependency injection during instantiation
            
            element_factories: Dict[Type, Callable[[], Any]] = {
                NavbarComponent: lambda: NavbarComponent(on_page_change=self.__change_page),
                VisualsPage: lambda: VisualsPage(ark=self.__ARK),
                FooterComponent: lambda: FooterComponent(ark=self.__ARK),
                
                DebugPage: lambda: DebugPage(), 
                LogsPage: lambda: LogsPage(),
                SettingsPage: lambda: SettingsPage(),
            }

            for ui_class in self.__UI_ELEMENTS:
                factory = element_factories.get(ui_class, ui_class)
                instance = factory()
                
                instance.build()
                self.__registry[ui_class.__name__] = instance

            self.__change_page("visual-container")

        dpg.set_primary_window("main_window", True)
        dpg.show_viewport()
        
        themes.register() 
        themes.apply("main_window", themes.primary)

        self.__register_handlers()
        
        logger.success("App Started")
        
        while dpg.is_dearpygui_running():
            self.__on_tick()
            dpg.render_dearpygui_frame()
            
        dpg.destroy_context()