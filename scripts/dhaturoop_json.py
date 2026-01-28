import json
from collections import OrderedDict


def refine_active_voice_db(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # १. पाणिनीय लकार क्रम (Standard Order Mapping)
    lakara_order = {
        "plat": 1, "alat": 2,  # लट्
        "plit": 3, "alit": 4,  # लिट्
        "plut": 5, "alut": 6,  # लुट्
        "plrut": 7, "alrut": 8,  # लृट्
        "plot": 9, "alot": 10,  # लोट्
        "plang": 11, "alang": 12,  # लङ्
        "pvidhiling": 13, "avidhiling": 14,  # विधिलिङ्
        "pashirling": 15, "aashirling": 16,  # आशीर्लिङ्
        "plung": 17, "alung": 18,  # लुङ्
        "plrung": 19, "alrung": 20  # लृङ्
    }

    refined_db = {}

    for dhatu_id, lakaras in data.items():
        # २. लकारों को क्रमबद्ध करना (Sorting Lakaras)
        sorted_lakaras = sorted(
            lakaras.items(),
            key=lambda x: lakara_order.get(x[0], 99)
        )

        # ३. पुरुष और वचन का क्रम भी सुनिश्चित करना (OrderedDict)
        ordered_lakaras = OrderedDict()
        for lakara_name, grid in sorted_lakaras:
            ordered_grid = OrderedDict()
            for purusha in ["prathama", "madhyama", "uttama"]:
                if purusha in grid:
                    ordered_grid[purusha] = OrderedDict(
                        (v, grid[purusha][v]) for v in ["ekavachana", "dvivachana", "bahuvachana"] if v in grid[purusha]
                    )
            ordered_lakaras[lakara_name] = ordered_grid

        refined_db[dhatu_id] = ordered_lakaras

    # ४. सुरक्षित रूप से फाइल सेव करना
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(refined_db, f, ensure_ascii=False, indent=4)

    return "✅ Database Examination & Refinement Successful!"

# निष्पादन
status = refine_active_voice_db('active_voice.json', 'active_voice_refined.json')
print(status)