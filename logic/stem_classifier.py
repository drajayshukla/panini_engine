# logic/stem_classifier.py

# logic/stem_classifier.py

def apply_6_4_3_nami_check(varna_list, nimitta_text):
    """
    Sutra: नामि (६.४.३)
    Condition: If the suffix following the Aṅga is 'नाम' (Aam + Nut).
    Action: Triggers Dīrgha (Lengthening) of the Aṅga-Antya (final vowel).
    """
    if nimitta_text == "नाम्":
        # Find the last vowel of the anga and lengthen it
        for i in range(len(varna_list) - 1, -1, -1):
            v = varna_list[i]
            if v.is_vowel:
                v.sanjnas.add("दीर्घ")
                v.trace.append("६.४.३ (नामि) के द्वारा अङ्ग-दीर्घ संज्ञा")
                break
    return varna_list


def apply_6_4_8_sarvanamasthane(varna_list, is_sarvanamasthana):
    """
    Sutra: सर्वनामस्थाने चासम्बुद्धौ (६.४.८)
    Condition: Suffix is a Sarvanamasthana (Si, Au, Jas, Am, Aut) and not Sambuddhi.
    Action: Penultimate (Upadha) vowel becomes Dirgha.
    """
    if not is_sarvanamasthana:
        return varna_list

    # Find Upadha (Penultimate) - 1.1.65 logic
    # In 'Rajan', the 'a' before 'n'
    for i in range(len(varna_list) - 2, -1, -1):
        v = varna_list[i]
        if v.is_vowel:
            v.sanjnas.add("दीर्घ")
            v.trace.append("६.४.८ (सर्वनामस्थाने...) के द्वारा उपधा-दीर्घ")
            break
    return varna_list


def apply_6_4_11_aptunvrich(varna_list, word_type):
    """
    Sutra: अप्तृन्वृच्स्वसृनप्तृनेष्टृत्वष्टृक्षत्तृहोतृपोतृप्रशास्तृणाम् (६.४.११)
    Condition: Targets specific nouns like Swasṛ, Naptṛ, etc.
    Action: Upadha Dīrgha in Sarvanamasthana.
    """
    # targets list based on sutra
    targets = ["स्वसृ", "नप्तृ", "नेष्टृ", "त्वष्टृ", "क्षत्तृ", "होतृ", "पोतृ", "प्रशास्तृ"]

    if any(t in "".join([v.char for v in varna_list]) for t in targets):
        for v in varna_list:
            if v.char == 'ऋ':
                v.char = 'ॠ'  # Operation
                v.sanjnas.add("दीर्घ")
                v.trace.append("६.४.११ के द्वारा ऋकार का दीर्घ (ॠ)")
    return varna_list