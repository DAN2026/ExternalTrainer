from typing import Callable, List, Tuple, Any, Dict
import dearpygui.dearpygui as dpg
from trainer.ui.components.base import BaseComponent
from trainer.ui.styles import fonts, themes, icons
from trainer.ui.animations.underline import UnderlineTransition
from trainer.ui.components.dropdown import FloatingDropdownComponent
from trainer.ui.common.math import Math


class NavbarComponent(BaseComponent):
    """
    Navigation bar with integrated hover-triggered dropdown menus and synced animations.
    """

    __slots__ = (
        "__underlines", 
        "__on_page_change", 
        "__dropdowns", 
        "__nav_tags",
        "__hover_counters"
    )

    def __init__(self, on_page_change: Callable[[str], None]) -> None:
        """
        Initializes navbar state.
        """
        self.__underlines: Dict[str, UnderlineTransition] = {}
        self.__dropdowns: Dict[str, FloatingDropdownComponent] = {}
        self.__on_page_change: Callable[[str], None] = on_page_change
        self.__nav_tags: List[str] = []
        self.__hover_counters: Dict[str, int] = {}
        super().__init__()

    def build(self) -> None:
        """
        Constructs Navbar and attaches dropdowns with proximity-aware hover logic.
        """
        dropdown_positions: List[List[float]] = [
            [22.0, 110.0],
            [120.0, 110.0],
            [217.5, 110.0],
            [317.5, 110.0],
        ]

        nav_items: List[Tuple[str, str, float, float, Callable, List[Dict[str, Any]]]] = [
            ("eye", "Visuals", 60.0, 42.5, lambda: None, [
                {"label": "INI", "callback": lambda: self.__on_page_change("visual-ini")},
                {"label": "Display", "callback": lambda: self.__on_page_change("visual-display")},
            ]),
            ("tool", "Utilities", 65.0, 40.0, lambda: None, [
                {"label": "Logging", "callback": lambda: self.__on_page_change("util-logs")},
                {"label": "Automation", "callback": lambda: self.__on_page_change("util-auto")},
                {"label": "Overlays", "callback": lambda: self.__on_page_change("util-overlays")},
            ]),
            ("stats", "Stats", 57.5, 47.5, lambda: None, [
                {"label": "Servers", "callback": lambda: self.__on_page_change("stats-servers")},
                {"label": "Sessions", "callback": lambda: self.__on_page_change("stats-sessions")},
            ]),
            ("settings", "Settings", 60.0, 32.5, lambda: None, [
                {"label": "Keybinds", "callback": lambda: self.__on_page_change("settings-keys")},
                {"label": "Configs", "callback": lambda: self.__on_page_change("settings-configs")},
            ]),
        ]

        with dpg.child_window(tag="app-navbar", width=425, height=75, border=False, indent=12.5) as navbar:
            themes.apply(navbar, themes.container)

            with dpg.group(horizontal=True, indent=15):
                for i, (label_lower, label, img_ind, txt_ind, callback, dd_items) in enumerate(nav_items):
                    group_tag: str = f"nav-group-{label_lower}"
                    self.__nav_tags.append(group_tag)
                    self.__hover_counters[group_tag] = 0

                    with dpg.group(tag=group_tag):
                        dpg.add_spacer(height=10.5)

                        img_val = Math.centre_text_indent(img_ind, label, fonts.font_bold_18)
                        dpg.add_image(icons.apply(label_lower), width=24, height=24, indent=img_val)

                        txt_val = Math.centre_text_indent(txt_ind, label, fonts.font_bold_18)
                        txt_item = dpg.add_text(label, indent=txt_val)
                        fonts.apply(txt_item, fonts.font_bold_18)

                    if dd_items:
                        dd_tag = f"dropdown_{label_lower}"
                        dropdown = FloatingDropdownComponent(
                            tag=dd_tag,
                            width=50,
                            pos=dropdown_positions[i],
                            items=dd_items,
                            theme=themes.navbar_dropdown,
                            font=fonts.font_bold_16,
                            duration=0.2,
                            bg_color=(14, 14, 14),
                        )
                        dropdown.build()
                        self.__dropdowns[group_tag] = dropdown

                    with dpg.item_handler_registry() as registry:
                        dpg.add_item_clicked_handler(callback=callback)
                        dpg.add_item_hover_handler(callback=lambda s, a, u=group_tag: self.__on_hover(u))

                    dpg.bind_item_handler_registry(group_tag, registry)

                    self.__underlines[group_tag] = UnderlineTransition(
                        target=group_tag,
                        width=90,
                        color=(1, 180, 240, 255),
                        duration=0.2,
                    )

        super().build()

    def __on_hover(self, group_tag: str) -> None:
        """
        Activates the dropdown for the hovered navbar item.
        """
        if dropdown := self.__dropdowns.get(group_tag):
            dropdown.toggle(True)

    def tick(self) -> None:
        """
        Drives animations with hysteresis and mouse-state validation.
        """
        is_mouse_down = dpg.is_mouse_button_down(0)

        for group_tag in self.__nav_tags:
            dropdown = self.__dropdowns.get(group_tag)
            underline = self.__underlines.get(group_tag)
            
            is_nav_hovered = dpg.is_item_hovered(group_tag)
            is_menu_hovered = False
            
            if dropdown:
                is_menu_hovered = dpg.is_item_hovered(dropdown.tag)

            if is_nav_hovered or is_menu_hovered or (is_mouse_down and self.__hover_counters[group_tag] > 0):
                self.__hover_counters[group_tag] = 5
            else:
                self.__hover_counters[group_tag] = max(0, self.__hover_counters[group_tag] - 1)

            is_active = self.__hover_counters[group_tag] > 0

            if dropdown:
                dropdown.toggle(is_active)
                dropdown.tick()

            if underline:
                underline.tick(active=is_active)