import pandas as pd
import re
import os


def correct_panini_data(input_txt, ref_csv_path, output_txt):
    """
    CSV-Exclusive Workflow for the Pāṇinian Engine.
    Implements R6 (Sthānyādeśa) substitution by mapping corrupted OCR
    to authoritative reference data.
    """
    # 1. Load the reference CSV with encoding fallbacks for Pāṇinian diacritics
    try:
        try:
            # Attempt standard UTF-8 first
            df_ref = pd.read_csv(ref_csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            # Fallback to ISO-8859-1 to handle 0xad and other non-UTF8 bytes
            df_ref = pd.read_csv(ref_csv_path, encoding='ISO-8859-1')

        print("✅ Authoritative Reference CSV loaded.")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # Clean headers to ensure R3: Saṃjñā class tagging works reliably
    df_ref.columns = df_ref.columns.str.strip()

    # Create a lookup dictionary mapping coordinate keys (e.g., '1-1-1')
    # to authoritative text
    try:
        df_ref['key'] = (df_ref['Chapter # अध्यायः'].astype(str) + "-" +
                         df_ref['Paada # पादः'].astype(str) + "-" +
                         df_ref['Sutra # सू. सं.'].astype(str))
        sutra_lookup = dict(zip(df_ref['key'], df_ref['Sutra text सूत्रम्‌']))
    except KeyError as e:
        print(f"❌ Column header mismatch: {e}")
        return

    corrected_output = []

    # 2. Process the raw text file (Atomic Tokenization context)
    if not os.path.exists(input_txt):
        print(f"❌ Source file not found: {input_txt}")
        return

    with open(input_txt, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Regex to detect the Adhyāya-Pāda-Sūtra numbering
            match = re.match(r'^(\d+-\d+-\d+)\s+(.*)', line)

            if match:
                sutra_id = match.group(1)
                if sutra_id in sutra_lookup:
                    # R6: Sthānyādeśa - Substitution of corrupted OCR with valid Lakṣaṇa
                    authoritative_text = sutra_lookup[sutra_id]
                    corrected_output.append(f"{sutra_id} {authoritative_text}")
                else:
                    # Keep original line if no match found in reference
                    corrected_output.append(line)
            else:
                # Retain non-sūtra lines (Vṛtti notes, source tags)
                corrected_output.append(line)

    # 3. Final Lakṣya-Lakṣaṇa Output
    with open(output_txt, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(corrected_output))

    print(f"🚀 Success! Corrected file saved as: {output_txt}")


# --- CONFIGURATION ---
input_file = '/Users/dr.ajayshukla/Downloads/panini sutra with vritti.txt'
reference_csv = '/Users/dr.ajayshukla/Downloads/sutras Kaumudi Krama.xlsx - Sutra sorted by Index No..csv'
output_file = '/Users/dr.ajayshukla/Downloads/corrected_panini_sutras.txt'

if __name__ == "__main__":
    correct_panini_data(input_file, reference_csv, output_file)