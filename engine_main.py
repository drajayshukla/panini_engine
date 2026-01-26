from core.phonology import sanskrit_varna_vichhed
from core.it_sanjna_engine import apply_halantyam

# सही टेस्ट: ल्युट् प्रत्यय
input_word = "ल्युट्"
tokens = sanskrit_varna_vichhed(input_word)

print(f"१. सही विच्छेद: {tokens}")
# आउटपुट: ['ल्', 'य्', 'उ', 'ट्']

remaining, its = apply_halantyam(tokens)

print(f"२. इत् वर्ण (हलन्त्यम्): {its}")
# आउटपुट: ['ट्']

print(f"३. लोप के बाद शेष: {remaining}")
# आउटपुट: ['ल्', 'य्', 'उ']