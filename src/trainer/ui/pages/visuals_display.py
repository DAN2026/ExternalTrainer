from typing import ClassVar, List, Optional, Any, Dict
import dearpygui.dearpygui as dpg
from loguru import logger
from trainer.ui.pages.base import BasePage
from trainer.ui.styles import themes
from trainer.ui.components.slider_row import SliderRowComponent
from trainer.ui.components.search_bar import SearchBarComponent
from trainer.ui.animations.color import ColorTransition
from trainer.memory.game import ShooterGame
from trainer.events import signals


class VisualsDisplayPage(BasePage):
    """
    Handles display modifications and batched group sliders with active syncing.
    """

    __slots__ = ("__ARK", "__transitions", "__last_conn_state", "__display_data")

    __HEIGHT: ClassVar[float] = 395.0
    __WIDTH: ClassVar[float] = 425.0
    __ROW_WIDTH: ClassVar[float] = 400.0

    def __init__(self, ark: ShooterGame) -> None:
        self.__ARK: ShooterGame = ark
        self.__transitions: List[ColorTransition] = []
        self.__last_conn_state: bool = False
        self.__display_data: Dict[str, str] = {
            "fov": "FOV",
            "gamma": "Gamma",
            "vd": "View Dist",
            "test_ini": "Ini Test",
            "lighting_grp": "Lighting",
            "grass_grp": "Grass",
            "texture_grp": "Texture",
            "mip": "Mipbias",
            "shadows_grp": "Shadows",
        }
        super().__init__()

    def build(self) -> None:
        with dpg.child_window(
            tag="visual-display",
            width=self.__WIDTH,
            height=self.__HEIGHT,
            border=False,
            indent=12.5,
            show=False,
        ) as container:

            with dpg.theme() as scroll_theme:
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 14.0)
                    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 0.0)

            dpg.bind_item_theme(container, scroll_theme)
            
            SearchBarComponent(
                tag="display_search",
                hint="Search display settings...",
                icon="search",
                width=self.__ROW_WIDTH,
                padding_top=5.0,
                data_map=self.__display_data
            ).build(self.__transitions)

            with dpg.group(tag="display-group-container"):
                configs = {
                    "fov": lambda: SliderRowComponent("fov", "FOV", 0.0, 2.0, 1.25, lambda s, v: signals.set_fov.send(self, value=v), width=self.__ROW_WIDTH).build(self.__transitions),
                    "gamma": lambda: SliderRowComponent("gamma", "Gamma", 0.0, 5.0, 2.2, lambda s, v: signals.set_gamma.send(self, value=v), width=self.__ROW_WIDTH).build(self.__transitions),
                    "vd": lambda: SliderRowComponent("vd", "View Dist", 0.0, 2.0, 1.0, lambda s, v: signals.set_view_distance.send(self, value=v), width=self.__ROW_WIDTH).build(self.__transitions),
                    "test_ini": lambda: SliderRowComponent("test_ini", "Ini Test", 0, 10, 0.0, lambda s, v: signals.set_testing_ini.send(self, value=v), width=self.__ROW_WIDTH).build(self.__transitions),
                    "lighting_grp": lambda: SliderRowComponent("lighting_grp", "Lighting", 0.0, 1.0, 0.5, lambda s, v: print(f"Batch: Lighting -> {v}"), width=self.__ROW_WIDTH).build(self.__transitions),
                    "grass_grp": lambda: SliderRowComponent("grass_grp", "Grass", 0.0, 1.0, 0.5, lambda s, v: print(f"Batch: Grass -> {v}"), width=self.__ROW_WIDTH).build(self.__transitions),
                    "texture_grp": lambda: SliderRowComponent("texture_grp", "Texture", 0.0, 1.0, 0.5, lambda s, v: print(f"Batch: Texture -> {v}"), width=self.__ROW_WIDTH).build(self.__transitions),
                    "mip": lambda: SliderRowComponent("mip", "Mipbias", 0, 100000, 100000, lambda s, v: signals.set_mipbias.send(self, value=v), width=self.__ROW_WIDTH).build(self.__transitions),
                    "shadows_grp": lambda: SliderRowComponent("shadows_grp", "Shadows", 0.0, 1.0, 0.5, lambda s, v: print(f"Batch: Shadows -> {v}"), width=self.__ROW_WIDTH).build(self.__transitions),
                }

                for tag in self.__display_data:
                    with dpg.group(tag=f"{tag}_row"):
                        configs[tag]()

        themes.apply(container, themes.container)
        super().build()

    def __handle_connection_watchdog(self) -> None:
        curr: bool = self.__ARK.is_connected
        if curr != self.__last_conn_state:
            if curr:
                logger.info("ShooterGame detected: Syncing Display.")
                self.__sync_settings()
            self.__last_conn_state = curr

    def __sync_settings(self) -> None:
        sync_map = {
            "fov_slider": signals.get_fov,
            "gamma_slider": signals.get_gamma,
            "vd_slider": signals.get_view_distance,
        }

        for tag, sig in sync_map.items():
            if not dpg.does_item_exist(tag):
                continue
                
            resp = sig.send(self)
            if resp:
                _, val = resp[0]
                if val is not None:
                    dpg.set_value(tag, val)
                    logger.debug(f"Synced {tag} to {val}")

    def tick(self) -> None:
        self.__handle_connection_watchdog()
        for trans in self.__transitions:
            trans.tick()