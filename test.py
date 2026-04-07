import dearpygui.dearpygui as dpg
from trainer.ui.animations.animations import RotationTransition

def run_test():
    dpg.create_context()
    dpg.create_viewport(title="Animation Test", width=300, height=300)

    with dpg.window(label="Test Bench", width=300, height=300):
        dpg.add_text("Click the triangle to spin it")
        
        # 1. Create a drawlist and a node for the 'icon'
        with dpg.drawlist(width=100, height=100):
            with dpg.draw_node(tag="test_icon_node"):
                dpg.draw_triangle(
                    (50, 20), (20, 80), (80, 80), 
                    color=(0, 200, 255, 255), 
                    fill=(0, 200, 255, 50)
                )

        # 2. Initialize the transition (Center of 100x100 is 50,50)
        spinner = RotationTransition("test_icon_node", center=[50, 50], duration=0.6)
        
        # 3. Add a trigger button
        dpg.add_spacer(height=10)
        dpg.add_button(label="Trigger Spin", callback=spinner.trigger, width=100)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Main Loop
    while dpg.is_dearpygui_running():
        # Update the animation state every frame
        spinner.tick()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    run_test()