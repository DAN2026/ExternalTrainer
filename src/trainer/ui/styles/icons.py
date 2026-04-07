from trainer.ui.styles.base import BaseStyle
from loguru import logger
import dearpygui.dearpygui as dpg
from pathlib import Path
from typing import ClassVar


class Icons(BaseStyle):
    
    
    def __init__(self):
        
        self.__textures: dict[str, int] = {}
        
        super().__init__()
    
    ICONS_DIR: ClassVar[Path] = Path(__file__).parent / "icons"
    
    ICONS: ClassVar[list[str]] = [
        "eye",
        "bug",
        "settings",
        "logs",
        "discord",
        "arkopedia",
        "logout"
    ]

    def register(self) -> None:
        with dpg.texture_registry():
            for name in self.ICONS:
                path = str(self.ICONS_DIR / f"{name}.png")
                width, height, _, data = dpg.load_image(path)
                self.__textures[name] = dpg.add_static_texture(width, height, data)
                
    def apply(self, name: str) -> int:
        return self.__textures[name]
    
    