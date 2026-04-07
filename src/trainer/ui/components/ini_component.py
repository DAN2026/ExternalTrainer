from typing import List, Optional, Union, Callable
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.components.text import TextComponent
from trainer.ui.components.toggle import Toggle
from trainer.ui.styles import themes, fonts


class IniComponent(BaseComponent):
    """
    A component representing a single INI setting.
    Layout order: [Icon] -> [Text Description] -> [Toggle Switch]
    """

    __slots__ = (
        "__tag",
        "__icon_name",
        "__label",
        "__pos",
        "__width",
        "__height",
        "__on_toggle",
        "__theme",
        "__icon_btn",
        "__text_label",
        "__toggle",
        "__default_state",
    )

    def __init__(
        self,
        tag: str,
        icon_name: str,
        label: str,
        pos: List[float],
        width: float = 425.0,
        height: float = 45.0,
        default_state: bool = False,
        on_toggle: Optional[Callable[[str, bool], None]] = None,
        theme: Optional[Union[int, str]] = None,
    ) -> None:
        super().__init__()
        self.__tag: str = tag
        self.__icon_name: str = icon_name
        self.__label: str = label
        self.__pos: List[float] = pos
        self.__width: float = width
        self.__height: float = height
        self.__on_toggle: Optional[Callable[[str, bool], None]] = on_toggle
        self.__theme: Optional[Union[int, str]] = theme
        self.__default_state: bool = default_state
        
        self.__icon_btn: Optional[IconButtonComponent] = None
        self.__text_label: Optional[TextComponent] = None
        self.__toggle: Optional[Toggle] = None

    def build(self) -> None:
        try:
            with dpg.child_window(
                tag=self.__tag,
                width=self.__width,
                height=self.__height,
                pos=self.__pos,
                border=False,
                no_scrollbar=True
            ) as container:
                
                if self.__theme:
                    themes.apply(container, self.__theme)

                # 1. Icon (Far Left)
                self.__icon_btn = IconButtonComponent(
                    tag=f"{self.__tag}_icon",
                    icon_name=self.__icon_name,
                    theme=themes.container,
                    pos=[5, 5],
                    width=35,
                    height=35,
                    icon_size=20,
                    x_indent=7.5,
                    y_indent=7.5
                )
                self.__icon_btn.build()

                # 2. Text Description (Middle)
                self.__text_label = TextComponent(
                    tag=f"{self.__tag}_text",
                    text=self.__label,
                    pos=[50, 0], # Offset to the right of the icon
                    width=300,
                    height=self.__height,
                    y_indent=12.5,
                    font=fonts.font_18,
                )
                self.__text_label.build()

                # 3. Animated Toggle (Far Right)
                # Note: The callback wraps the internal state to match your (tag, val) requirement
                self.__toggle = Toggle(
                    parent=container,
                    label=self.__label,
                    default_state=self.__default_state,
                    width=44,
                    height=24,
                    callback=lambda state: self.__handle_callback(state)
                )
                self.__toggle.build()
                
                # Align toggle to the right edge
                dpg.set_item_pos(self.__toggle._Toggle__drawlist_tag, [self.__width - 55, 10])

            super().build()

        except Exception as e:
            logger.error(f"Failed to build `IniComponent` [{self.__tag}]: {e}")

    def __handle_callback(self, state: bool) -> None:
        """Ensures the external callback receives both the tag and the value."""
        if self.__on_toggle:
            self.__on_toggle(self.__tag, state)

    def tick(self) -> None:
        if self.__icon_btn:
            self.__icon_btn.tick()
        
        if self.__toggle:
            self.__toggle.tick()

    @property
    def value(self) -> bool:
        return self.__toggle.value if self.__toggle else False

    @value.setter
    def value(self, new_state: bool) -> None:
        if self.__toggle:
            self.__toggle.value = new_state