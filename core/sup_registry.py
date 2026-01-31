"""
FILE: core/sup_registry.py
TIMESTAMP: 2026-01-30 20:25:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: The 21 Suffixes
"""


class SupRegistry:
    """
    [SUTRA]: ४.१.२ स्वौजसमौट्छष्टाभ्याम्भिस्ङेभ्याम्भ्यस्ङसिभ्याम्भ्यस्ङसोसाम्ङ्योस्सुप्।
    Defines the 21 Sup Pratyayas organized by Vibhakti (Case) and Vacana (Number).
    """

    # Table: (Vibhakti, Vacana) -> (Raw Suffix, Tags)
    SUP_TABLE = {
        # Prathama (Nominative)
        (1, 1): ("सुँ", {"su", "sup", "vibhakti", "svadi", "prathama"}),
        (1, 2): ("औ", {"sup", "vibhakti", "svadi", "prathama"}),
        (1, 3): ("जस्", {"jas", "sup", "vibhakti", "svadi", "prathama"}),

        # Dvitiya (Accusative)
        (2, 1): ("अम्", {"am", "sup", "vibhakti", "svadi", "dvitiya"}),
        (2, 2): ("औट्", {"aut", "sup", "vibhakti", "svadi", "dvitiya"}),
        (2, 3): ("शस्", {"shas", "sup", "vibhakti", "svadi", "dvitiya"}),

        # Tritiya (Instrumental)
        (3, 1): ("टा", {"ta", "sup", "vibhakti", "svadi", "tritiya"}),
        (3, 2): ("भ्याम्", {"bhyam", "sup", "vibhakti", "svadi", "tritiya"}),
        (3, 3): ("भिस्", {"bhis", "sup", "vibhakti", "svadi", "tritiya"}),

        # Chaturthi (Dative)
        (4, 1): ("ङे", {"nge", "sup", "vibhakti", "svadi", "chaturthi"}),
        (4, 2): ("भ्याम्", {"bhyam", "sup", "vibhakti", "svadi", "chaturthi"}),
        (4, 3): ("भ्यस्", {"bhyas", "sup", "vibhakti", "svadi", "chaturthi"}),

        # Panchami (Ablative)
        (5, 1): ("ङसिँ", {"ngasi", "sup", "vibhakti", "svadi", "panchami"}),
        (5, 2): ("भ्याम्", {"bhyam", "sup", "vibhakti", "svadi", "panchami"}),
        (5, 3): ("भ्यस्", {"bhyas", "sup", "vibhakti", "svadi", "panchami"}),

        # Shashthi (Genitive)
        (6, 1): ("ङस्", {"ngas", "sup", "vibhakti", "svadi", "shashthi"}),
        (6, 2): ("ओस्", {"os", "sup", "vibhakti", "svadi", "shashthi"}),
        (6, 3): ("आम्", {"am", "sup", "vibhakti", "svadi", "shashthi"}),

        # Saptami (Locative)
        (7, 1): ("ङि", {"ngi", "sup", "vibhakti", "svadi", "saptami"}),
        (7, 2): ("ओस्", {"os", "sup", "vibhakti", "svadi", "saptami"}),
        (7, 3): ("सुप्", {"sup", "vibhakti", "svadi", "saptami"}),
    }

    @staticmethod
    def get_suffix(vibhakti, vacana):
        """
        Returns the raw suffix string and its tag set for a given Case and Number.
        """
        return SupRegistry.SUP_TABLE.get((vibhakti, vacana))