from core.upadesha_registry import UpadeshaType


class PratipadikaEngine:
    """
    सूत्र: अर्थवदधातुरप्रत्ययः प्रातिपदिकम् (१.२.४५)
    सूत्र: कृत्तद्धितसमासाश्च (१.२.४६)
    उद्देश्य: सुबन्त-प्रक्रिया (noun derivation) के लिए आधार की पहचान करना।
    """

    @staticmethod
    def identify_base(text):
        """
        Determines if the entry is a Pratipadika (Base).
        It checks if the input is a Dhatu or Pratyaya first.
        """
        # Step 1: Check against known Dhatus and Pratyayas via Auto-detection
        detected_type, is_taddhita = UpadeshaType.auto_detect(text)

        if detected_type is not None:
            # १.२.४५ के अनुसार: अधातुः अप्रत्ययः (Must not be a Dhatu or Pratyaya)
            # अपवाद: १.२.४६ के अनुसार तद्धित/कृदन्त प्रत्यय युक्त शब्द प्रातिपदिक हो सकते हैं।
            if is_taddhita:
                return {
                    "is_pratipadika": True,
                    "text": text,
                    "sutra_applied": "१.२.४६ (कृत्तद्धितसमासाश्च)",
                    "description": f"चूंकि '{text}' एक तद्धित प्रत्यय युक्त रूप है, इसकी प्रातिपदिक संज्ञा होती है।",
                    "link": "https://ashtadhyayi.com/sutraani/1/2/46"
                }

            return {
                "is_pratipadika": False,
                "detected_as": detected_type.value,
                "reason": f"यह एक {detected_type.value} के रूप में पहचाना गया है, अतः १.२.४५ से वर्जित है।",
                "sutra": None
            }

        # Step 2: 1.2.45 Logic - Meaningful base that is NOT a Dhatu or Pratyaya
        return {
            "is_pratipadika": True,
            "text": text,
            "sutra_applied": "१.२.४५ (अर्थवदधातुरप्रत्ययः प्रातिपदिकम्)",
            "description": f"चूंकि '{text}' न धातु है न प्रत्यय, और अर्थवान है, इसकी प्रातिपदिक संज्ञा होती है।",
            "link": "https://ashtadhyayi.com/sutraani/1/2/45"
        }

    @staticmethod
    def get_sup_vibhakti_map():
        """
        सूत्र: स्वौजसमौट्... (४.१.२)
        २१ सुप्-प्रत्ययों का पदानुक्रमित मानचित्र.
        """
        return {
            "प्रथमा": {"एकवचन": "सुँ", "द्विवचन": "औ", "बहुवचन": "जस्"},
            "द्वितीया": {"एकवचन": "अम्", "द्विवचन": "औट्", "बहुवचन": "शस्"},
            "तृतीया": {"एकवचन": "टा", "द्विवचन": "भ्याम्", "बहुवचन": "भिस्"},
            "चतुर्थी": {"एकवचन": "ङे", "द्विवचन": "भ्याम्", "बहुवचन": "भ्यस्"},
            "पञ्चमी": {"एकवचन": "ङसिँ", "द्विवचन": "भ्याम्", "बहुवचन": "भ्यस्"},
            "षष्ठी": {"एकवचन": "ङस्", "द्विवचन": "ओस्", "बहुवचन": "आम्"},
            "सप्तमी": {"एकवचन": "ङि", "द्विवचन": "ओस्", "बहुवचन": "सुप्"}
        }