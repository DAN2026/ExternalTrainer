from typing import ClassVar
import ctypes
import win32gui
import win32con
import dearpygui.dearpygui as dpg
from trainer.ui.styles.base import BaseStyle
from loguru import logger

class Themes(BaseStyle):

    __BG_PRIMARY: ClassVar[tuple] = (14, 14, 14, 255)
    __BG_SECONDARY: ClassVar[tuple] = (20, 20, 20, 255)
    
    __WINDOW_RADIUS: ClassVar[int] = 2
    __WINDOW_OPACITY: ClassVar[int] = 235
    __CHROMA_KEY: ClassVar[int] = 0x0000FF00

    def __init__(self, window_width: float, window_height: float, window_name: str):
        
        self.__width = window_width
        self.__height = window_height
        self.__name = window_name
        
        super().__init__()
    
    def register(self) -> None:
        
        """Call this AFTER dpg.show_viewport() so the HWND exists"""
        
        self.__setup_window(self.__width, self.__height, self.__name)
        
        logger.success("Registered Themes")
        
    def apply(self, component: int | str, theme: int) -> None:
        
        dpg.bind_item_theme(component, theme)
        
    @property
    def primary(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.__BG_PRIMARY)
        return theme
    
    @property
    def container(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_SECONDARY)
        return theme
    
    @property
    def footer_text(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_PRIMARY)
        return theme
    
    @property
    def footer_error(self) -> int:
        """
        Returns the theme identifier for the footer error state.
        
        Applies a rounded child window style and sets the text color to red.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_PRIMARY)
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0, 255])
                
        return theme
    
    @property
    def discord_icon(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))
        return theme 
    @property
    def navbar_btn_container(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_SECONDARY)
        return theme
    
    @property
    def header(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_SECONDARY)
        return theme
    
    @property
    def img_btn(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll): 
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                
        return theme

    @property
    def header_text(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,  0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 150, 255, 255))
        return theme
    
    @property
    def navbar_text(self) -> int:
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,  0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 150, 255, 255))
        return theme
    
    def __setup_window(self, width: int, height: int, name: str) -> None:
        
        hwnd = win32gui.FindWindow(None, name)

        hrgn = ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, width, height, self.__WINDOW_RADIUS * 2, self.__WINDOW_RADIUS * 2)
        
        ctypes.windll.user32.SetWindowRgn(hwnd, hrgn, True)

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
        
        win32gui.SetLayeredWindowAttributes(
            hwnd,
            self.__CHROMA_KEY,
            self.__WINDOW_OPACITY,
            win32con.LWA_COLORKEY | win32con.LWA_ALPHA,
        )

