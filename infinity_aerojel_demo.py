import streamlit as st
import pandas as pd
import random
import base64
import os

# Arka plan ve logo ayarları
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Arka plan resmi
if os.path.exists("background.png"):
    img_base64 = get_base64_of_bin_file("background.png")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Sol üstte logo
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .logo-img {{
            position: fixed;
            top: 100px;
            left: 100px;
            max-width: 180px;
            max-height: 180px;
            z-index: 10000;
            margin: 0 !important;
            padding: 0 !important;
            display: block;
        }}
        </style>
        <img src="data:image/png;base64,{logo_base64}" class="logo-img" />
        """,
        unsafe_allow_html=True
    )

# Sağ altta takım logosu (varsa)
if os.path.exists("team_logo.png"):
    with open("team_logo.png", "rb") as team_logo_file:
        team_logo_base64 = base64.b64encode(team_logo_file.read()).decode()
    st.markdown(
        f'''
        <img src="data:image/png;base64,{team_logo_base64}" style="
            position: fixed;
            bottom: 10px;
            right: 10px;
            max-width: 120px;
            max-height: 120px;
            z-index: 9999;
            margin: 0 !important;
            padding: 0 !important;
            display: block;
        " />
        ''',
        unsafe_allow_html=True
    )

# Dil metinleri
texts = {
    "Türkçe": {
        "welcome": "### HOŞGELDİNİZ\nBaşlamak için **Devam Et** butonuna basınız.",
        "continue": "DEVAM ET",
        "select_language": "Dil Seçimi",
        "languages": ["Türkçe", "English", "عربي"],
        "enter_tc": "Lütfen TC Kimlik Numaranızı Giriniz",
        "enter_age": "Lütfen Yaşınızı Giriniz",
        "enter_gender": "Lütfen Cinsiyetinizi Seçiniz",
        "genders": ["Erkek", "Kadın", "Diğer"],
        "symptoms": [
            ("Terleme Durumunu Gir", "sweating", 10),
            ("Ateş, Baş Ağrısı Gir", "fever", 15),
            ("Karın Ağrısı Gir", "abdominal_pain", 5),
            ("Nefes Darlığı Gir", "breath", 15),
            ("Mide Bulantısı Gir", "nausea", 5),
            ("Göğüs Ağrısı Gir", "chest_pain", 8)
        ],
        "symptom_question": "Durumunuz nedir?",
        "yes": "Evet",
        "no": "Hayır",
        "score": "### Hasta Puanı: ",
        "info": "TriAl sizi değerlendirme odasına yönlendiriyor. Sıra Numaranız: X\nYazdır ve Anons Yap",
        "warn": "Orta Acil durum. TriAl sizi kısa süre içinde değerlendirme odasına yönlendiriyor. Sıra Numaranız: X\nYazdır ve Anons Yap",
        "error": "ACİL DURUM. Lütfen beklemeden odaya geçiniz.",
        "reset": "Başa Dön"
    },
    "English": {
        "welcome": "### WELCOME\nPress **Continue** to start.",
        "continue": "CONTINUE",
        "select_language": "Select Language",
        "languages": ["Türkçe", "English", "عربي"],
        "enter_tc": "Please enter your ID number",
        "enter_age": "Please enter your age",
        "enter_gender": "Please select your gender",
        "genders": ["Male", "Female", "Other"],
        "symptoms": [
            ("Enter Sweating Status", "sweating", 10),
            ("Enter Fever, Headache", "fever", 15),
            ("Enter Abdominal Pain", "abdominal_pain", 5),
            ("Enter Shortness of Breath", "breath", 15),
            ("Enter Nausea", "nausea", 5),
            ("Enter Chest Pain", "chest_pain", 8)
        ],
        "symptom_question": "What is your status?",
        "yes": "Yes",
        "no": "No",
        "score": "### Patient Score: ",
        "info": "TriAl is directing you to the evaluation room. Your Queue Number: X\nPrint and Announce",
        "warn": "Moderate Emergency. TriAl will direct you to the evaluation room soon. Your Queue Number: X\nPrint and Announce",
        "error": "EMERGENCY. Please proceed to the room immediately.",
        "reset": "Restart"
    },
    "عربي": {
        "welcome": "### مرحبًا\nاضغط **متابعة** للبدء.",
        "continue": "متابعة",
        "select_language": "اختيار اللغة",
        "languages": ["Türkçe", "English", "عربي"],
        "enter_tc": "الرجاء إدخال رقم الهوية",
        "enter_age": "الرجاء إدخال عمرك",
        "enter_gender": "الرجاء اختيار جنسك",
        "genders": ["ذكر", "أنثى", "آخر"],
        "symptoms": [
            ("أدخل حالة التعرق", "sweating", 10),
            ("أدخل الحمى، الصداع", "fever", 15),
            ("أدخل ألم البطن", "abdominal_pain", 5),
            ("أدخل ضيق التنفس", "breath", 15),
            ("أدخل الغثيان", "nausea", 5),
            ("أدخل ألم الصدر", "chest_pain", 8)
        ],
        "symptom_question": "ما هي حالتك؟",
        "yes": "نعم",
        "no": "لا",
        "score": "### درجة المريض: ",
        "info": "TriAl يوجهك إلى غرفة التقييم. رقم دورك: X\nاطبع وأعلن",
        "warn": "حالة طوارئ متوسطة. TriAl سيوجهك إلى غرفة التقييم قريبًا. رقم دورك: X\nاطبع وأعلن",
        "error": "حالة طوارئ. يرجى التوجه إلى الغرفة فورًا.",
        "reset": "البدء من جديد"
    }
}

# Session state başlat
if 'step' not in st.session_state:
    st.session_state.step = "welcome"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'language' not in st.session_state:
    st.session_state.language = "Türkçe"
if 'answers' not in st.session_state:
    st.session_state.answers = []

def reset():
    st.session_state.step = "welcome"
    st.session_state.score = 0
    st.session_state.answers = []
    for key in list(st.session_state.keys()):
        if key not in ['step', 'score', 'language', 'answers']:
            del st.session_state[key]
    st.rerun()

def is_valid_tc(tc):
    return tc.isdigit() and len(tc) == 11

def main():
    # Sağ üstte dil seçici
    st.markdown(
        """
        <style>
        .lang-radio {
            position: fixed;
            top: 100px;
            right: 100px;
            width: 100px;
            background: rgba(255,255,255,0.0);
            margin: 0 !important;
            padding: 0 !important;
            z-index: 10000;
            display: block;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="lang-radio">', unsafe_allow_html=True)
        lang_select = st.radio(
            "Dil Seçimi",
            options=["Türkçe", "English", "عربي"],
            key="lang_select_top"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        if lang_select != st.session_state.language:
            st.session_state.language = lang_select
            st.rerun()

    lang = st.session_state.language
    t = texts[lang]

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.title("Hasta Değerlendirme Sistemi / Patient Evaluation System")

    if st.session_state.step == "welcome":
        st.write(t["welcome"])
        if st.button(t["continue"], key="btn_welcome"):
            st.session_state.step = "tc_kimlik"
            st.rerun()

    elif st.session_state.step == "tc_kimlik":
        tc = st.text_input(t["enter_tc"], key="tc_input")
        st.session_state.tc_kimlik = tc
        if st.button(t["continue"], key="btn_tc"):
            if is_valid_tc(tc):
                st.session_state.step = "age"
                st.rerun()
            else:
                st.warning(
                    "TC Kimlik numarası 11 haneli ve sadece rakamlardan oluşmalıdır." if lang == "Türkçe" else
                    "ID number must be 11 digits." if lang == "English" else
                    "يجب أن يتكون رقم الهوية من 11 رقمًا فقط.")

    elif st.session_state.step == "age":
        age = st.number_input(t["enter_age"], min_value=0, max_value=150, key="age_input", label_visibility="visible")
        st.session_state.age = age
        if st.button(t["continue"], key="btn_age"):
            if 0 < age <= 150:
                st.session_state.step = "gender"
                st.rerun()
            else:
                st.warning("Yaş 0 ile 150 arasında olmalıdır.")

    elif st.session_state.step == "gender":
        gender = st.selectbox(t["enter_gender"], options=t["genders"], key="gender_select_unique")
        st.session_state.gender = gender
        if st.button(t["continue"], key="btn_gender"):
            st.session_state.step = t["symptoms"][0][1]
            st.rerun()

    # Semptomlar
    symptoms = t["symptoms"]
    symptom_keys = [s[1] for s in symptoms]
    if st.session_state.step in symptom_keys:
        idx = symptom_keys.index(st.session_state.step)
        symptom_text = symptoms[idx][0]
        st.subheader(symptom_text)
        answer = st.radio(
            t["symptom_question"],
            options=[t["yes"], t["no"]],
            key=f"radio_{st.session_state.step}_unique"
        )
        if st.button(t["continue"], key=f"btn_{st.session_state.step}_unique"):
            puan = symptoms[idx][2] if answer == t["yes"] else 0
            found = False
            for a in st.session_state.answers:
                if a["symptom"] == symptom_text:
                    a["answer"] = answer
                    a["score"] = puan
                    found = True
            if not found:
                st.session_state.answers.append({
                    "symptom": symptom_text,
                    "answer": answer,
                    "score": puan
                })
            if answer == t["yes"]:
                st.session_state.score += symptoms[idx][2]
            if idx + 1 < len(symptoms):
                st.session_state.step = symptoms[idx + 1][1]
            else:
                st.session_state.step = "result"
            st.rerun()

    elif st.session_state.step == "result":
        st.write(f"{t['score']}{st.session_state.score}")
        queue_number = random.randint(0, 1000)
        df = pd.DataFrame(st.session_state.answers)
        df = df.rename(columns={"symptom": "Soru", "answer": "Cevap", "score": "Puan"})
        st.table(df)
        st.markdown(f"""
            **TC Kimlik No:** {st.session_state.get('tc_kimlik', '-')}
            **Yaş:** {st.session_state.get('age', '-')}
            **Cinsiyet / Gender:** {st.session_state.get('gender', '-')}
            """)
        info_text = t["info"].replace("X", str(queue_number))
        warn_text = t["warn"].replace("X", str(queue_number))
        if st.session_state.score < 50:
            st.info(info_text)
        elif st.session_state.score < 100:
            st.warning(warn_text)
        else:
            st.error(t["error"])
        if st.button(t["reset"], key="btn_reset"):
            reset()

if __name__ == "__main__":
    main()