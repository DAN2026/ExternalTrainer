import dearpygui.dearpygui as dpg
from typing import Dict, Any
from loguru import logger

from trainer.ui.components.keybind_button import KeybindButton
from trainer.events.signals import (
    request_save_config,
    request_load_config,
    on_save_success,
    on_save_failure,
    on_load_complete
)


class ConfigTestComponent:
    """
    Component to validate serialization logic and signal integrity.
    """

    __slots__ = (
        "__test_registry",
        "__weakref__"
    )

    def __init__(self) -> None:
        """
        Initializes the test registry and connects to global lifecycle signals.
        """
        self.__test_registry: Dict[str, KeybindButton] = {}

        # Connect listeners for feedback
        on_save_success.connect(self.__handle_save_success)
        on_save_failure.connect(self.__handle_save_failure)
        on_load_complete.connect(self.__handle_load_complete)

    def __handle_save_success(self, sender: Any, payload: Dict[str, Any]) -> None:
        """
        Signal listener for successful save events.
        """
        logger.debug(f"[TEST] Save Success! Data written: {payload}")

    def __handle_save_failure(self, sender: Any, error: Exception) -> None:
        """
        Signal listener for failed save events.
        """
        logger.error(f"[TEST] Save Failed! Error: {error}")

    def __handle_load_complete(self, sender: Any, binds: Dict[str, int]) -> None:
        """
        Signal listener for load completion.
        """
        logger.debug(f"[TEST] Load Complete! Binds retrieved: {binds}")

    def run_save_test(self) -> None:
        """
        Fires a save request signal to trigger the Serializer.
        """
        logger.info("[TEST] Requesting Save...")
        
        # Setup dummy data if registry is empty
        if not self.__test_registry:
            test_btn = KeybindButton(tag="test_btn", default_key=dpg.mvKey_X)
            self.__test_registry["aim_bot"] = test_btn

        request_save_config.send(self, registry=self.__test_registry)

    def run_load_test(self) -> None:
        """
        Fires a load request signal to trigger the Deserializer.
        """
        logger.info("[TEST] Requesting Load...")
        request_load_config.send(self)

    def build_ui(self) -> None:
        """
        Simple UI trigger to run tests manually via signals.
        """
        with dpg.window(label="Debug: Config Tester", width=300, height=200):
            dpg.add_text("Check console for Loguru output.")
            dpg.add_button(label="Trigger Save Signal", callback=self.run_save_test)
            dpg.add_button(label="Trigger Load Signal", callback=self.run_load_test)


def main() -> None:
    """
    Main entry point for the serialization test harness.
    """
    from trainer.serialisation.serializer import ConfigSerializer
    from trainer.serialisation.deserializer import ConfigDeserializer

    dpg.create_context()

    # We must instantiate these so they start listening to the signals
    _s = ConfigSerializer()
    _d = ConfigDeserializer()

    tester = ConfigTestComponent()
    tester.build_ui()

    dpg.create_viewport(title='Serialization Test Harness', width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    
    # Run initial sequence
    tester.run_save_test()
    tester.run_load_test()

    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()