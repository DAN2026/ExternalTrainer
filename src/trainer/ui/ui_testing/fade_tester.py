import dearpygui.dearpygui as dpg
from typing import Any


class FadeTester:
    """
    Utility tool for verifying FadeTransition logic and visibility toggles.
    """

    __slots__ = ("__dropdown", "__state")

    def __init__(self, dropdown_instance: Any) -> None:
        """
        Initializes the tester. 
        Note: state defaults to True to match your manual toggle(True) call.
        """
        self.__dropdown: Any = dropdown_instance
        self.__state: bool = True

    def __callback(self) -> None:
        """
        Inverts the toggle state and triggers the dropdown transition.
        """
        self.__state = not self.__state
        self.__dropdown.toggle(self.__state)

    def build(self) -> None:
        """
        Creates a dedicated controller window for animation testing.
        """
        with dpg.window(
            label="Fade Controller",
            width=200,
            height=100,
            pos=[200, 100],
            no_collapse=True,
            no_resize=True
        ):
            dpg.add_text("Animation Testing")
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            dpg.add_button(
                label="Toggle Dropdown",
                callback=self.__callback,
                width=-1,
                height=35
            )