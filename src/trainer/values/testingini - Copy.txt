from trainer.values.base_value import BaseValue


class TestingtINI(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x043D54B0

    @property
    def offsets(self) -> list[int]:
        return [0x10, 0x18, 0x0, 0x18, 0x8, 0x30, 0x8C]

    @property
    def value_type(self) -> str:
        return "int"
