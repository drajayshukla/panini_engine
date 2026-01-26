import json
import re
import os


def parse_paninian_description(desc):
    """
    Regex और बेहतर स्प्लिट लॉजिक के माध्यम से डेटा को शुद्ध करना।
    """
    data = {
        "kaumudi_index": "",
        "mula_dhatu": "",
        "upadesha": "",
        "artha_sanskrit": "",
        "gana": "अनिर्धारित",
        "pada": "अनिर्धारित",
        "it_type": "",
        "karmaka": "",
        "tags": []
    }

    # 1. कौमुदी इंडेक्स निकालना
    k_match = re.search(r'कौमुदीधातुः-(\d+)', desc)
    if k_match:
        data["kaumudi_index"] = k_match.group(1)

    # 2. धातुओं को अलग करना (Commas के आधार पर)
    # चुरादि धातुओं में parts[1] में ही मूल और उपदेश दोनों हो सकते हैं
    parts = [p.strip() for p in desc.split(',')]

    if len(parts) >= 3:
        # 'पिञ्ज् पिजिँ हिंसाबलादान...' वाले हिस्से को स्पेस से तोड़ना
        raw_dhatu_info = parts[1].split(' ')
        data["mula_dhatu"] = raw_dhatu_info[0]

        # उपदेश रूप की पहचान (अक्सर दूसरा शब्द होता है)
        if len(raw_dhatu_info) > 1:
            data["upadesha"] = raw_dhatu_info[1]
        else:
            # अगर उपदेश अलग नहीं है, तो तीसरे पार्ट से लें (भ्वादि गण की तरह)
            sub_parts = parts[2].split(' ', 1)
            data["upadesha"] = sub_parts[0]
            if len(sub_parts) > 1:
                data["artha_sanskrit"] = sub_parts[1]

        # यदि artha_sanskrit अभी भी खाली है और चुरादि गण है
        if not data["artha_sanskrit"] and len(raw_dhatu_info) > 2:
            data["artha_sanskrit"] = " ".join(raw_dhatu_info[2:])

    # 3. गण, पद, इत्-प्रकार की पहचान (सटीक मिलान)
    ganas = ["भ्वादि", "अदादि", "जुहोत्यादि", "दिवादि", "स्वादि", "तुदादि", "रुधादि", "तन्वादि", "क्र्यादि", "चुरादि"]
    for g in ganas:
        if g in desc:
            data["gana"] = g
            break

    # पद पहचान
    if "परस्मैपदी" in desc:
        data["pada"] = "परस्मैपदी"
    elif "आत्मनेपदी" in desc:
        data["pada"] = "आत्मनेपदी"
    elif "उभयपदी" in desc:
        data["pada"] = "उभयपदी"

    # सेट्/अनिट्
    if "सेट्" in desc:
        data["it_type"] = "सेट्"
    elif "अनिट्" in desc:
        data["it_type"] = "अनिट्"

    # सकर्मक/अकर्मक
    if "सकर्मक" in desc:
        data["karmaka"] = "सकर्मक"
    elif "अकर्मक" in desc:
        data["karmaka"] = "अकर्मक"

    # 4. इत्-संज्ञा टैग्स (Logic based on upadesha)
    u = data["upadesha"]
    if 'ँ' in u: data["tags"].append("{अदित्}")
    if 'िँ' in u: data["tags"].append("{इदित्}")
    if 'ृँ' in u: data["tags"].append("{ऋदित्}")
    if 'ॡँ' in u: data["tags"].append("{ॡदित्}")

    return data


def main():
    input_file = '/Users/dr.ajayshukla/Downloads/panini_function copy/dhatu_gan.json'
    output_file = '/Users/dr.ajayshukla/Downloads/panini_function copy/dhatu_master_structured.json'

    if not os.path.exists(input_file):
        print(f"❌ फाइल नहीं मिली: {input_file}")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        structured_list = []
        for entry in old_data:
            parsed = parse_paninian_description(entry.get("description", ""))
            parsed["identifier"] = entry.get("identifier", "")
            structured_list.append(parsed)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structured_list, f, ensure_ascii=False, indent=4)

        print(f"✅ रूपांतरण पूर्ण! {len(structured_list)} धातुएं प्रोसेस हुईं।")
        print(f"📂 फाइल यहाँ है: {output_file}")

    except Exception as e:
        print(f"❌ एरर: {e}")


if __name__ == "__main__":
    main()