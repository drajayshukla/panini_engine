# utils/data_loader.py
import json
import os


def get_all_dhatus():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "dhatupatha.json")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # सभी श्रेणियों की धातुओं को एक लिस्ट में जोड़ें
            return [dhatu for sublist in data.values() for dhatu in sublist]
    return []
