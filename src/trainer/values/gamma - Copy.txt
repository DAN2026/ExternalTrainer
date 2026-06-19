from trainer.values.base_value import BaseValue


class GammaValue(BaseValue):

    @property
    def base_offset(self) -> int:
        return 0x0437FE28

    @property
    def offsets(self) -> list[int]:
        return [0x6CC]

    @property
    def value_type(self) -> str:
        return "float"