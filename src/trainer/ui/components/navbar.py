from loguru import logger
from trainer.ui.components.base import BaseComponent
import dearpygui.dearpygui as dpg
from trainer.ui.styles import fonts, themes, icons
from trainer.ui.animations.animations import UnderlineTransition
from trainer.ui.common.math import Math

class NavbarComponent(BaseComponent):

    def __init__(self, on_page_change):
        self.__underlines: list[UnderlineTransition] = []
        
        self.__on_page_change = on_page_change
        
        super().__init__()

    def _on_nav_clicked(self, sender, app_data, user_data):
        if user_data == "Visuals":
            self.show_visuals()
        elif user_data == "Logs":
            self.show_logs()
        elif user_data == "Debug":
            self.show_debug()
        elif user_data == "Settings":
            self.show_settings()

    def show_visuals(self, *args, **kwargs):
        
        self.__on_page_change("visual-container")
        
    def show_logs(self, *args, **kwargs):
        
        self.__on_page_change("logs-container")
        
    def show_debug(self, *args, **kwargs):
        
        self.__on_page_change("debug-container")
        
    def show_settings(self, *args, **kwargs):
        
        self.__on_page_change("settings-container")
        
    def build(self):
        nav_items = [
            ("eye", "Visuals", 60, 42.5, self.show_visuals),
            ("logs", "Logs", 65, 60, self.show_logs),
            ("bug", "Debug", 60, 42.5, self.show_debug),
            ("settings", "Settings", 60, 32.5, self.show_settings)
        ]

        with dpg.child_window(tag="app-navbar", width=425, height=100, border=False, indent=12.5) as navbar:
            themes.apply(navbar, themes.container)

            with dpg.group(horizontal=True, indent=15):
                for index, (icon, label, img_indent, text_indent, target_callback) in enumerate(nav_items, start=1):
                    group_tag = f"nav-visuals-{index}"

                    with dpg.group(tag=group_tag):
                        dpg.add_spacer(height=25)
                        
                        img_ind_val = Math.centre_text_indent(img_indent, label, fonts.font_bold_18)
                        dpg.add_image(icons.apply(icon), width=24, height=24, indent=img_ind_val)
                        
                        text_ind_val = Math.centre_text_indent(text_indent, label, fonts.font_bold_18)
                        text = dpg.add_text(label, indent=text_ind_val)
                        fonts.apply(text, fonts.font_bold_18)

                    with dpg.item_handler_registry() as registry:
                        dpg.add_item_clicked_handler(callback=target_callback)
                    
                    dpg.bind_item_handler_registry(group_tag, registry)

                    self.__underlines.append(
                        UnderlineTransition(
                            target=group_tag,
                            width=90, 
                            color=(0, 180, 255, 255),
                            duration=0.2,
                        )
                    )

        super().build()

    def tick(self) -> None:
        for u in self.__underlines:
            u.tick()