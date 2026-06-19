from trainer.values.base_value import BaseValue


class BeerValue(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x043D7F98

    @property
    def offsets(self) -> list[int]:
        return [0x268, 0xEC0]

    @property
    def value_type(self) -> str:
        return "int"
