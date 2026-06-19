import re
from typing import Dict, List, Tuple, Callable, Union, Optional, Any
import dearpygui.dearpygui as dpg
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.components.icon_button import IconButtonComponent
from trainer.ui.animations.color import ColorTransition
from trainer.ui.styles import fonts, themes


class SearchBarComponent(BaseComponent):
    """
    Search bar component with regex support and data mapping.
    """

    __slots__ = (
        "__tag",
        "__hint",
        "__icon",
        "__data_map",
        "__callback",
        "__width",
        "__height",
        "__padding_left",
        "__padding_bottom",
        "__padding_top",
        "__bg_color",
        "__hover_color",
        "__last_query",
    )

    DEFAULT_WIDTH: float = 400.0
    DEFAULT_HEIGHT: int = 45
    DEFAULT_PADDING_LEFT: float = 5.0
    DEFAULT_PADDING_BOTTOM: float = 0.5
    DEFAULT_PADDING_TOP: float = 0.0
    DEFAULT_BG: Tuple[int, int, int, int] = (16, 16, 16, 255)
    DEFAULT_HOVER: Tuple[int, int, int, int] = (28, 28, 28, 255)

    def __init__(
        self,
        tag: str,
        hint: str,
        icon: str,
        data_map: Dict[str, str],
        width: float = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        padding_left: float = DEFAULT_PADDING_LEFT,
        padding_bottom: float = DEFAULT_PADDING_BOTTOM,
        padding_top: float = DEFAULT_PADDING_TOP,
        bg_color: Tuple[int, int, int, int] = DEFAULT_BG,
        hover_color: Tuple[int, int, int, int] = DEFAULT_HOVER,
        callback: Optional[Callable[[str, int], None]] = None,
    ) -> None:
        """
        Initializes search bar parameters.
        """
        self.__tag: str = tag
        self.__hint: str = hint
        self.__icon: str = icon
        self.__data_map: Dict[str, str] = data_map
        self.__width: float = width
        self.__height: int = height
        self.__padding_left: float = padding_left
        self.__padding_bottom: float = padding_bottom
        self.__padding_top: float = padding_top
        self.__bg_color: Tuple[int, int, int, int] = bg_color
        self.__hover_color: Tuple[int, int, int, int] = hover_color
        self.__callback: Optional[Callable[[str, int], None]] = callback
        self.__last_query: str = ""

        super().__init__()

    def build(self, transition_list: List[ColorTransition]) -> None:
        """
        Constructs the search bar UI.
        """
        icon_tag: str = f"icon_{self.__tag}"
        
        if self.__padding_top > 0:
            dpg.add_spacer(height=self.__padding_top)

        try:
            with dpg.child_window(
                tag=f"{self.__tag}_container",
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

                    dpg.add_input_text(
                        tag=self.__tag,
                        hint=self.__hint,
                        width=self.__width - 60,
                        callback=self.__on_change,
                        no_spaces=False,
                    )

                    themes.apply(self.__tag, themes.visuals_item)
                    fonts.apply(self.__tag, fonts.font_bold_18)
                    
                    dpg.set_item_pos(self.__tag, [50, 7.5])

            transition_list.append(
                ColorTransition(
                    target=f"{self.__tag}_container",
                    initial=self.__bg_color,
                    final=self.__hover_color,
                    related_items=[icon_tag, self.__tag],
                )
            )
            
            dpg.add_spacer(height=self.__padding_bottom)

            super().build()

        except Exception as e:
            logger.error(f"Failed to build SearchBarComponent [{self.__tag}]: {e}")
            raise e

    def __on_change(self, sender: str, app_data: str, *args: Any) -> None:
        """
        Handles text changes and filters mapped rows.
        """
        self.__last_query = app_data
        match_count: int = 0

        try:
            pattern = re.compile(app_data, re.IGNORECASE)

            for tag, label in self.__data_map.items():
                is_match = bool(pattern.search(label))
                row_tag = f"{tag}_row"

                if dpg.does_item_exist(row_tag):
                    dpg.configure_item(row_tag, show=is_match)
                    if is_match:
                        match_count += 1

            if self.__callback:
                self.__callback(app_data, match_count)

        except re.error:
            pass

    def tick(self) -> None:
        """
        Component update logic.
        """
        pass

    @property
    def query(self) -> str:
        """
        Returns the most recent search query.
        """
        return self.__last_query