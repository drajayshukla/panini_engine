# core/upadesha_registry.py
from enum import Enum
from utils.data_loader import get_all_dhatus, get_all_vibhakti


class UpadeshaType(Enum):
    """
    पाणिनीय व्याकरण के उपदेशों की श्रेणियाँ और उनके डेटाबेस से संबंध।
    """
    DHATU = "Dhatu"  # संबंधित: dhatupatha.json
    SUTRA = "Sutra"
    GANA = "Gana"
    UNADI = "Unadi"
    VAKYA = "Vartika"
    LINGA = "Linganusasana"
    AGAMA = "Agama"
    PRATYAYA = "Pratyaya"  # संबंधित: vibhaktipatha.json
    ADESH = "Adesha"

    @classmethod
    def is_upadesha(cls, value):
        return any(value == item.value for item in cls)

    @staticmethod
    def validate_input(text, upadesha_type):
        """
        चेक करता है कि इनपुट टेक्स्ट संबंधित JSON डेटाबेस में मौजूद है या नहीं।
        """
        if upadesha_type == UpadeshaType.DHATU:
            return text in get_all_dhatus()

        elif upadesha_type == UpadeshaType.PRATYAYA:
            return text in get_all_vibhakti()

        # अन्य श्रेणियों के लिए फिलहाल True
        return True

    @staticmethod
    def auto_detect(text):
        """
        बिना यूजर से पूछे, डेटाबेस के आधार पर उपदेश के प्रकार का पता लगाना।
        """
        # 1. पहले धातुओं (Dhatu) में खोजें
        if text in get_all_dhatus():
            return UpadeshaType.DHATU

        # 2. फिर प्रत्ययों/विभक्तियों (Pratyaya) में खोजें
        if text in get_all_vibhakti():
            return UpadeshaType.PRATYAYA

        # 3. अगर कहीं न मिले, तो None (यानी कस्टम इनपुट)
        return None