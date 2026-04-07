from typing import Callable, Optional, List, Union
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.handlers.button import ButtonHandler
from trainer.ui.styles import themes, icons
from trainer.ui.exceptions.exceptions import DPGItemNotFoundError


class IconButtonComponent(BaseComponent):
    """
    A specialized `BaseComponent` that renders an interactive icon using a `child_window`.

    This component allows for independent configuration of the container dimensions,
    internal icon size, and manual offsets (x/y indents) for precise alignment.
    """

    __slots__ = (
        "__tag",
        "__icon_name",
        "__theme",
        "__pos",
        "__width",
        "__height",
        "__x_indent",
        "__y_indent",
        "__icon_size",
        "__on_click",
        "__handler",
        "__show",
    )

    def __init__(
        self,
        tag: str,
        icon_name: str,
        theme: Union[int, str],
        pos: List[float],
        width: float = 55.0,
        height: float = 55.0,
        x_indent: float = 0.0,
        y_indent: float = 0.0,
        icon_size: Optional[float] = None,
        show: bool = True,
        on_click: Optional[Callable[[str], None]] = None,
    ) -> None:
        """
        Initializes the icon button component.

        Args:
            tag (str): Unique identifier for the component.
            icon_name (str): Key for the icon texture.
            theme (Union[int, str]): Theme to apply to the container.
            pos (List[float]): [x, y] coordinates.
            width (float): Width of the child window container.
            height (float): Height of the child window container.
            x_indent (float): Horizontal offset for the icon within the container.
            y_indent (float): Vertical offset for the icon within the container.
            icon_size (Optional[float]): Size of the icon. Defaults to min(width, height).
            show (bool): Initial visibility state.
            on_click (Optional[Callable]): Callback triggered on click.
        """
        self.__tag: str = tag
        self.__icon_name: str = icon_name
        self.__theme: Union[int, str] = theme
        self.__pos: List[float] = pos
        self.__width: float = width
        self.__height: float = height
        self.__x_indent: float = x_indent
        self.__y_indent: float = y_indent
        self.__icon_size: float = icon_size if icon_size else min(width, height)
        self.__show: bool = show
        self.__on_click: Optional[Callable[[str], None]] = on_click
        self.__handler: Optional[ButtonHandler] = None

        super().__init__()

    def build(self) -> None:
        """
        Builds the UI with configurable container dimensions and icon offsets.
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
                themes.apply(container, self.__theme)

                icon_item = dpg.add_image(
                    icons.apply(self.__icon_name),
                    width=self.__icon_size,
                    height=self.__icon_size,
                )
                
                dpg.set_item_pos(icon_item, [self.__x_indent, self.__y_indent])

            self.__handler = ButtonHandler(
                tag=self.__tag,
                on_click=self.__on_click
            )

            super().build()

        except Exception as e:
            logger.error(f"Failed to build `IconButtonComponent` [{self.__tag}]: {e}")
            raise e

    def tick(self) -> None:
        """
        Processes interaction polling if the component is visible.
        """
        if not self.__show:
            return

        if self.__handler:
            try:
                self.__handler.update()
            except DPGItemNotFoundError as e:
                logger.warning(f"Interaction update failed for `{self.__tag}`: {e}")
                raise e

    def toggle(self, show: bool) -> None:
        """
        Updates the visibility state of the component.
        """
        self.__show = show
        if dpg.does_item_exist(self.__tag):
            dpg.configure_item(self.__tag, show=show)

    def set_pos(self, pos: List[float]) -> None:
        """
        Updates the component position.
        """
        self.__pos = pos
        if dpg.does_item_exist(self.__tag):
            dpg.set_item_pos(self.__tag, pos)

    @property
    def tag(self) -> str:
        """Returns the unique tag identifier."""
        return self.__tag

    @property
    def is_visible(self) -> bool:
        """Returns the current visibility state."""
        return self.__show