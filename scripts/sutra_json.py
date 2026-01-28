import json
import re


def parse_panini_text(file_path):
    sutras = []

    # फाइल को ओपन करें (utf-8 एन्कोडिंग के साथ)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Regex to capture: सूत्र संख्या (1.1.1), कौमुदी संख्या (16), और सूत्र का नाम (वृद्धिरादैच्)
        # पैटर्न: संख्या.संख्या.संख्या [स्पेस] कौमुदी-संख्या [स्पेस] सूत्र_नाम
        match = re.match(r'(\d+\.\d+\.\d+)\s+कौमुदी-(\d+)(.*)', line)

        if match:
            sutra_num = match.group(1)
            kaumudi_num = match.group(2)
            sutra_name = match.group(3).strip()

            sutra_obj = {
                "sutra_num": sutra_num,
                "kaumudi_num": kaumudi_num,
                "name": sutra_name,
                "adhyaya": int(sutra_num.split('.')[0]),
                "pada": int(sutra_num.split('.')[1]),
                "order": int(sutra_num.split('.')[2]),
                "type": "Sanjna" if "संज्ञा" in sutra_name or sutra_num.startswith("1.1") else "Vidhi"
                # प्राथमिक वर्गीकरण
            }
            sutras.append(sutra_obj)
        elif line.startswith('•'):
            # यह वार्त्तिक या विशेष टिप्पणी है, इसे पिछले सूत्र के साथ जोड़ें
            if sutras:
                if "vartikas" not in sutras[-1]:
                    sutras[-1]["vartikas"] = []
                sutras[-1]["vartikas"].append(line.replace('•', '').strip())

    return sutras
#__init__.py

# फाइल को प्रोसेस करें
file_input = '08_Kala_Lab.txt'
sutra_data = parse_panini_text(file_input)

# JSON में सेव करें
with open('panini_sutras.json', 'w', encoding='utf-8') as f:
    json.dump(sutra_data, f, ensure_ascii=False, indent=4)

print(f"Success! {len(sutra_data)} sutras have been structured into panini_sutras.json")