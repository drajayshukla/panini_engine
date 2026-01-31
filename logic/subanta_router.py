"""
FILE: logic/subanta_router.py
"""
from logic.subanta.s_1_1 import SubantaEngine11


# from logic.subanta.s_1_2 import SubantaEngine12

class SubantaRouter:

    @staticmethod
    def route_derivation(stem_str, anga_varnas, vibhakti, vacana, logger):
        """
        Dispatches to the correct specialized engine.
        """
        # Case 1.1
        if vibhakti == "Prathama" and vacana == "Eka":
            return SubantaEngine11.derive(stem_str, anga_varnas, logger)

        # Case 1.2 (Future)
        # elif vibhakti == "Prathama" and vacana == "Dvi":
        #     return SubantaEngine12.derive(...)

        else:
            return ["Error: Engine not implemented for this case"]