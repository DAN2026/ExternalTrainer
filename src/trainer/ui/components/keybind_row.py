from typing import Dict, List, Tuple, Callable, Optional
import dearpygui.dearpygui as dpg
from trainer.ui.components.keybind_button import KeybindButton
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.animations.color import ColorTransition
from trainer.ui.styles import fonts, themes


class KeybindRowComponent:
    """
    KeybindRowComponent encapsulates a standardized UI row with a 
    KeybindButton for hardware input mapping.
    """

    __slots__ = (
        "__tag",
        "__key",
        "__label",
        "__icon",
        "__callback",
        "__default_key",
        "__width",
        "__height",
        "__btn_height",
        "__padding_left",
        "__padding_top",
        "__padding_bottom",
        "__indent",
        "__row_padding_bottom",
        "__bg_color",
        "__hover_color",
    )

    DEFAULT_WIDTH: float = 400.0
    DEFAULT_HEIGHT: int = 45
    DEFAULT_BTN_HEIGHT: int = 30
    DEFAULT_PADDING_LEFT: float = 5.0
    DEFAULT_PADDING_BOTTOM: float = 5.0
    DEFAULT_BG: Tuple[int, int, int, int] = (16, 16, 16, 255)
    DEFAULT_HOVER: Tuple[int, int, int, int] = (28, 28, 28, 255)

    def __init__(
        self,
        key: str,
        label: str,
        icon: str,
        callback: Optional[Callable[[int], None]] = None,
        default_key: int = dpg.mvKey_None,
        width: float = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        btn_height: int = DEFAULT_BTN_HEIGHT,
        padding_left: float = DEFAULT_PADDING_LEFT,
        padding_top: float = 0.0,
        padding_bottom: float = 0.0,
        indent: float = 0.0,
        row_padding_bottom: float = DEFAULT_PADDING_BOTTOM,
        bg_color: Tuple[int, int, int, int] = DEFAULT_BG,
        hover_color: Tuple[int, int, int, int] = DEFAULT_HOVER,
    ) -> None:
        self.__key: str = key
        self.__label: str = label
        self.__icon: str = icon
        self.__callback: Optional[Callable[[int], None]] = callback
        self.__default_key: int = default_key
        self.__width: float = width
        self.__height: int = height
        self.__btn_height: int = btn_height
        self.__padding_left: float = padding_left
        self.__padding_top: float = padding_top
        self.__padding_bottom: float = padding_bottom
        self.__indent: float = indent
        self.__row_padding_bottom: float = row_padding_bottom
        self.__bg_color: Tuple[int, int, int, int] = bg_color
        self.__hover_color: Tuple[int, int, int, int] = hover_color
        self.__tag: str = f"row_{key}"

    def build(
        self, 
        keybind_registry: Dict[str, KeybindButton], 
        transition_list: List[ColorTransition]
    ) -> None:
        """
        Constructs the row and passes configuration to the KeybindButton.
        """
        icon_tag: str = f"icon_{self.__key}"
        text_tag: str = f"label_{self.__key}"
        button_tag: str = f"btn_{self.__key}"

        with dpg.child_window(
            tag=self.__tag,
            width=self.__width,
            height=self.__height,
            border=False,
            no_scrollbar=True,
            indent=self.__padding_left,
        ):
            with dpg.group(horizontal=True):
                IconButtonComponent(
                    tag=icon_tag,
                    icon_name=self.__icon,
                    width=40,
                    height=40,
                    icon_size=22,
                    x_indent=9,
                    y_indent=9,
                    theme=themes.visuals_item,
                ).build()

                TextComponent(
                    tag=text_tag,
                    text=self.__label,
                    width=180,
                    height=40,
                    y_indent=10,
                    font=fonts.font_bold_18,
                    theme=themes.visuals_item,
                ).build()

                keybind_registry[self.__key] = KeybindButton(
                    tag=button_tag,
                    default_key=self.__default_key,
                    callback=self.__callback,
                    padding_top=self.__padding_top,
                    padding_bottom=self.__padding_bottom,
                    indent=self.__indent,
                    height=self.__btn_height,
                )
                
                with dpg.group():
                    keybind_registry[self.__key].build(width=100)

        transition_list.append(
            ColorTransition(
                target=self.__tag,
                initial=self.__bg_color,
                final=self.__hover_color,
                related_items=[icon_tag, text_tag],
            )
        )
        dpg.add_spacer(height=self.__row_padding_bottom)