from trainer.values.base_value import BaseValue


class PrevviewmodeValue(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x0437FE28

    @property
    def offsets(self) -> list[int]:
        return [0x970, 0x58, 0x88]

    @property
    def value_type(self) -> str:
        return "int"