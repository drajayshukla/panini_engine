"""
utils/sanskrit_utils.py
यह मॉड्यूल अब core/phonology.py के 'Gold Standard' फंक्शन का उपयोग करता है।
"""

# core/phonology से 'Perfect Logic' का आयात
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga

# अब इस फाइल को इम्पोर्ट करने वाले अन्य मॉड्यूल्स (जैसे analyzer.py) 
# बिना किसी बदलाव के काम करते रहेंगे।