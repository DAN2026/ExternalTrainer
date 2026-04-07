from typing import List, Optional, Union
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.styles import themes, fonts


class TextComponent(BaseComponent):
    """
    A customizable text component encapsulated within a `child_window`.

    Supports dynamic positioning and a configurable vertical indent to 
    manually offset the text from the top of the container.
    """

    __slots__ = (
        "__tag",
        "__text",
        "__pos",
        "__width",
        "__height",
        "__y_indent",
        "__theme",
        "__font",
        "__color",
        "__show",
    )

    def __init__(
        self,
        tag: str,
        text: str,
        pos: List[float],
        width: float,
        height: float,
        y_indent: float = 0.0,
        show: bool = True,
        theme: Optional[Union[int, str]] = None,
        font: Optional[Union[int, str]] = None,
        color: Optional[List[int]] = None,
    ) -> None:
        """
        Initializes the `TextComponent`.

        Args:
            tag (str): Unique identifier for the component.
            text (str): The string content to display.
            pos (List[float]): [x, y] coordinates for the container.
            width (float): Width of the containing child window.
            height (float): Height of the containing child window.
            y_indent (float): Vertical offset from the top of the container.
            show (bool): Initial visibility state of the component.
            theme (Optional[Union[int, str]]): Theme for the container.
            font (Optional[Union[int, str]]): Font registry for the text.
            color (Optional[List[int]]): Optional RGBA override for the text.
        """
        self.__tag: str = tag
        self.__text: str = text
        self.__pos: List[float] = pos
        self.__width: float = width
        self.__height: float = height
        self.__y_indent: float = y_indent
        self.__show: bool = show
        self.__theme: Optional[Union[int, str]] = theme
        self.__font: Optional[Union[int, str]] = font
        self.__color: Optional[List[int]] = color

        super().__init__()

    def build(self) -> None:
        """
        Constructs the text element inside a child window with a vertical offset.
        """
        try:
            with dpg.child_window(
                tag=self.__tag,
                width=self.__width,
                height=self.__height,
                border=False,
                no_scrollbar=True,
                no_scroll_with_mouse=True,
                show=self.__show,
            ) as container:
                dpg.set_item_pos(container, self.__pos)

                if self.__theme:
                    themes.apply(container, self.__theme)

                text_item = dpg.add_text(
                    default_value=self.__text,
                    tag=f"{self.__tag}_label",
                    color=self.__color if self.__color else (-1, -1, -1, -1),
                )

                dpg.set_item_pos(text_item, [0, self.__y_indent])

                if self.__font:
                    fonts.apply(text_item, self.__font)

            super().build()

        except Exception as e:
            logger.error(f"Failed to build `TextComponent` [{self.__tag}]: {e}")
            raise e

    def tick(self) -> None:
        """
        Static visual component.
        """
        pass

    def toggle(self, show: bool) -> None:
        """
        Updates the visibility of the component.

        Args:
            show (bool): The new visibility state.
        """
        self.__show = show
        if dpg.does_item_exist(self.__tag):
            dpg.configure_item(self.__tag, show=show)

    def set_pos(self, pos: List[float]) -> None:
        """
        Updates the container position.

        Args:
            pos (List[float]): The new [x, y] coordinates.
        """
        self.__pos = pos
        if dpg.does_item_exist(self.__tag):
            dpg.set_item_pos(self.__tag, pos)

    def set_y_indent(self, y_indent: float) -> None:
        """
        Updates the vertical offset of the text within the container.

        Args:
            y_indent (float): The new vertical offset.
        """
        self.__y_indent = y_indent
        label_tag = f"{self.__tag}_label"
        if dpg.does_item_exist(label_tag):
            dpg.set_item_pos(label_tag, [0, y_indent])

    def set_text(self, text: str) -> None:
        """
        Updates the internal text value.

        Args:
            text (str): The new string value to display.
        """
        self.__text = text
        label_tag = f"{self.__tag}_label"
        if dpg.does_item_exist(label_tag):
            dpg.set_value(label_tag, text)

    @property
    def tag(self) -> str:
        """
        Returns the unique tag identifier.
        """
        return self.__tag

    @property
    def pos(self) -> List[float]:
        """
        Returns the current [x, y] position.
        """
        return self.__pos