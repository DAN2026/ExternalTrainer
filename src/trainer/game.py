from trainer.core.memory_connection import MemoryConnection
from trainer.values.fov import FovValue
from trainer.values.prevviewmode import PreviewmodeValue

class ShooterGame:
    
    def __init__(self):
        
        conn = MemoryConnection("ShooterGame.exe")

        self.fov = FovValue(conn)
        
        self.previewmode = PreviewmodeValue(conn)
