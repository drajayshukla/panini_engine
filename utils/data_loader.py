import json
import os
from core.upadesha_registry import UpadeshaType


def get_base_path():
    """प्रोजेक्ट के रूट डायरेक्टरी का पाथ प्राप्त करने के लिए।"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_all_dhatus():
    """
    केवल 'dhatu_master_structured.json' से डेटा लोड करता है।
    (UpadeshaType के कैश्ड लोडर का उपयोग सुनिश्चित करता है)
    """
    data = UpadeshaType._load_data('dhatu_master_structured.json')

    # यदि डेटा लिस्ट है तो सीधे भेजें, वरना 'dhatus' की खोजें
    if isinstance(data, list):
        return data
    return data.get("dhatus", [])


def get_all_vibhakti():
    """
    vibhaktipatha.json से सुँप् और तिङ् प्रत्ययों को लोड करता है।
    """
    data = UpadeshaType._load_data('vibhaktipatha.json')

    if not data or not isinstance(data, dict):
        return []

    # डेटाबेस की कीज़ (Keys) के अनुसार मिलान (sup_pratyayas और tin_pratyayas)
    sup = data.get("sup_pratyayas", [])
    tin = data.get("tin_pratyayas", [])
    extra = data.get("extra_taddhita_avyaya", [])

    return sup + tin + extra


def get_shiva_sutras():
    """माहेश्वर सूत्रों (Shiva Sutras) को लोड करता है।"""
    return UpadeshaType._load_data('shiva_sutras.json')


def get_sutra_data():
    """अष्टाध्यायी के मास्टर सूत्रों को लोड करता है।"""
    return UpadeshaType._load_data('panini_sutras_final.json')