st.subheader("📖 Vedic Svara Scanner")
vedic_input = st.text_input("Vedic Text Enter करें:", value="अ॒ग्निमी॑ळे")

if vedic_input:
    svara_report = []
    for i, char in enumerate(vedic_input):
        if char == '\u0952':
            svara_report.append({"वर्ण": vedic_input[i - 1], "Pitch": "Anudatta", "Sutra": "१.२.३० (नीचैरनुदात्तः)"})
        elif char == '\u0951':
            svara_report.append({"वर्ण": vedic_input[i - 1], "Pitch": "Svarit", "Sutra": "१.२.३१ (समाहारः स्वरितः)"})

    if svara_report:
        st.table(pd.DataFrame(svara_report))
    else:
        st.info("No specific Anudatta/Svarit marks found. Defaulting to Udatta (१.२.२९).")