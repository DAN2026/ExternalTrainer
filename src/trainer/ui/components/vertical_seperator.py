from typing import List, Optional, Union
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.styles import themes


class VerticalSeparatorComponent(BaseComponent):
    """
    A visual component that renders a thin vertical separator line.

    This component utilizes a `drawlist` within a `child_window` to create a 
    crisp vertical line with configurable height, thickness, and color.
    """

    __slots__ = (
        "__tag",
        "__theme",
        "__pos",
        "__height",
        "__thickness",
        "__color",
    )

    def __init__(
        self,
        tag: str,
        pos: List[float],
        height: float,
        theme: Optional[Union[int, str]] = None,
        thickness: float = 1.0,
        color: List[int] = [255, 255, 255, 255],
    ) -> None:
        """
        Initializes the `VerticalSeparatorComponent`.

        Args:
            tag (str): Unique identifier for the component.
            pos (List[float]): Initial [x, y] coordinates.
            height (float): Total height of the separator line.
            theme (Optional[Union[int, str]]): Optional theme for the container.
            thickness (float): Thickness of the line. Defaults to 1.0.
            color (List[int]): RGBA color list. Defaults to White.
        """
        self.__tag: str = tag
        self.__pos: List[float] = pos
        self.__height: float = height
        self.__theme: Optional[Union[int, str]] = theme
        self.__thickness: float = thickness
        self.__color: List[int] = color

        super().__init__()

    def build(self) -> None:
        """
        Constructs the vertical line within a non-interactive `child_window`.
        """
        try:
            with dpg.child_window(
                tag=self.__tag,
                width=self.__thickness,
                height=self.__height,
                border=False,
                no_scrollbar=True,
                no_scroll_with_mouse=True,
            ) as container:
                dpg.set_item_pos(container, self.__pos)

                if self.__theme:
                    themes.apply(container, self.__theme)

                with dpg.drawlist(width=self.__thickness, height=self.__height):
                    dpg.draw_line(
                        p1=[self.__thickness / 2, 0],
                        p2=[self.__thickness / 2, self.__height],
                        color=self.__color,
                        thickness=self.__thickness,
                    )

            super().build()

        except Exception as e:
            logger.error(f"Failed to build `VerticalSeparatorComponent` [{self.__tag}]: {e}")
            raise e

    def tick(self) -> None:
        """
        Static visual component; no per-frame logic required.
        """
        pass

    def set_pos(self, pos: List[float]) -> None:
        """
        Updates the component position using `dpg.set_item_pos`.

        Args:
            pos (List[float]): The new [x, y] coordinates.
        """
        self.__pos = pos
        if dpg.does_item_exist(self.__tag):
            dpg.set_item_pos(self.__tag, pos)

    @property
    def tag(self) -> str:
        """
        Returns the unique tag identifier.
        """
        return self.__tag

    @property
    def pos(self) -> List[float]:
        """
        Returns the current position of the component.
        """
        return self.__pos