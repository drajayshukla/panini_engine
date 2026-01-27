# core/pratyahara_engine.py

class PratyaharaGenerator:
    """
    सूत्र: आदिरन्त्येन सहेता (SK2 / 1.1.71)
    लॉजिक: आदि वर्ण से लेकर अन्त्य इत् वर्ण तक के सभी वर्णों को एकत्रित करना।
    """

    @staticmethod
    def generate(adi, antya_it, shiva_sutras):
        pratyahara_list = []
        found_adi = False

        for sutra in shiva_sutras:
            # माहेश्वर सूत्र के वर्णों में आदि वर्ण को खोजना
            current_varnas = sutra['varnas']
            current_it = sutra['it_varna']

            for v in current_varnas:
                if v == adi:
                    found_adi = True

                if found_adi:
                    pratyahara_list.append(v)

            # यदि इसी सूत्र का इत् वर्ण हमारा 'antya_it' है, तो रुकना
            if found_adi and current_it == antya_it:
                return pratyahara_list

        return pratyahara_list  # प्रत्याहार तैयार!