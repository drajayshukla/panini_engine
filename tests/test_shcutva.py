"""
FILE: tests/test_shcutva.py
PURPOSE: Verify 8.4.40 Stoḥ Ścunā Ścuḥ and 8.4.44 Śāt
"""
import unittest
from logic.sandhi_processor import SandhiProcessor
from core.core_foundation import ad, sanskrit_varna_samyoga

class TestShcutva(unittest.TestCase):
    def run_scutva(self, t1, t2):
        l, r = SandhiProcessor.apply_shcutva(ad(t1), ad(t2))
        return sanskrit_varna_samyoga(l + r)

    def test_s_to_sh(self):
        # रामस् + शेते -> रामश्शेते
        self.assertEqual(self.run_scutva("रामस्", "शेते"), "रामश्शेते")

    def test_s_to_ch_varga(self):
        # रामस् + चिनोति -> रामश्चिनोति
        self.assertEqual(self.run_scutva("रामस्", "चिनोति"), "रामश्चिनोति")

    def test_t_varga_to_c_varga(self):
        # सत् + चित् -> सच्चित् (Assuming direct contact t+c)
        self.assertEqual(self.run_scutva("सत्", "चित्"), "सच्चित्")
        # शार्ङ्गिन् + जय -> शार्ङ्गिञ्जय (n -> ñ)
        self.assertEqual(self.run_scutva("शार्ङ्गिन्", "जय"), "शार्ङ्गिञ्जय")

    def test_right_side_change(self):
        # यज् + न -> यज्ञ (j + n -> j + ñ)
        self.assertEqual(self.run_scutva("यज्", "न"), "यज्ञ")
        
        # याच् + ना -> याच्ञा (c + n -> c + ñ)
        self.assertEqual(self.run_scutva("याच्", "ना"), "याच्ञा")

    def test_shaat_exception(self):
        # 8.4.44: ś + t-varga -> No Change
        # प्रश् + न -> प्रश्न (Not Praśña)
        self.assertEqual(self.run_scutva("प्रश्", "न"), "प्रश्न")
        
        # विश् + न -> विश्न
        self.assertEqual(self.run_scutva("विश्", "न"), "विश्न")
