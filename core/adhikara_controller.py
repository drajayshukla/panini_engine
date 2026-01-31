"""
FILE: core/adhikara_controller.py
PURPOSE: Manages R12 (Headers) and R31 (Nivṛtti - Deactivation).
"""

class AdhikaraController:
    # Mathematical Boundaries of Adhikaras in Ashtadhyayi
    SCOPES = {
        "ANGASYA": (6, 4, 1, 7, 4, 97),   # 6.4.1 to 7.4.97
        "BHASYA":  (6, 4, 129, 6, 4, 175) # 6.4.129 to 6.4.175
    }

    @staticmethod
    def is_rule_in_scope(rule_str, adhikara_name):
        """
        Checks if a target rule falls within the Adhikara's mathematical domain.
        rule_str format: "x.y.z" (e.g., "7.1.12")
        """
        try:
            c, p, s = map(int, rule_str.split('.'))
        except:
            return False # Non-standard rule format

        start_c, start_p, start_s, end_c, end_p, end_s = AdhikaraController.SCOPES[adhikara_name]

        # Convert to absolute integer for comparison (simple heuristic: c*10000 + p*1000 + s)
        target_val = c * 10000 + p * 1000 + s
        start_val = start_c * 10000 + start_p * 1000 + start_s
        end_val = end_c * 10000 + end_p * 1000 + end_s

        return start_val <= target_val <= end_val

    @staticmethod
    def check_nivritti(context, adhikara_name):
        """
        R31 (Nivṛtti): Checks if the Context DEACTIVATES the Adhikara.
        """
        # BHASYA Context: Needs suffix to be Y-adi or Vowel-adi (1.4.18) AND weak (non-sarvanamasthana)
        if adhikara_name == "BHASYA":
            is_yachi = context.get("is_yachi", False)
            is_bham = context.get("is_bham", False)
            if not is_bham:
                return True # NIVRITTI: Deactivate Bhasya rules!
        
        return False # Active
