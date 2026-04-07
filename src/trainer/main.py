import dearpygui.dearpygui as dpg
from trainer.ui.app import App

def main() -> None:
    
    __app = App()
    
    __app.start()

if __name__ == "__main__":
    main()