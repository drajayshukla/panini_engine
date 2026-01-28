# core/pratyahara_engine.py
# panini_engine/core/pratyahara_engine.py

class PratyaharaGenerator:
    """
    सूत्र: आदिरन्त्येन सहेता (१.१.७१)
    लॉजिक: आदि वर्ण से लेकर अन्त्य इत् वर्ण तक के वर्ण, इत् वर्णों को छोड़कर।
    """

    @staticmethod
    def generate(adi, antya_it, shiva_sutras):
        """
        adi: प्रत्याहार का पहला वर्ण (उदा. 'अ')
        antya_it: प्रत्याहार का अंतिम इत् वर्ण (उदा. 'ण्')
        shiva_sutras: डेटाबेस से माहेश्वर सूत्रों की लिस्ट
        """
        pratyahara_list = []
        found_adi = False

        for sutra in shiva_sutras:
            current_varnas = sutra['varnas']  # सूत्र के मुख्य वर्ण (अ, इ, उ)
            current_it = sutra['it_varna']  # सूत्र का इत् वर्ण (ण्)

            # १. आदि वर्ण खोजना और वर्णों को इकट्ठा करना
            for v in current_varnas:
                if v == adi:
                    found_adi = True

                if found_adi:
                    pratyahara_list.append(v)

            # २. सीमा परीक्षण (Boundary Check)
            # यदि वर्तमान सूत्र का इत् वर्ण ही हमारा 'antya_it' है, तो प्रक्रिया पूर्ण।
            # ध्यान दें: हम current_it को लिस्ट में append नहीं कर रहे हैं।
            if found_adi and current_it == antya_it:
                return pratyahara_list

        # यदि पूरा लूप खत्म हो जाए और आदि न मिले
        return pratyahara_list if found_adi else []