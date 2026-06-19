from trainer.values.base_value import BaseValue


class ViewDistanceValue(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x043D89C0

    @property
    def offsets(self) -> list[int]:
        return [0x438, 0xF8, 0x120, 0x50, 0x1DC]

    @property
    def value_type(self) -> str:
        return "float"