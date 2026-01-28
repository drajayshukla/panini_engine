# panini_engine/logic/conflict_resolver.py

class ConflictResolver:
    """
    पाणिनीय विप्रतिषेध और अपवाद इंजन।
    सिद्धांत: विप्रतिषेधे परं कार्यम् (१.४.२) और नित्य-अन्तरङ्ग-अपवाद।
    """

    @staticmethod
    def resolve_vipratishedha(sutra_a, sutra_b):
        """
        दो टकराते हुए सूत्रों के बीच वरीयता (Priority) तय करना।
        sutra_a, sutra_b: Sutra Objects (from panini_sutras_final.json)
        """
        # १. विप्रतिषेधे परं कार्यम् (१.४.२): अष्टाध्यायी क्रम में जो बाद में है, वह जीतेगा।
        # उदाहरण: यदि 1.1.1 और 1.1.2 में टकराव हो, तो 1.1.2 प्रबल होगा।

        order_a = (sutra_a['adhyaya'], sutra_a['pada'], sutra_a['order'])
        order_b = (sutra_b['adhyaya'], sutra_b['pada'], sutra_b['order'])

        if order_b > order_a:
            return sutra_b, "विप्रतिषेधे परं कार्यम् (१.४.२) के अनुसार पर-शास्त्र बलवान है।"
        else:
            return sutra_a, "विप्रतिषेधे परं कार्यम् (१.४.२) के अनुसार पूर्व-शास्त्र (यदि नियम विरुद्ध हो) या पर-शास्त्र प्रभावी।"

    @staticmethod
    def check_apavada(utsarga_sutra, apavada_sutra):
        """
        उत्सर्ग (General Rule) और अपवाद (Exception) का मिलान।
        नियम: 'निरवकाशो विधिरापवादः' - अपवाद हमेशा उत्सर्ग को रोकता है।
        """
        # यहाँ भविष्य में अपवादों की मैपिंग आएगी
        return apavada_sutra