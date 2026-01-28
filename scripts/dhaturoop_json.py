import json
import os

def refine_dhatupath(input_file, output_file):
    """
    धातु-रूप डेटा को ३x३ मैट्रिक्स (पुरुष x वचन) में बदलना।
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} नहीं मिली।")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    refined_data = {}

    # पाणिनीय ग्रिड के मानक नाम
    vachanas = ["ekavachana", "dvivachana", "bahuvachana"]
    purushas = ["prathama", "madhyama", "uttama"]

    for index, lakaras in raw_data.items():
        refined_data[index] = {}

        for lakara_key, forms_str in lakaras.items():
            # ';' के आधार पर ९ खानों को अलग करना
            # उदाहरण: "भवति;भवतः;भवन्ति..."
            forms_list = [f.strip() for f in forms_str.split(';')]

            # यदि ९ रूप मौजूद हैं, तो उन्हें ३x३ मैट्रिक्स में मैप करें
            if len(forms_list) == 9:
                matrix = {}
                for i, p in enumerate(purushas):
                    matrix[p] = {}
                    for j, v in enumerate(vachanas):
                        # फ्लैट लिस्ट को पुरुष-वचन मैट्रिक्स में डालना
                        # यदि एक खाने में विकल्प हों (जैसे: 'अभवत्,अभवद्'), वे स्ट्रिंग के रूप में सुरक्षित रहेंगे
                        matrix[p][v] = forms_list[i * 3 + j]
                refined_data[index][lakara_key] = matrix
            else:
                # यदि ९ से कम या ज्यादा हों, तो उन्हें लिस्ट के रूप में ही रखें
                refined_data[index][lakara_key] = forms_list

    # नया रिफाइंड JSON सेव करना (active_voice.json)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(refined_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Refinement Complete: {output_file} तैयार है।")

# रन करने के लिए (पाथ को सरल बनाया गया है)
refine_dhatupath('dhatupath_best7.json', '../data/active_voice.json')