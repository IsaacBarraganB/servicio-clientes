from typing import List
class AuthConfig:
    def __init__(self) -> None:
        self.__info: List[str] = []

    def set_info(self, info: List[str]):
        self.__info = info
    
    def get_info(self) -> List[str]:
        return self.__info