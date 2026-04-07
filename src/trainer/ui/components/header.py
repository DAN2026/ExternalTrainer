from trainer.ui.components.base import BaseComponent
import dearpygui.dearpygui as dpg
from trainer.ui.animations.animations import ColorTransition
from trainer.ui.common.math import Math
from trainer.ui.styles import fonts, themes

class HeaderComponent(BaseComponent):
    
    __HEIGHT: float = 25
    
    def __init__(self):
        
        self.__transitions: list[ColorTransition] = []
        super().__init__()
    
    def build(self):

        
        with dpg.child_window(tag="app-header", width=450, height=self.__HEIGHT, border=False) as header:
            
            dpg.add_spacer(height=1.5)
            
            text = dpg.add_text(
                "ARKOPEDIA",
                indent=Math.centre_text_indent(385, "ARKOPEDIA", fonts.font_bold_16)  
            )
            fonts.apply(text, fonts.font_bold_16) 
            
            themes.apply(text, themes.header_text)
            
        dpg.add_spacer(height=5)
            
        themes.apply(header, themes.header)
        
        super().build()
        
        
    def tick(self) -> None: pass
