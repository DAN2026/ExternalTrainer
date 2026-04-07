from abc import ABC
from loguru import logger
from abc import ABC, abstractmethod

class BasePage(ABC):
    
    def __init__(self):
        logger.info(f"Initializing page: {self.__class__.__name__}")

    @abstractmethod    
    def build(self) -> None:
        
        logger.success(f"Built page: {self.__class__.__name__}")


    @abstractmethod
    def tick(self) -> None: pass
        

