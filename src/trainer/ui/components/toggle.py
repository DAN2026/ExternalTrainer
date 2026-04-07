from typing import Callable, Optional, List, Tuple, Any
import dearpygui.dearpygui as dpg
import time
from loguru import logger

from trainer.ui.components.base import BaseComponent
from trainer.ui.common.math import Math

class Toggle(BaseComponent):
    """
    A custom animated toggle switch component using `Dear PyGui` drawing primitives.
    
    This component manages a boolean state with a smooth linear interpolation (LERP)
    animation between 'On' and 'Off' visual states.
    """
    __slots__ = (
        "__parent", "__label", "__is_enabled", "__animation_progress", 
        "__animation_duration", "__last_frame_time", "__on_change_callback", 
        "__width", "__height", "__knob_start_x", "__knob_end_x", 
        "__knob_radius", "__drawlist_tag", "__track_tag", "__knob_tag", 
        "__handler_registry"
    )

    __TRACK_OFF_COLOR: Tuple[int, int, int, int] = (60, 60, 60, 255)
    __TRACK_ON_COLOR: Tuple[int, int, int, int] = (0, 149, 255, 255)
    __KNOB_COLOR: Tuple[int, int, int, int] = (255, 255, 255, 255)

    def __init__(
        self,
        parent: str | int,
        label: str = "",
        default_state: bool = False,
        animation_duration: float = 0.15,
        callback: Optional[Callable[[bool], None]] = None,
        width: int = 44,
        height: int = 24,
    ) -> None:
        """
        Initializes the toggle component and calculates spatial boundaries.

        Args:
            parent (str | int): The DPG container identifier.
            label (str): A unique string used for identification in logs.
            default_state (bool): The initial boolean value of the toggle.
            animation_duration (float): Seconds taken to complete the transition.
            callback (Optional[Callable]): Executed when the state toggles.
            width (int): Total pixel width of the toggle track.
            height (int): Total pixel height of the toggle track.
        """
        super().__init__()
        
        self.__parent: str | int = parent
        self.__label: str = label
        self.__is_enabled: bool = default_state
        self.__animation_progress: float = 1.0 if default_state else 0.0
        self.__animation_duration: float = animation_duration
        self.__last_frame_time: float = time.time()
        self.__on_change_callback: Optional[Callable[[bool], None]] = callback
        self.__width: int = width
        self.__height: int = height

        padding: int = 3
        self.__knob_start_x: float = float(padding)
        self.__knob_end_x: float = float(width - height + padding)
        self.__knob_radius: float = (height / 2.0) - padding

    def build(self) -> None:
        
        """
        Constructs the visual primitives and binds interaction handlers.
        """
        
        with dpg.group(horizontal=True, parent=self.__parent):
            self.__drawlist_tag = dpg.add_drawlist(width=self.__width, height=self.__height)

            self.__track_tag = dpg.draw_rectangle(
                pmin=(0, 0),
                pmax=(self.__width, self.__height),
                color=(0, 0, 0, 0),
                fill=self.__TRACK_ON_COLOR if self.__is_enabled else self.__TRACK_OFF_COLOR,
                rounding=self.__height / 2.0,
                parent=self.__drawlist_tag,
            )

            initial_knob_x: float = (
                self.__knob_end_x if self.__is_enabled else self.__knob_start_x
            ) + self.__knob_radius

            self.__knob_tag = dpg.draw_circle(
                center=(initial_knob_x, self.__height / 2.0),
                radius=self.__knob_radius,
                color=(0, 0, 0, 0),
                fill=self.__KNOB_COLOR,
                parent=self.__drawlist_tag,
            )

        self.__handler_registry = dpg.add_item_handler_registry()
        dpg.add_item_clicked_handler(
            parent=self.__handler_registry, 
            callback=self.__handle_interaction
        )
        dpg.bind_item_handler_registry(self.__drawlist_tag, self.__handler_registry)

        super().build()

    def __handle_interaction(self, *args: Any) -> None:
        
        """
        Internal logic to flip state and trigger external callbacks.
        """
        
        self.value = not self.__is_enabled
        logger.debug(f"Toggle `{self.__label}` switched to: {self.__is_enabled}")
        
        if self.__on_change_callback:
            self.__on_change_callback(self.__is_enabled)

    def tick(self) -> None:
        """
        Calculates delta time and updates LERP values for the visual transition.
        """
        current_time: float = time.time()
        delta_time: float = current_time - self.__last_frame_time
        self.__last_frame_time = current_time

        target_progress: float = 1.0 if self.__is_enabled else 0.0
        
        if abs(self.__animation_progress - target_progress) > 0.001:
            step_direction: int = 1 if self.__animation_progress < target_progress else -1
            self.__animation_progress += step_direction * (delta_time / self.__animation_duration)
            self.__animation_progress = max(0.0, min(1.0, self.__animation_progress))

            current_track_color = Math.lerp_color(
                self.__TRACK_OFF_COLOR, 
                self.__TRACK_ON_COLOR, 
                self.__animation_progress
            )
            dpg.configure_item(self.__track_tag, fill=current_track_color)

            current_knob_x = Math.lerp(
                self.__knob_start_x + self.__knob_radius, 
                self.__knob_end_x + self.__knob_radius, 
                self.__animation_progress
            )
            dpg.configure_item(self.__knob_tag, center=(current_knob_x, self.__height / 2.0))

    @property
    def value(self) -> bool:
        """
        Returns the current boolean state of the toggle.
        """
        return self.__is_enabled

    @value.setter
    def value(self, new_state: bool) -> None:
        """
        Updates the toggle state and prepares the animation for the next tick.
        """
        if self.__is_enabled != new_state:
            self.__is_enabled = new_state