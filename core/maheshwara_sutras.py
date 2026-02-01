"""
FILE: core/maheshwara_sutras.py
"""
class MaheshwaraSutras:
    # Defined as (Content, IT_Marker_String)
    # This avoids ambiguity with slicing and halants.
    SUTRAS_DATA = [
        ("अइउ", "ण्"),        # 1. N1
        ("ऋऌ", "क्"),         # 2
        ("एओ", "ङ्"),         # 3
        ("ऐऔ", "च्"),         # 4. AC stops here
        ("हयवर", "ट्"),       # 5. AT stops here
        ("ल", "ण्"),          # 6. N2 (IN stops here usually)
        ("ञमङणन", "म्"),      # 7
        ("झभ", "ञ्"),         # 8
        ("घढध", "ष्"),        # 9
        ("जबगडद", "श्"),      # 10
        ("खफछठथचटत", "व्"),   # 11
        ("कप", "य्"),         # 12
        ("शषस", "र्"),        # 13
        ("ह", "ल्")           # 14
    ]
    
    SAVARNA_MAP = {
        'अ': ['अ', 'आ'], 'इ': ['इ', 'ई'], 'उ': ['उ', 'ऊ'], 'ऋ': ['ऋ', 'ॠ'], 'ऌ': ['ऌ']
    }

    @staticmethod
    def get_pratyahara(p_name, force_n2=False):
        """
        p_name: e.g., "अच्", "अट्", "इण्"
        """
        if not p_name or len(p_name) < 2: return set()
        
        p_name = p_name.strip()
        adi = p_name[0]
        # The IT marker is the rest of the string (e.g., 'च्' or 'ण्')
        # This captures the consonant AND the virama.
        it = p_name[1:] 
        
        chars = set()
        collecting = False
        n_count = 0
        
        for content, marker in MaheshwaraSutras.SUTRAS_DATA:
            # Check content
            for char in content:
                if char == adi:
                    collecting = True
                
                if collecting:
                    chars.add(char)
                    if char in MaheshwaraSutras.SAVARNA_MAP:
                        chars.update(MaheshwaraSutras.SAVARNA_MAP[char])
            
            # Check Stop
            if collecting and marker == it:
                # Handle ambiguity of 'N' (Nna) which appears in Sutra 1 and 6.
                if it == 'ण्':
                    n_count += 1
                    # If force_n2 is True, we skip the first N (Sutra 1)
                    if force_n2 and n_count == 1:
                        continue
                
                break
        
        return chars
