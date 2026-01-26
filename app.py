import streamlit as st
from core.phonology import sanskrit_varna_vichhed

st.title("🕉️ अष्टाध्यायी-यंत्र: वर्ण-विच्छेदक")
input_val = st.text_input("संस्कृत शब्द/धातु/प्रत्यय लिखें:", value="डुभृञ्")

if input_val:
    varna_list = sanskrit_varna_vichhed(input_val)
    st.write("### विच्छेदित वर्ण सूची:")
    st.write(varna_list)

    # विज़ुअलाइज़ेशन के लिए
    formatted_output = " + ".join(varna_list)
    st.code(formatted_output, language=None)