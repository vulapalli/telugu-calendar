import streamlit as st
import ephem
import math
from datetime import datetime
import pytz
import base64
# --- PROFESSIONAL UI OVERRIDE ---
st.set_page_config(page_title="Telugu Panchangam", page_icon="🕉️", layout="wide")

hide_ui_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* This removes the padding at the top for a cleaner look */
    .block-container {padding-top: 2rem;}
    </style>
"""
st.markdown(hide_ui_style, unsafe_allow_html=True)

# --- 1. ENGINE (No changes here, kept for NameError safety) ---
def format_lang(pair, mode):
    if mode == "Telugu": return pair[0]
    if mode == "English": return pair[1]
    return f"{pair[0]} ({pair[1]})"

def calculate_panchangam(dt_local, tz_name, mode):
    SAMVATSARALU = [["ప్రభవ", "Prabhava"], ["విభవ", "Vibhava"], ["శుక్ల", "Shukla"], ["ప్రమోదూత", "Pramodoota"], ["ప్రజోత్పత్తి", "Prajotpatti"], ["అంగీరస", "Angirasa"], ["శ్రీముఖ", "Srimukha"], ["భావ", "Bhava"], ["యువ", "Yuva"], ["ధాత", "Dhata"], ["ఈశ్వర", "Eswara"], ["బహుధాన్య", "Bahudhanya"], ["ప్రమాది", "Pramadi"], ["విక్రమ", "Vikrama"], ["వృష", "Vrisha"], ["చిత్రభాను", "Chitrabhanu"], ["స్వభాను", "Swabhanu"], ["తారణ", "Tarana"], ["పార్థివ", "Parthiva"], ["వ్యయ", "Vyaya"], ["సర్వజిత్తు", "Sarvajittu"], ["సర్వధారి", "Sarvadhari"], ["విరోధి", "Virodhi"], ["వికృతి", "Vikruti"], ["ఖర", "Khara"], ["నందన", "Nandana"], ["విజయ", "Vijaya"], ["జయ", "Jaya"], ["మన్మథ", "Manmatha"], ["దుర్ముఖి", "Durmukhi"], ["హేవిలంబి", "Hevilambi"], ["విలంబి", "Vilambi"], ["వికారి", "Vikari"], ["శార్వరి", "Sharvari"], ["ప్లవ", "Plava"], ["శుభకృతు", "Shubhakrutu"], ["శోభకృతు", "Sobhakrutu"], ["క్రోధి", "Krodhi"], ["విశ్వావసు", "Vishwavasu"], ["పరాభవ", "Parabhava"], ["ప్లవంగ", "Plavanga"], ["కీలక", "Keelaka"], ["సౌమ్య", "Saumya"], ["సాధారణ", "Sadharana"], ["విరోధికృతు", "Virodhikrutu"], ["పరీధావి", "Paridhavi"], ["ప్రమాదీచ", "Pramadicha"], ["ఆనంద", "Ananda"], ["రాక్షస", "Rakshasa"], ["నల", "Nala"], ["పింగళ", "Pingala"], ["కాళయుక్తి", "Kalayukti"], ["సిద్ధార్థి", "Siddharthi"], ["రౌద్రి", "Raudri"], ["దుర్మతి", "Durmati"], ["దుందుభి", "Dundubhi"], ["రుధిరోద్గారి", "Rudhirodgari"], ["రక్తాక్షి", "Raktakshi"], ["క్రోధన", "Krodhana"], ["అక్షయ", "Akshaya"]]
    MONTHS = [["చైత్రము", "Chaitramu"], ["వైశాఖము", "Vaishakhamu"], ["జ్యేష్ఠము", "Jyeshthamu"], ["ఆషాఢము", "Ashadhamu"], ["శ్రావణము", "Shravanamu"], ["భాద్రపదము", "Bhadrapadamu"], ["ఆశ్వయుజము", "Ashwayujamu"], ["కార్తీకము", "Kartikamu"], ["మార్గశిరము", "Margashiramu"], ["పుష్యము", "Pushyamu"], ["మాఘము", "Maghamu"], ["ఫాల్గుణము", "Phalgunamu"]]
    TITHIS = [["పాడ్యమి", "Padyami"], ["విదియ", "Vidiya"], ["తదియ", "Tadiya"], ["చవితి", "Chavithi"], ["పంచమి", "Panchami"], ["షష్ఠి", "Shashti"], ["సప్తమి", "Saptami"], ["అష్టమి", "Ashtami"], ["నవమి", "Navami"], ["దశమి", "Dashami"], ["ఏకాదశి", "Ekadashi"], ["ద్వాదశి", "Dvadashi"], ["త్రయోదశి", "Trayodashi"], ["చతుర్దశి", "Chaturdashi"], ["పౌర్ణమి", "Pournami"], ["పాడ్యమి", "Padyami"], ["విదియ", "Vidiya"], ["తదియ", "Tadiya"], ["చవితి", "Chavithi"], ["పంచమి", "Panchami"], ["షష్ఠి", "Shashti"], ["సప్తమి", "Saptami"], ["అష్టమి", "Ashtami"], ["నవమి", "Navami"], ["దశమి", "Dashami"], ["ఏకాదశి", "Ekadashi"], ["ద్వాదశి", "Dvadashi"], ["త్రయోదశి", "Trayodashi"], ["చతుర్దశి", "Chaturdashi"], ["అమావాస్య", "Amavasya"]]
    VARAMS = [["ఆదివారము", "Aadivaramu"], ["సోమవారము", "Somavaramu"], ["మంగళవారము", "Mangalavaramu"], ["బుధవారము", "Budhavaramu"], ["గురువారము", "Guruvaramu"], ["శుక్రవారము", "Shukravaramu"], ["శనివారము", "Shanivaramu"]]
    RUTUS = [["వసంత", "Vasanta"], ["గ్రీష్మ", "Grishma"], ["వర్ష", "Varsha"], ["శరద్", "Sharad"], ["హేమంత", "Hemanta"], ["శిశిర", "Shishira"]]
    AAYANAMS = [["ఉత్తరాయణము", "Uttarayanamu"], ["దక్షిణాయణము", "Dakshinayana"]]
    PAKSHAMS = [["శుక్ల పక్షము", "Shukla Paksham"], ["కృష్ణ పక్షము", "Krishna Paksham"]]

    tz = pytz.timezone(tz_name)
    dt_utc = tz.localize(dt_local).astimezone(pytz.utc)
    sun, moon = ephem.Sun(), ephem.Moon()
    ayanamsa = 23.85 + ((dt_utc.year + (dt_utc.month - 1)/12.0 + dt_utc.day/365.0) - 1950) * 0.01397
    
    def get_lon(body, time):
        body.compute(time)
        return (math.degrees(ephem.Ecliptic(body).lon) - ayanamsa) % 360

    s_lon, m_lon = get_lon(sun, dt_utc), get_lon(moon, dt_utc)
    t_idx = int(((m_lon - s_lon) % 360) // 12)
    v_idx = (dt_local.weekday() + 1) % 7
    
    ug_nm = ephem.next_new_moon(datetime(dt_local.year, 3, 1))
    calc_year = dt_local.year - 1 if dt_utc < ug_nm.datetime().replace(tzinfo=pytz.utc) else dt_local.year
    sam_idx = (calc_year - 1987) % 60
    
    pnm = ephem.previous_new_moon(dt_utc)
    m_idx = (int(get_lon(sun, pnm) // 30) + 1) % 12
    
    lbls = {"Telugu": ["సంవత్సరం", "అయనం", "ఋతువు", "మాసం", "పక్షం", "తిథి", "వారం"],
            "English": ["Year", "Aayanam", "Rutu", "Month", "Paksham", "Tithi", "Varam"],
            "Bilingual": ["సంవత్సరం (Year)", "అయనం (Aayanam)", "ఋతువు (Rutu)", "మాసం (Month)", "పక్షం (Paksham)", "తిథి (Tithi)", "వారం (Varam)"]}[mode]

    return {lbls[0]: format_lang(SAMVATSARALU[sam_idx], mode),
            lbls[1]: format_lang(AAYANAMS[0] if 270 <= s_lon or s_lon < 90 else AAYANAMS[1], mode),
            lbls[2]: format_lang(RUTUS[m_idx // 2], mode),
            lbls[3]: format_lang(MONTHS[m_idx], mode),
            lbls[4]: format_lang(PAKSHAMS[0] if t_idx < 15 else PAKSHAMS[1], mode),
            lbls[5]: format_lang(TITHIS[t_idx], mode),
            lbls[6]: format_lang(VARAMS[v_idx], mode)}

# --- 2. LOCATION DATA ---
@st.cache_data
def get_locations():
    locs = []
    for code, name in pytz.country_names.items():
        timezones = pytz.country_timezones.get(code, [])
        for tz in timezones:
            city = tz.split('/')[-1].replace('_', ' ')
            label = f"{name} ({city})" if len(timezones) > 1 else name
            locs.append({"label": label, "tz": tz})
    return sorted(locs, key=lambda x: x['label'])

# --- 3. UI SETUP ---
st.set_page_config(page_title="Panchangam", layout="wide")

# --- RESET LOGIC FIX ---
# Initialize session state keys for the widgets
if "d_key" not in st.session_state:
    st.session_state.d_key = datetime.now().date()
if "t_key" not in st.session_state:
    st.session_state.t_key = datetime.now().time()

def reset_to_now():
    # Force update the widget values directly in session state
    st.session_state.d_key = datetime.now().date()
    st.session_state.t_key = datetime.now().time()

st.title("🕉️ Telugu Daily Panchangam")

location_data = get_locations()
labels = [i['label'] for i in location_data]

# Layout
c1, c2 = st.columns([1, 2])
with c1:
    lang = st.selectbox("Language / భాష", ["Bilingual", "Telugu", "English"])
with c2:
    default_idx = next((i for i, v in enumerate(labels) if "Singapore" in v), 0)
    sel_label = st.selectbox("Select Country", labels, index=default_idx)
    sel_tz = next(i['tz'] for i in location_data if i['label'] == sel_label)

# The date and time pickers MUST use the key to bind to session_state
c3, c4 = st.columns(2)
with c3:
    d = st.date_input("Date", key="d_key")
with c4:
    t = st.time_input("Time", key="t_key")

# Calculate results based on the widget values
results = calculate_panchangam(datetime.combine(d, t), sel_tz, lang)

st.divider()

# --- DISPLAY CARD ---
st.info(f"📍 **{sel_label}** | 🕒 {d.strftime('%d-%b-%Y')} {t.strftime('%H:%M')}")

grid = st.columns(2)
items = list(results.items())
for i, (k, v) in enumerate(items):
    with grid[i % 2]:
        st.metric(label=k, value=v)

st.divider()

# --- ACTION BUTTONS ---
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    # Reset Button
    st.button("🔄 Reset to Current Time", on_click=reset_to_now, use_container_width=True)

with btn_col2:
    # Sharing Formatting
    share_text = f"🕉️ *Telugu Panchangam*\n📍 {sel_label}\n📅 {d.strftime('%d-%b-%Y')}\n"
    for k, v in results.items():
        share_text += f"• *{k}*: {v}\n"
    whatsapp_url = f"https://wa.me/?text={share_text.replace(' ', '%20').replace('#', '%23').replace('\n', '%0A')}"
    
    st.markdown(f'''<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
        <div style="text-align:center; border-radius:10px; background-color:#25D366; color:white; padding:10px; font-weight:bold;">
            🟢 Share on WhatsApp
        </div></a>''', unsafe_allow_html=True)
