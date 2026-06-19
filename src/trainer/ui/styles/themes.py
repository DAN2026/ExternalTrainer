from typing import ClassVar, Tuple, Union, Optional, List
import ctypes
import win32gui
import win32con
import dearpygui.dearpygui as dpg
from trainer.ui.styles.base import BaseStyle
from loguru import logger


class Themes(BaseStyle):
    """
    `Themes` manages the global and component-specific styling for the application,
    utilizing Windows API for advanced window effects.
    """

    __BG_PRIMARY: ClassVar[Tuple[int, int, int, int]] = (14, 14, 14, 255)
    __BG_SECONDARY: ClassVar[Tuple[int, int, int, int]] = (20, 20, 20, 255)
    __BG_THIRD: ClassVar[Tuple[int, int, int, int]] = (16, 16, 16, 255)
    __BG_SLIDERS: ClassVar[Tuple[int, int, int, int]] = (24, 24, 24, 255)
    __BG_TOOLTIP: ClassVar[Tuple[int, int, int, int]] = (32, 32, 32, 255)

    __BLUE: ClassVar[Tuple[int, int, int, int]] = (1, 180, 240, 255)

    __WINDOW_RADIUS: ClassVar[int] = 2
    __WINDOW_OPACITY: ClassVar[int] = 248
    __CHROMA_KEY: ClassVar[int] = 0x0000FF00

    __slots__ = ("__width", "__height", "__name")

    def __init__(self, window_width: float, window_height: float, window_name: str) -> None:
        """
        Initializes the Themes manager.
        """
        self.__width: float = window_width
        self.__height: float = window_height
        self.__name: str = window_name
        super().__init__()

    def register(self) -> None:
        """
        Initializes the low-level window styling and rounding via Win32 API.
        """
        self.__setup_window(int(self.__width), int(self.__height), self.__name)
        logger.success("Registered Themes")

    def apply(self, component: Union[int, str], theme: int) -> None:
        """
        Binds a specific theme to a UI component.
        """
        dpg.bind_item_theme(component, theme)

    @property
    def primary(self) -> int:
        """
        Global window theme configuration.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.__BG_PRIMARY)
        return theme

    @property
    def container(self) -> int:
        """
        Standard container theme for child windows.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_SECONDARY)
        return theme


    @property
    def keybind_btn(self) -> int:
        """
        Theme for the KeybindButton component using the third background tier.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (26, 26, 26, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (32, 32, 32, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.__BLUE)
                
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
                
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220, 255))
                
        return theme

    @property
    def tooltip(self) -> int:
        """
        Theme for floating tooltip windows.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_TOOLTIP)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 60, 60, 255))
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220, 255))
        return theme

    @property
    def footer_text(self) -> int:
        """
        Theme for the footer text container.
        """
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
        Theme identifier for the footer error state with red text.
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
    def footer_sucess(self) -> int:
        """
        Theme identifier for the footer error state with red text.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_PRIMARY)
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 255, 0, 255])
        return theme
    
    @property
    def header(self) -> int:
        """
        Header container theme.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_SECONDARY)
        return theme

    @property
    def visuals_item(self) -> int:
        """
        Theme for list items that allows background transparency for parent animations.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 0))
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
        return theme
    
    @property
    def navbar_dropdown(self) -> int:
        """
        Theme for navbar_dropdown with specific styling.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 4, 4)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
                
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.__BG_PRIMARY)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.__BG_PRIMARY)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (36, 36, 36, 255))

        return theme

    @property
    def slider_float_theme(self) -> int:
        """
        Float slider theme with transparent background.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvSliderFloat):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (25, 25, 25, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (30, 30, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (35, 35, 35, 255))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, self.__BLUE)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (0, 120, 215))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 12)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
        return theme

    @property
    def discord_icon(self) -> int:
        """
        Theme for the Discord icon container.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255, 255))
        return theme

    @property
    def navbar_btn_container(self) -> int:
        """
        Theme for the navbar button container.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.__BG_SECONDARY)
        return theme

    @property
    def img_btn(self) -> int:
        """
        Theme for image buttons focusing on layout reset.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
        return theme

    @property
    def header_text(self) -> int:
        """
        Header text styling with blue accent color.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.__BLUE)
        return theme
    
    @property
    def tooltip_window(self) -> int:
        """
        Theme for floating tooltip windows with white text and matching background.
        """
        white: Tuple[int, int, int, int] = (255, 255, 255, 255)
        
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.__BG_SECONDARY)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 60, 60, 255))
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 4)
            
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, white)
                
        return theme
    
    @property
    def navbar_text(self) -> int:
        """
        Navbar text styling with specific blue variation.
        """
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 150, 255, 255))
        return theme

    def __setup_window(self, width: int, height: int, name: str) -> None:
        """
        Configures OS-level window attributes including rounding and layered transparency.
        """
        hwnd = win32gui.FindWindow(None, name)
        hrgn = ctypes.windll.gdi32.CreateRoundRectRgn(
            0, 0, width, height, 
            self.__WINDOW_RADIUS * 2, 
            self.__WINDOW_RADIUS * 2
        )
        ctypes.windll.user32.SetWindowRgn(hwnd, hrgn, True)

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(
            hwnd,
            self.__CHROMA_KEY,
            self.__WINDOW_OPACITY,
            win32con.LWA_COLORKEY | win32con.LWA_ALPHA,
        )