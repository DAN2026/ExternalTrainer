import dearpygui.dearpygui as dpg
from typing import Optional, List, Dict, Any, Tuple, ClassVar
from trainer.ui.components.base import BaseComponent
from trainer.ui.animations.fade import FadeTransition


class FloatingDropdownComponent(BaseComponent):
    """
    Dropdown component with independent item hover text and fade transitions.
    """

    DEFAULT_BG: ClassVar[Tuple[int, int, int]] = (30, 30, 30)
    DEFAULT_FG: ClassVar[Tuple[int, int, int]] = (230, 230, 230)

    __slots__ = (
        "__tag",
        "__width",
        "__height",
        "__pos",
        "__items",
        "__is_active",
        "__transition",
        "__duration",
        "__bg_color",
        "__fg_color",
        "__font",
        "__base_theme",
    )

    def __init__(
        self,
        tag: str,
        width: float = 50.0,
        pos: List[float] = None,
        items: List[Dict[str, Any]] = None,
        theme: Optional[int] = None,
        font: Optional[int] = None,
        duration: float = 0.2,
        bg_color: Optional[Tuple[int, int, int]] = None,
        fg_color: Optional[Tuple[int, int, int]] = None,
        height: float = 50.0,
    ) -> None:
        """
        Initializes the dropdown component with configurable dimensions.
        """
        self.__tag: str = tag
        self.__width: float = width
        self.__height: float = height
        self.__pos: List[float] = pos or [0.0, 0.0]
        self.__items: List[Dict[str, Any]] = items or []
        self.__font: Optional[int] = font
        self.__base_theme: Optional[int] = theme
        self.__duration: float = duration
        self.__bg_color: Tuple[int, int, int] = bg_color or self.DEFAULT_BG
        self.__fg_color: Tuple[int, int, int] = fg_color or self.DEFAULT_FG
        self.__is_active: bool = False
        self.__transition: Optional[FadeTransition] = None
        super().__init__()

    def build(self) -> None:
        """
        Constructs the UI and registers per-item hover handlers.
        """
        with dpg.window(
            tag=self.__tag,
            pos=self.__pos,
            width=int(self.__width),
            height=int(self.__height),
            no_title_bar=True,
            no_move=True,
            no_resize=True,
            no_scrollbar=True,
            show=False,
        ):
            for i, item in enumerate(self.__items):
                item_tag: str = f"{self.__tag}_item_{i}"
                dpg.add_button(
                    tag=item_tag,
                    label=item.get("label", "Unknown"),
                    width=-1,
                    callback=item.get("callback"),
                )
                if self.__font:
                    dpg.bind_item_font(item_tag, self.__font)

        self.__transition = FadeTransition(
            target=self.__tag,
            bg_rgb=self.__bg_color,
            fg_rgb=self.__fg_color,
            duration=self.__duration,
            base_theme=self.__base_theme
        )

        for i in range(len(self.__items)):
            self.__transition.add_hover_handler(f"{self.__tag}_item_{i}")

        super().build()

    def toggle(self, show: bool) -> None:
        """
        Updates internal visibility state.
        """
        self.__is_active = show
        if show:
            dpg.show_item(self.__tag)
            dpg.focus_item(self.__tag)

    def tick(self) -> None:
        """
        Drives the transition animation and hides window upon completion.
        """
        if not dpg.does_item_exist(self.__tag):
            return

        if self.__transition:
            self.__transition.tick(active=self.__is_active)
            if not self.__is_active and self.__transition.progress <= 0.0:
                dpg.hide_item(self.__tag)

    @property
    def tag(self) -> str:
        """
        Returns the DPG tag for the dropdown window.
        """
        return self.__tag