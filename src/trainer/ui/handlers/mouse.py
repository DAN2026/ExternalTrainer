import dearpygui.dearpygui as dpg
from typing import List, ClassVar, Union, Any
from trainer.ui.handlers.base import BaseHandler


class MouseHandler(BaseHandler):
    """
    MouseHandler manages global viewport interaction, specifically handling
    window dragging while respecting an exclusion list of UI tags.

    Uses internal DPG mapping to resolve integer IDs back to string aliases
    for consistent filtering.
    """

    __EXCLUSIONS: ClassVar[List[str]] = [
        "visual-container",
        "visual-display",
        "visual-ini",
        "settings-keys",
    ]

    __slots__ = ()

    def __init__(self) -> None:
        """
        Initializes the mouse handler.
        """
        super().__init__()

    def register(self) -> None:
        """
        Registers the mouse drag handler within the global DPG handler registry.
        """
        with dpg.handler_registry(tag="viewport_move_handler"):
            dpg.add_mouse_drag_handler(
                button=dpg.mvMouseButton_Left,
                callback=self._static_drag_viewport,
            )

    @staticmethod
    def _static_drag_viewport(sender: Union[int, str], app_data: Any) -> None:
        """
        Calculates and updates viewport position based on mouse delta.

        Resolves the active window's integer ID to its string tag (alias)
        to check against the exclusion list.
        """
        active_window: Union[int, str] = dpg.get_active_window()

        if not active_window:
            return

        tag: str = dpg.get_item_alias(active_window)
        
        if tag in MouseHandler.__EXCLUSIONS:
            return

        if app_data and len(app_data) >= 3:
            dx: float = app_data[1]
            dy: float = app_data[2]

            if dx != 0 or dy != 0:
                pos: List[int] = dpg.get_viewport_pos()
                dpg.set_viewport_pos([pos[0] + int(dx), pos[1] + int(dy)])