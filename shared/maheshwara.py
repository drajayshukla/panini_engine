
class MaheshwaraSutras:
    SUTRAS = [("अइउ", "ण्"), ("ऋऌ", "क्"), ("एओ", "ङ्"), ("ऐऔ", "च्"), ("हयवर", "ट्"), ("ल", "ण्"), ("ञमङणन", "म्"), ("झभ", "ञ्"), ("घढध", "ष्"), ("जबगडद", "श्"), ("खफछठथचटत", "व्"), ("कप", "य्"), ("शषस", "र्"), ("ह", "ल्")]
    SAVARNA = {'अ': ['अ', 'आ', 'अँ', 'आँ'], 'इ': ['इ', 'ई', 'इँ', 'ईँ'], 'उ': ['उ', 'ऊ', 'उँ', 'ऊँ'], 'ऋ': ['ऋ', 'ॠ']}
    @staticmethod
    def get(pratyahara):
        if not pratyahara: return set()
        adi, it = pratyahara[0], pratyahara[-1]
        chars, collecting = set(), False
        for content, marker in MaheshwaraSutras.SUTRAS:
            for c in content:
                if c == adi: collecting = True
                if collecting:
                    chars.add(c)
                    chars.update(MaheshwaraSutras.SAVARNA.get(c, []))
            if collecting and marker == it: break
        return chars
