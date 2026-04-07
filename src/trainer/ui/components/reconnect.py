from typing import Callable, Optional, List, Union
import math
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.handlers.button import ButtonHandler
from trainer.ui.styles import themes
from trainer.ui.animations.animations import RotationTransition


class ReconnectButtonComponent(BaseComponent):
    """
    A specialized `BaseComponent` that renders a vector-based reconnect spinner.

    The component supports visibility toggling to enable/disable interaction
    based on application state.
    """

    __slots__ = (
        "__tag",
        "__theme",
        "__pos",
        "__width",
        "__height",
        "__indent",
        "__on_click",
        "__handler",
        "__transition",
        "__show",
    )

    def __init__(
        self,
        tag: str,
        theme: Union[int, str],
        pos: List[float],
        width: float = 30.0,
        height: float = 30.0,
        indent: float = 0.0,
        show: bool = True,
        on_click: Optional[Callable[[str], None]] = None,
    ) -> None:
        """
        Initializes the `ReconnectButtonComponent`.
        """
        self.__tag: str = tag
        self.__theme: Union[int, str] = theme
        self.__pos: List[float] = pos
        self.__width: float = width
        self.__height: float = height
        self.__indent: float = indent
        self.__show: bool = show
        self.__on_click: Optional[Callable[[str], None]] = on_click

        self.__handler: Optional[ButtonHandler] = None
        self.__transition: Optional[RotationTransition] = None

        super().__init__()

    def build(self) -> None:
        """
        Constructs the UI with visibility controlled by the `show` property.
        """
        try:
            with dpg.child_window(
                tag=self.__tag,
                width=self.__width,
                height=self.__height,
                indent=self.__indent,
                border=False,
                no_scrollbar=True,
                no_scroll_with_mouse=True,
                show=self.__show,
            ) as container:
                dpg.set_item_pos(container, self.__pos)
                themes.apply(container, self.__theme)

                center_x: float = self.__width / 2
                center_y: float = self.__height / 2
                radius: float = min(self.__width, self.__height) * 0.25

                points: List[List[float]] = []
                for i in range(22):
                    angle: float = (i / 25) * (math.pi * 2)
                    points.append(
                        [
                            center_x + radius * math.cos(angle),
                            center_y + radius * math.sin(angle),
                        ]
                    )

                with dpg.drawlist(width=self.__width, height=self.__height):
                    with dpg.draw_node(tag=f"{self.__tag}_node"):
                        dpg.draw_polyline(
                            points,
                            tag=f"{self.__tag}_path",
                            color=(0, 200, 255, 255),
                            thickness=2.0,
                        )

            self.__transition = RotationTransition(
                target=f"{self.__tag}_node",
                center=[center_x, center_y],
                duration=0.5
            )

            self.__handler = ButtonHandler(
                tag=self.__tag,
                on_click=self.__internal_callback
            )

            super().build()

        except Exception as e:
            logger.error(f"Failed to build `ReconnectButtonComponent` [{self.__tag}]: {e}")
            raise e

    def __internal_callback(self, tag: str) -> None:
        """
        Triggers animation and user callback.
        """
        if self.__transition:
            self.__transition.trigger()

        if self.__on_click:
            self.__on_click(tag)

    def tick(self) -> None:
        """
        Processes polling and animation frames only if the component is visible.
        """
        if not self.__show:
            return

        if self.__handler:
            self.__handler.update()

        if self.__transition and dpg.does_item_exist(self.__transition.target):
            self.__transition.tick()

    def toggle(self, show: bool) -> None:
        """
        Toggles the visibility of the component.

        Args:
            show (bool): Whether to show or hide the component.
        """
        self.__show = show
        if dpg.does_item_exist(self.__tag):
            dpg.configure_item(self.__tag, show=show)

    def set_pos(self, pos: List[float]) -> None:
        """
        Updates the item position.
        """
        self.__pos = pos
        if dpg.does_item_exist(self.__tag):
            dpg.set_item_pos(self.__tag, pos)

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def is_visible(self) -> bool:
        return self.__show