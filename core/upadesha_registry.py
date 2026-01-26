# Path: core/upadesha_registry.py

from enum import Enum
from utils.data_loader import get_all_dhatus
class UpadeshaType(Enum):
    """
    पाणिनीय व्याकरण के ९ प्रकार के उपदेश (आद्योच्चारणम्)।
    यह Enum सुनिश्चित करता है कि इत्-संज्ञा केवल इन्हीं पर लागू हो।
    """
    DHATU = "Dhatu"          # उदा: √डुप्-पचँष् (Dhatupatha)
    SUTRA = "Sutra"          # उदा: अइउण् (Maheshwar Sutras / Ashtadhyayi)
    GANA = "Gana"            # उदा: सर्वादि (Ganapatha)
    UNADI = "Unadi"          # उदा: कृवापाजिमिस्वदिसाध्यशूभ्य उण् (Unadi Sutras)
    VAKYA = "Vartika"        # उदा: कात्यायन वार्तिक
    LINGA = "Linganusasana"  # लिंगानुशासनम्
    AGAMA = "Agama"          # उदा: नुँम्, इट् (Augments)
    PRATYAYA = "Pratyaya"    # उदा: सुँप्, तिँङ्, लँट् (Suffixes)
    ADESH = "Adesha"         # उदा: स्थानिवदादेशोऽनल्विधौ (Substitutes)

    @classmethod
    def is_upadesha(cls, value):
        return value in cls