from trainer.values.base_value import BaseValue


class MipbiasValue(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x0439E190

    @property
    def offsets(self) -> list[int]:
        return [0x30]

    @property
    def value_type(self) -> str:
        return "float"