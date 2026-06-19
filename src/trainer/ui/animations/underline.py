import time
import dearpygui.dearpygui as dpg
from typing import Union, Tuple
from trainer.ui.animations.lerp import lerp


class UnderlineTransition:
    """
    Manages the drawing and animation of a centered underline.
    """

    __slots__ = (
        "__target",
        "__width",
        "__color",
        "__duration",
        "__t",
        "__last",
        "__drawlist",
        "__line",
    )

    def __init__(
        self,
        target: Union[str, int],
        width: float,
        color: Tuple[int, int, int, int],
        duration: float = 0.2,
    ) -> None:
        """
        Initializes the underline state and DPG drawing items.
        """
        self.__target: Union[str, int] = target
        self.__width: float = width
        self.__color: Tuple[int, int, int, int] = color
        self.__duration: float = duration
        self.__t: float = 0.0
        self.__last: float = time.time()

        self.__drawlist: Union[str, int] = dpg.add_drawlist(
            width=width, height=4, parent=target
        )
        self.__line: Union[str, int] = dpg.draw_line(
            p1=(0, 0),
            p2=(0, 0),
            color=color,
            thickness=2,
            parent=self.__drawlist,
        )

    def tick(self, active: bool) -> None:
        """
        Updates the progress based on an external active state and redraws.
        """
        now: float = time.time()
        delta: float = now - self.__last
        self.__last = now

        direction: int = 1 if active else -1

        if (direction == 1 and self.__t >= 1.0) or (direction == -1 and self.__t <= 0.0):
            return

        self.__t = max(0.0, min(1.0, self.__t + direction * (delta / self.__duration)))

        centre: float = self.__width / 2
        half: float = lerp(0, self.__width / 2, self.__t)

        dpg.configure_item(
            self.__line,
            p1=(centre - half, 0),
            p2=(centre + half, 0),
        )