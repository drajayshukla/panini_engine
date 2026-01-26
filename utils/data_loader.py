import json
import os


def load_all_dhatus():
    # फाइल का सही पाथ ढूँढना
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "dhatupatha.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("dhatus", [])
    except FileNotFoundError:
        return []