from typing import Callable, Optional
import dearpygui.dearpygui as dpg
from trainer.ui.exceptions.exceptions import DPGItemNotFoundError

class ButtonHandler:
    
    """
    A stateful wrapper for `Dear PyGui` items to simulate button behavior.
    
    This class enables polling-based interaction for items like `child_window`, 
    `group`, or `image` which do not natively support the `clicked` state.
    """
    
    __slots__ = ("tag", "on_click", "on_hover", "__is_hovered")

    def __init__(
        self, 
        tag: str, 
        on_click: Optional[Callable[[str], None]] = None, 
        on_hover: Optional[Callable[[str], None]] = None
    ) -> None:
        
        """
        Initializes the interaction wrapper.

        Args:
            tag (str): The unique `Dear PyGui` identifier for the item.
            on_click (Optional[Callable[[str], None]]): Callback triggered on left-click.
            on_hover (Optional[Callable[[str], None]]): Callback triggered while hovering.
        """
        
        self.tag: str = tag
        self.on_click: Optional[Callable[[str], None]] = on_click
        self.on_hover: Optional[Callable[[str], None]] = on_hover
        self.__is_hovered: bool = False
        
        super().__init__()

    def update(self) -> None:
        
        """
        Polls the item state. Must be called within the application `tick` loop.

        Raises:
            DPGItemNotFoundError: If the `tag` does not exist in the DPG context.
        """
        
        if not dpg.does_item_exist(self.tag):
            raise DPGItemNotFoundError(f"Button tag '{self.tag}' not found.")

        currently_hovered: bool = dpg.is_item_hovered(self.tag)
        
        if currently_hovered:
            if self.on_hover:
                self.on_hover(self.tag)
            
            if dpg.is_mouse_button_clicked(0) and self.on_click:
                self.on_click(self.tag)
        
        self.__is_hovered = currently_hovered

    @property
    def is_hovered(self) -> bool:
        
        """
        Returns the current hover state of the item.
        """
        
        return self.__is_hovered