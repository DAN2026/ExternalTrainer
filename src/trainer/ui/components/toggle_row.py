from typing import Dict, List, Tuple, Callable, Union, Optional
import dearpygui.dearpygui as dpg
from trainer.ui.components.toggle import Toggle
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.animations.color import ColorTransition
from trainer.ui.styles import fonts, themes


class ToggleRowComponent:
    """
    ToggleRowComponent encapsulates a standardized UI row with default 
    visual styles matching the VisualsPage specifications.
    """

    __slots__ = (
        "__tag",
        "__key",
        "__label",
        "__icon",
        "__callback",
        "__on_true",
        "__on_false",
        "__default_state",
        "__width",
        "__height",
        "__padding_left",
        "__padding_bottom",
        "__bg_color",
        "__hover_color",
    )

    DEFAULT_WIDTH: float = 400.0
    DEFAULT_HEIGHT: int = 45
    DEFAULT_PADDING_LEFT: float = 5.0
    DEFAULT_PADDING_BOTTOM: float = 0.5
    DEFAULT_BG: Tuple[int, int, int, int] = (16, 16, 16, 255)
    DEFAULT_HOVER: Tuple[int, int, int, int] = (28, 28, 28, 255)

    def __init__(
        self,
        key: str,
        label: str,
        icon: str,
        callback: Optional[Callable[[bool], None]] = None,
        on_true: Optional[Callable[[], None]] = None,
        on_false: Optional[Callable[[], None]] = None,
        default_state: bool = False,
        width: float = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        padding_left: float = DEFAULT_PADDING_LEFT,
        padding_bottom: float = DEFAULT_PADDING_BOTTOM,
        bg_color: Tuple[int, int, int, int] = DEFAULT_BG,
        hover_color: Tuple[int, int, int, int] = DEFAULT_HOVER,
    ) -> None:
        """
        Initializes the toggle row with style defaults and dual-state callbacks.
        """
        self.__key: str = key
        self.__label: str = label
        self.__icon: str = icon
        self.__callback: Optional[Callable[[bool], None]] = callback
        self.__on_true: Optional[Callable[[], None]] = on_true
        self.__on_false: Optional[Callable[[], None]] = on_false
        self.__default_state: bool = default_state
        self.__width: float = width
        self.__height: int = height
        self.__padding_left: float = padding_left
        self.__padding_bottom: float = padding_bottom
        self.__bg_color: Tuple[int, int, int, int] = bg_color
        self.__hover_color: Tuple[int, int, int, int] = hover_color
        self.__tag: str = f"row_{key}"

    def build(
        self, 
        toggle_registry: Dict[str, Toggle], 
        transition_list: List[ColorTransition]
    ) -> None:
        """
        Constructs the row and registers it for state tracking and animations.
        """
        icon_tag: str = f"icon_{self.__key}"
        text_tag: str = f"label_{self.__key}"

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
                    width=600,
                    height=40,
                    y_indent=10,
                    font=fonts.font_bold_18,
                    theme=themes.visuals_item,
                ).build()

                toggle_registry[self.__key] = Toggle(
                    parent=dpg.last_container(),
                    label=f"##toggle_{self.__key}",
                    default_state=self.__default_state,
                    width=44,
                    height=24,
                    pos=[270, 5.5],
                    callback=self.__callback,
                    on_true=self.__on_true,
                    on_false=self.__on_false,
                )
                toggle_registry[self.__key].build()

        transition_list.append(
            ColorTransition(
                target=self.__tag,
                initial=self.__bg_color,
                final=self.__hover_color,
                related_items=[icon_tag, text_tag],
            )
        )
        dpg.add_spacer(height=self.__padding_bottom)