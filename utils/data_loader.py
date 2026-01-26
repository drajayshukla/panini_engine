# utils/data_loader.py
import json
import os


def get_all_dhatus():
    """
    data/dhatupatha.json से धातुओं की सूची लोड करता है।
    """
    # फाइल का सही पाथ सुनिश्चित करना
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(os.path.dirname(current_dir), "data", "dhatupatha.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("dhatus", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def get_all_vibhakti():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "vibhaktipatha.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["sup_pratyaya"] + data["tin_pratyaya"]
    except:
        return []