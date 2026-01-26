# core/upadesha_registry.py
from enum import Enum

class UpadeshaType(Enum):
    DHATU = "Dhatu"
    SUTRA = "Sutra"
    GANA = "Gana"
    UNADI = "Unadi"
    VAKYA = "Vartika"
    LINGA = "Linganusasana"
    AGAMA = "Agama"
    PRATYAYA = "Pratyaya"
    ADESH = "Adesha"

    @classmethod
    def is_upadesha(cls, value):
        return any(value == item.value for item in cls)