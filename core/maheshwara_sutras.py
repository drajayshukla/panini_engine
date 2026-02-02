"""
FILE: core/maheshwara_sutras.py
"""
class MaheshwaraSutras:
    SUTRAS_DATA = [
        ("अइउ", "ण्"), ("ऋऌ", "क्"), ("एओ", "ङ्"), ("ऐऔ", "च्"),
        ("हयवर", "ट्"), ("ल", "ण्"), ("ञमङणन", "म्"), ("झभ", "ञ्"),
        ("घढध", "ष्"), ("जबगडद", "श्"), ("खफछठथचटत", "व्"), ("कप", "य्"),
        ("शषस", "र्"), ("ह", "ल्")
    ]
    
    SAVARNA_MAP = {'अ': ['अ', 'आ'], 'इ': ['इ', 'ई'], 'उ': ['उ', 'ऊ'], 'ऋ': ['ऋ', 'ॠ'], 'ऌ': ['ऌ']}

    @staticmethod
    def get_pratyahara(p_name, force_n2=False):
        """
        Implementation of:
        1. [1.3.3 हलन्त्यम्]: Identifying the It-marker.
        2. [1.1.71 आदिरन्त्येन सहेता]: Adi + Antya-It defines the group.
        """
        if not p_name or len(p_name) < 2: return set()
        
        p_name = p_name.strip()
        adi = p_name[0]
        it_marker = p_name[1:] 
        
        chars = set()
        collecting = False
        n_count = 0
        
        for content, marker in MaheshwaraSutras.SUTRAS_DATA:
            # Step 1: Scan for Adi
            for char in content:
                if char == adi: collecting = True
                if collecting:
                    chars.add(char)
                    # [1.1.69 अणुदित् सवर्णस्य]: Include savarnas
                    if char in MaheshwaraSutras.SAVARNA_MAP:
                        chars.update(MaheshwaraSutras.SAVARNA_MAP[char])
            
            # Step 2: [1.3.3 & 1.1.71]: Stop if the 'It' marker matches
            if collecting and marker == it_marker:
                if it_marker == 'ण्':
                    n_count += 1
                    if force_n2 and n_count == 1: continue
                break
        return chars
