import json
import os


def clean_sanskrit_database(input_filename, output_filename):
    # १. फाइल लोड करना
    if not os.path.exists(input_filename):
        print(f"❌ त्रुटि: {input_filename} नहीं मिली।")
        return

    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"🔄 कुल {len(data)} प्रविष्टियों का विश्लेषण शुरू...")

    # २. रिडंडेंट फील्ड्स को हटाना (Diagnostic Cleaning)
    cleaned_count = 0
    for entry in data:
        # इन हेडिंग्स को हटाना जो हम कोड में खुद जनरेट कर सकते हैं
        keys_to_remove = ["separated_forms", "suffix_only"]

        for key in keys_to_remove:
            if key in entry:
                del entry[key]
                cleaned_count += 1

    # ३. 'Lean' JSON फाइल को सेव करना
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ सफलता! क्लीन फाइल '{output_filename}' तैयार है।")
    print(f"🗑️ कुल {cleaned_count} रिडंडेंट फील्ड्स हटाए गए।")


if __name__ == "__main__":
    # आपकी फाइल का नाम यहाँ लिखें
    input_file = "filtered_data.json"
    output_file = "shbadroop.json"

    clean_sanskrit_database(input_file, output_file)