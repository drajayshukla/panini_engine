import json
import os


def convert_digits(text):
    """देवनागरी अंकों को मानक अंकों में बदलता है।"""
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    mapping = str.maketrans('0123456789', '0123456789')
    return text.translate(mapping).strip()


def safe_int(value):
    """खाली या अमान्य वैल्यू होने पर क्रैश होने से बचाता है।"""
    clean_val = convert_digits(value)
    if not clean_val:  # यदि स्ट्रिंग खाली है
        return 0
    try:
        return int(clean_val)
    except ValueError:
        return 0


def upgrade_dhatu_master():
    input_file = "../data/dhatu_master_structured.json"
    output_file = "dhatu_master_v2.json"

    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' नहीं मिली।")
        return

    print("Diagnostic: डेटा की 'Surgical Cleaning' शुरू हो रही है...")

    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Surgery Failed: JSON फाइल खराब है। {e}")
            return

    upgraded_data = []

    for entry in data:
        new_entry = {}
        for key, value in entry.items():
            # 1. kaumudi_index (Safety Check के साथ)
            if key == 'kaumudi_index':
                new_entry[key] = safe_int(value)

            # 2. identifier (Formatting सुरक्षित रखते हुए)
            elif key == 'identifier':
                new_entry[key] = convert_digits(value) if value else ""

            # 3. tags (TypeError से बचाव)
            elif key == 'tags' and isinstance(value, list):
                new_entry[key] = [t.strip() for t in value if isinstance(t, str)]

            # 4. अन्य सभी स्ट्रिंग्स
            elif isinstance(value, str):
                new_entry[key] = value.strip()

            else:
                new_entry[key] = value

        upgraded_data.append(new_entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(upgraded_data, f, indent=4, ensure_ascii=False)

    print(f"Success: {len(upgraded_data)} धातुओं का डेटा 'Standardized' हो गया है।")
    print(f"नई फाइल: '{output_file}'")


if __name__ == "__main__":
    upgrade_dhatu_master()