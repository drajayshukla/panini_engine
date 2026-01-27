import csv
import json
import os


def convert_pratyahara_csv_to_json():
    # १. हार्डकोडेड पाथ (Current Folder)
    # यह उसी फोल्डर को टारगेट करेगा जहाँ आपकी स्क्रिप्ट रखी है
    current_folder = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(current_folder, 'pratyaharconverter_json.csv')
    output_json = os.path.join(current_folder, '../data/pratyahara_list.json')

    data = []

    try:
        # २. डेटा प्रोसेसिंग
        with open(input_csv, encoding='utf-8') as csvf:
            csv_reader = csv.DictReader(csvf)
            for rows in csv_reader:
                # 'varnas' कॉलम की स्ट्रिंग (अ, इ, उ) को लिस्ट में बदलना
                if 'varnas' in rows:
                    rows['varnas'] = [v.strip() for v in rows['varnas'].split(',')]
                data.append(rows)

        # ३. JSON राइटिंग
        with open(output_json, 'w', encoding='utf-8') as jsonf:
            json.dump(data, jsonf, indent=4, ensure_ascii=False)

        print(f"✅ सफलता! '{output_json}' फाइल तैयार है।")

    except FileNotFoundError:
        print(f"❌ त्रुटि: '{input_csv}' फाइल इसी फोल्डर में नहीं मिली।")
    except Exception as e:
        print(f"❌ अज्ञात त्रुटि: {str(e)}")


if __name__ == '__main__':
    convert_pratyahara_csv_to_json()