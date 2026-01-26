import json
import os

def get_base_path():
    """प्रोजेक्ट के रूट डायरेक्टरी का पाथ प्राप्त करने के लिए।"""
    # यह utils/ से एक लेवल ऊपर (root) जाएगा
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_all_dhatus():
    """dhatupatha.json से धातुओं की सूची लोड करता है।"""
    file_path = os.path.join(get_base_path(), "data", "dhatupatha.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("dhatus", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_all_vibhakti():
    """vibhaktipatha.json से सुँप् और तिङ् प्रत्ययों को लोड करता है।"""
    file_path = os.path.join(get_base_path(), "data", "vibhaktipatha.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # सुँप् और तिङ् दोनों को एक लिस्ट में जोड़कर वापस भेजें
            return data.get("sup_pratyaya", []) + data.get("tin_pratyaya", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []