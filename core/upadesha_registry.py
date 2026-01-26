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
        अतिरिक्त स्पेस को हटाकर (strip) मिलान किया जाता है।
        """
        # डेटा नॉर्मलाइजेशन: इनपुट के आसपास के स्पेस हटाना
        cleaned_text = text.strip() if text else ""

        if upadesha_type == UpadeshaType.DHATU:
            return cleaned_text in get_all_dhatus()

        elif upadesha_type == UpadeshaType.PRATYAYA:
            return cleaned_text in get_all_vibhakti()

        # अन्य श्रेणियों के लिए फिलहाल True (जब तक डेटाबेस न जुड़ें)
        return True

    @staticmethod
    def auto_detect(text):
        """
        बिना यूजर से पूछे, डेटाबेस के आधार पर उपदेश के प्रकार का पता लगाना।
        यह अतिरिक्त स्पेस को स्वतः हटाकर (strip) सर्च करता है।
        """
        if not text:
            return None

        cleaned_text = text.strip()

        # 1. पहले धातुओं (Dhatu) में खोजें
        if cleaned_text in get_all_dhatus():
            return UpadeshaType.DHATU

        # 2. फिर प्रत्ययों/विभक्तियों (Pratyaya) में खोजें
        if cleaned_text in get_all_vibhakti():
            return UpadeshaType.PRATYAYA

        # 3. अगर कहीं न मिले, तो None (अर्थात् कस्टम इनपुट)
        return None