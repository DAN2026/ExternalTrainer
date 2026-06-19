from trainer.values.base_value import BaseValue


class FovValue(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x043E1EA0

    @property
    def offsets(self) -> list[int]:
        return [0x158, 0xF0, 0xA0, 0x478, 0xAA0, 0x190, 0x158]

    @property
    def value_type(self) -> str:
        return "float"