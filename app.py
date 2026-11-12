
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(page_title="AgriOS | Smart Farm Management", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

# -------------------- Localization --------------------
T = {
    "English": {
        "nav":"NAVIGATION", "overview":"Overview", "crop":"Crop Management", "soil":"Soil & Nutrients",
        "irrigation":"Irrigation Planning", "disease":"AI Crop Disease Detection", "weather":"Weather Risk",
        "resources":"Farm Resources & Costs", "learn":"Education & Training", "decision":"Decision Support",
        "voice":"Voice Assistant", "settings":"Farm Settings", "farm":"Farm profile", "location":"Farm location",
        "area":"Farm area (acres)", "crop_type":"Main crop", "welcome":"Your farm, one intelligent workspace.",
        "subtitle":"Your farm performance at a glance. Monitor crops, soil, water and field activity.",
        "overview_title":"Farm overview", "conditions":"Current farm conditions", "temperature":"Temperature",
        "humidity":"Humidity", "rain":"Rain chance", "soil_moisture":"Soil moisture", "alerts":"Priority alerts",
        "tasks":"Today's recommended tasks", "quick":"Quick actions", "stage":"Growth stage",
        "plan":"Crop plan", "planting":"Planting date", "harvest":"Expected harvest", "recommendation":"Recommendation",
        "ph":"Soil pH", "nitrogen":"Nitrogen", "phosphorus":"Phosphorus", "potassium":"Potassium",
        "soil_note":"Enter soil-test values to receive structured, crop-aware guidance.",
        "water":"Water availability", "method":"Irrigation method", "next_irrigation":"Next irrigation",
        "calculate":"Generate irrigation plan", "upload":"Upload a crop photo", "analyze":"Analyze crop image",
        "crop_select":"Select crop", "symptom":"Observed symptom", "result":"Possible condition",
        "confidence":"Symptom match", "solution":"Recommended action", "important":"Screening information",
        "notice":"Preliminary symptom-based screening: the selected crop and symptoms guide this result; the uploaded image is retained for visual reference and is not classified by a trained image model. Confirm before treatment.",
        "forecast":"7-day outlook", "risk":"Operation risk", "cost":"Estimated input costs",
        "input":"Farm input", "quantity":"Quantity", "unit_cost":"Unit cost (PKR)", "add":"Add / update estimate",
        "total":"Estimated total", "scenario":"Training scenario", "scenario_desc":"Explore how changing one farm condition affects decisions.",
        "ask":"Ask AgriOS", "question":"What would you like help with?", "send":"Get guidance",
        "language":"Language", "english":"English", "urdu":"Urdu", "sindhi":"Sindhi",
        "voice_title":"Speak to AgriOS", "voice_help":"Choose Urdu or Sindhi and record a short question. Speech recognition depends on browser/device support.",
        "record":"Record audio", "voice_lang":"Voice language", "voice_guidance":"Voice guidance",
        "save":"Save farm settings", "footer":"AgriOS • Smart Farm Management",
        "crop_tasks":"Growth-stage task planner", "task_name":"Task", "due":"Due date", "status":"Status",
        "add_task":"Add task", "soil_result":"Soil guidance", "irrigation_result":"Suggested irrigation window",
        "weather_alert":"Weather-based planning notes", "resource_note":"Enter your supplier prices and quantities to calculate seasonal input costs.",
        "module":"Module", "open":"Open module", "small":"Designed to support an integrated farm workflow alongside specialist advice."
    },
    "اردو": {
        "nav":"نیویگیشن", "overview":"جائزہ", "crop":"فصل کا انتظام", "soil":"مٹی اور غذائیت",
        "irrigation":"آبپاشی کی منصوبہ بندی", "disease":"اے آئی فصل کی بیماری کی شناخت", "weather":"موسمی خطرات",
        "resources":"زرعی وسائل اور اخراجات", "learn":"تعلیم اور تربیت", "decision":"فیصلہ سازی میں معاونت",
        "voice":"آواز کا معاون", "settings":"فارم کی ترتیبات", "farm":"فارم پروفائل", "location":"فارم کا مقام",
        "area":"فارم کا رقبہ (ایکڑ)", "crop_type":"اہم فصل", "welcome":"آپ کا فارم، ایک ذہین پلیٹ فارم۔",
        "subtitle":"چھوٹے اور درمیانے فارمز کے لیے فیصلہ سازی کا عملی نمونہ۔",
        "overview_title":"فارم کا جائزہ", "conditions":"موجودہ نمائشی حالات", "temperature":"درجہ حرارت",
        "humidity":"نمی", "rain":"بارش کا امکان", "soil_moisture":"مٹی کی نمی", "alerts":"اہم انتباہات",
        "tasks":"آج کے تجویز کردہ کام", "quick":"فوری اقدامات", "stage":"نشوونما کا مرحلہ",
        "plan":"فصل کا منصوبہ", "planting":"کاشت کی تاریخ", "harvest":"متوقع کٹائی", "recommendation":"تجویز",
        "ph":"مٹی کا پی ایچ", "nitrogen":"نائٹروجن", "phosphorus":"فاسفورس", "potassium":"پوٹاشیم",
        "soil_note":"مٹی کے ٹیسٹ کی قدریں درج کریں تاکہ فصل کے مطابق رہنمائی مل سکے۔",
        "water":"پانی کی دستیابی", "method":"آبپاشی کا طریقہ", "next_irrigation":"اگلی آبپاشی",
        "calculate":"آبپاشی کا منصوبہ بنائیں", "upload":"فصل کی تصویر اپ لوڈ کریں", "analyze":"تصویر کا تجزیہ (ڈیمو)",
        "crop_select":"فصل منتخب کریں", "symptom":"نظر آنے والی علامت", "result":"نمونہ تشخیص",
        "confidence":"علامتوں سے مطابقت", "solution":"تجویز کردہ اقدامات", "important":"تشخیصی معلومات",
        "notice":"یہ ابتدائی علامات پر مبنی جانچ ہے۔ حتمی تشخیص کے لیے مقامی زرعی ماہر سے رجوع کریں۔",
        "forecast":"سات دن کا نمائشی موسم", "risk":"زرعی کام کا خطرہ", "cost":"زرعی اخراجات کا تخمینہ",
        "input":"زرعی چیز", "quantity":"مقدار", "unit_cost":"فی یونٹ قیمت (روپے)", "add":"تخمینہ شامل / تبدیل کریں",
        "total":"کل تخمینہ", "scenario":"تربیتی منظرنامہ", "scenario_desc":"دیکھیں کہ فارم کی صورتحال بدلنے سے فیصلے کیسے بدلتے ہیں۔",
        "ask":"AgriOS سے پوچھیں", "question":"آپ کس بارے میں رہنمائی چاہتے ہیں؟", "send":"رہنمائی حاصل کریں",
        "language":"زبان", "english":"English", "urdu":"اردو", "sindhi":"سنڌي",
        "voice_title":"AgriOS سے بات کریں", "voice_help":"اردو یا سندھی منتخب کریں اور مختصر سوال ریکارڈ کریں۔ آواز کی شناخت براؤزر اور ڈیوائس پر منحصر ہے۔",
        "record":"آڈیو ریکارڈ کریں", "voice_lang":"آواز کی زبان", "voice_guidance":"صوتی رہنمائی",
        "save":"فارم کی ترتیبات محفوظ کریں", "footer":"AgriOS • زرعی انتظامی نظام",
        "crop_tasks":"فصل کے مرحلے کے کام", "task_name":"کام", "due":"آخری تاریخ", "status":"حالت",
        "add_task":"کام شامل کریں", "soil_result":"مٹی سے متعلق رہنمائی", "irrigation_result":"تجویز کردہ آبپاشی کا وقت",
        "weather_alert":"موسم کے مطابق منصوبہ بندی", "resource_note":"اپنے سپلائر کی قیمتیں اور مقدار درج کریں؛ نیچے دی گئی قدریں قابلِ ترمیم ڈیمو ہیں۔",
        "module":"ماڈیول", "open":"ماڈیول کھولیں", "small":"یہ مربوط نظام کا نمونہ ہے، ماہرین کا متبادل نہیں۔"
    },
    "سنڌي": {
        "nav":"رهنمائي", "overview":"جائزو", "crop":"فصل جو انتظام", "soil":"مٽي ۽ غذائيت",
        "irrigation":"آبپاشي جي رٿابندي", "disease":"اي آءِ فصل جي بيماري سڃاڻپ", "weather":"موسمي خطرا",
        "resources":"فارم جا وسيلا ۽ خرچ", "learn":"تعليم ۽ تربيت", "decision":"فيصلي ۾ مدد",
        "voice":"آواز وارو مددگار", "settings":"فارم جون سيٽنگون", "farm":"فارم پروفائل", "location":"فارم جو هنڌ",
        "area":"فارم جو ايراضي (ايڪڙ)", "crop_type":"مکيه فصل", "welcome":"توهان جو فارم، هڪ ذهين پليٽفارم.",
        "subtitle":"ننڍن ۽ وچولي فارمن لاءِ فيصلي ۾ مدد جو عملي نمونو.",
        "overview_title":"فارم جو جائزو", "conditions":"موجوده ڊيمو حالتون", "temperature":"گرمي پد",
        "humidity":"نمي", "rain":"مينهن جو امڪان", "soil_moisture":"مٽي جي نمي", "alerts":"اهم خبرداريون",
        "tasks":"اڄ جا تجويز ڪيل ڪم", "quick":"تڪڙا قدم", "stage":"واڌ جو مرحلو",
        "plan":"فصل جي رٿ", "planting":"پوکڻ جي تاريخ", "harvest":"امڪاني لابارو", "recommendation":"صلاح",
        "ph":"مٽي جو پي ايڇ", "nitrogen":"نائٽروجن", "phosphorus":"فاسفورس", "potassium":"پوٽاشيم",
        "soil_note":"مٽي جي ٽيسٽ جا انگ داخل ڪريو ته جيئن فصل مطابق رهنمائي ملي.",
        "water":"پاڻي جي دستيابي", "method":"آبپاشي جو طريقو", "next_irrigation":"ايندڙ آبپاشي",
        "calculate":"آبپاشي جو منصوبو ٺاهيو", "upload":"فصل جي تصوير اپلوڊ ڪريو", "analyze":"تصوير جو جائزو (ڊيمو)",
        "crop_select":"فصل چونڊيو", "symptom":"نظر ايندڙ نشاني", "result":"ڊيمو تشخيص",
        "confidence":"مثالي اعتماد", "solution":"تجويز ڪيل قدم", "important":"تشخيص بابت ڄاڻ",
        "notice":"هي علامتن تي ٻڌل ابتدائي جائزو آهي. پڪي تشخيص لاءِ مقامي زرعي ماهر سان رابطو ڪريو.",
        "forecast":"ست ڏينهن جو ڊيمو موسم", "risk":"زرعي ڪم جو خطرو", "cost":"زرعي خرچ جو اندازو",
        "input":"زرعي سامان", "quantity":"مقدار", "unit_cost":"في يونٽ قيمت (روپيا)", "add":"اندازو شامل / تبديل ڪريو",
        "total":"ڪل اندازو", "scenario":"تربيت وارو منظرنامو", "scenario_desc":"ڏسو ته فارم جون حالتون بدلائڻ سان فيصلا ڪيئن بدلجن ٿا.",
        "ask":"AgriOS کان پڇو", "question":"توهان کي ڪهڙي مدد گهرجي؟", "send":"رهنمائي حاصل ڪريو",
        "language":"ٻولي", "english":"English", "urdu":"اردو", "sindhi":"سنڌي",
        "voice_title":"AgriOS سان ڳالهايو", "voice_help":"اردو يا سنڌي چونڊيو ۽ مختصر سوال رڪارڊ ڪريو. آواز جي سڃاڻپ برائوزر ۽ ڊوائيس تي دارومدار رکي ٿي.",
        "record":"آڊيو رڪارڊ ڪريو", "voice_lang":"آواز جي ٻولي", "voice_guidance":"آواز جي رهنمائي",
        "save":"فارم جون سيٽنگون محفوظ ڪريو", "footer":"AgriOS • زرعي انتظام جو نظام",
        "crop_tasks":"فصل جي مرحلي جا ڪم", "task_name":"ڪم", "due":"تاريخ", "status":"حالت",
        "add_task":"ڪم شامل ڪريو", "soil_result":"مٽي بابت رهنمائي", "irrigation_result":"تجويز ڪيل آبپاشي جو وقت",
        "weather_alert":"موسم مطابق رٿابندي", "resource_note":"پنهنجي سپلائر جون قيمتون ۽ مقدار داخل ڪريو؛ هيٺيان انگ ڊيمو آهن.",
        "module":"ماڊيول", "open":"ماڊيول کوليو", "small":"هي گڏيل نظام جو نمونو آهي، ماهرن جو متبادل ناهي۔"
    }
}

if "lang" not in st.session_state: st.session_state.lang = "English"
if "page" not in st.session_state: st.session_state.page = "Overview"
lang = st.sidebar.selectbox("🌐 " + ("Language / زبان / ٻولي"), ["English", "اردو", "سنڌي"],
                           index=["English","اردو","سنڌي"].index(st.session_state.lang))
st.session_state.lang = lang
t = T[lang]
rtl = lang != "English"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Noto+Nastaliq+Urdu&display=swap');
:root{--green:#16865b;--deep:#173e2e;--mint:#e9f4ed;--ink:#202b25;--muted:#7b8580}
.stApp{background:#f1f3f1;color:var(--ink);font-family:'DM Sans',sans-serif}
section[data-testid="stSidebar"]{background:#f7f8f7;border-right:1px solid #e2e7e3;min-width:76px!important}
section[data-testid="stSidebar"] *{color:#45534b}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{color:#647168}
.block-container{padding:1.15rem 1.35rem 1.5rem;max-width:1600px}
.hero{background:transparent;padding:3px 2px 15px;border-radius:0;color:#202b25;box-shadow:none;margin-bottom:8px}
.hero h1{font-size:1.55rem;font-weight:700;margin:0 0 4px;color:#202b25}.hero p{color:#7b8580;margin:0;font-size:.88rem}
.eyebrow{font-size:.66rem;letter-spacing:.13em;font-weight:800;color:#16865b;text-transform:uppercase;margin-bottom:5px}
.metric{background:#fff;border:1px solid #e5e9e6;border-radius:15px;padding:15px 17px;box-shadow:0 3px 12px #172b1e08;min-height:105px}
.metric .k{color:#78847d;font-size:.78rem;font-weight:600}.metric .v{font-size:1.55rem;font-weight:800;color:#183d2c;margin-top:6px}.metric .s{font-size:.73rem;color:#25845a;margin-top:3px}
.panel{background:white;border:1px solid #e5e9e6;border-radius:15px;padding:17px 18px;margin:8px 0;box-shadow:0 3px 12px #172b1e08}
.panel h3{color:#24352b;margin-top:0;font-size:1rem}
.pill{display:inline-block;background:#e5f4eb;color:#16764e;border-radius:30px;padding:5px 10px;font-size:.7rem;font-weight:700}
.alert{background:#fff7e8;border-left:4px solid #e3a23b;padding:12px 14px;border-radius:10px;color:#694c1c;margin:8px 0}
.info{background:#edf5ff;border-left:4px solid #5b9be0;padding:12px 14px;border-radius:10px;color:#294b70;margin:8px 0}
div.stButton>button{background:#16865b;color:white;border:0;border-radius:10px;padding:.55rem 1rem;font-weight:700}
div.stButton>button:hover{background:#116b48;color:white}
[data-testid="stMetric"]{background:white;border:1px solid #e5e9e6;padding:14px;border-radius:14px}
h1,h2,h3{letter-spacing:-.02em}
[data-testid="stFileUploader"]{background:#f8faf8;border:1px dashed #b7c9bd;border-radius:12px;padding:8px}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

if rtl:
    st.markdown("<style>.stApp, .stMarkdown, label, p, h1,h2,h3,div[data-testid='stMarkdownContainer']{direction:rtl;text-align:right;font-family:'Noto Nastaliq Urdu','DM Sans',sans-serif} section[data-testid='stSidebar']{direction:rtl}</style>", unsafe_allow_html=True)

pages = [t["overview"],t["crop"],t["soil"],t["irrigation"],t["disease"],t["weather"],t["resources"],t["learn"],t["decision"],t["voice"],t["settings"]]
english_pages = ["Overview","Crop Management","Soil & Nutrients","Irrigation Planning","AI Crop Disease Detection","Weather Risk","Farm Resources & Costs","Education & Training","Decision Support","Voice Assistant","Farm Settings"]
mapping = dict(zip(english_pages,pages))
reverse = dict(zip(pages,english_pages))
st.sidebar.markdown(
    """
    <div style='padding:8px 4px 20px'>
        <div style='font-size:2rem;font-weight:800;color:#173e2e;line-height:1.2'>
            🌱 AgriOS
        </div>
        <div style='color:#647168;font-size:.8rem;font-weight:600;letter-spacing:.04em'>
            SMART FARM OPERATING SYSTEM
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("**"+t["nav"]+"**")
selected = st.sidebar.radio("Modules", pages, index=pages.index(mapping.get(st.session_state.page,t["overview"])), label_visibility="collapsed")
page = reverse[selected]
st.session_state.page = page
st.sidebar.markdown("---")
st.sidebar.markdown("<span class='pill'>● FARM CONNECTED</span>",unsafe_allow_html=True)
st.sidebar.caption("AgriOS • Farm intelligence")
st.sidebar.caption("Karachi • Pakistan")

def hero(title, subtitle):
    st.markdown(f"<div class='hero'><div class='eyebrow'>AGRIOS / FIELD INTELLIGENCE</div><h1>{title}</h1><p>{subtitle}</p></div>",unsafe_allow_html=True)
def metric(label,value,sub=""):
    st.markdown(f"<div class='metric'><div class='k'>{label}</div><div class='v'>{value}</div><div class='s'>{sub}</div></div>",unsafe_allow_html=True)
def section(title, body=None):
    st.markdown(f"<div class='panel'><h3>{title}</h3>{body or ''}</div>",unsafe_allow_html=True)

crops=["Wheat","Rice","Cotton","Maize","Sugarcane","Tomato","Chilli","Onion"]
if "farm_crop" not in st.session_state: st.session_state.farm_crop="Wheat"
if "farm_area" not in st.session_state: st.session_state.farm_area=12.0

if page=="Overview":
    hero(t["welcome"],t["subtitle"])
    st.markdown(f"**{t['overview_title']}**",unsafe_allow_html=True)
    cols=st.columns(4)
    for col,(a,b,c) in zip(cols,[(t["temperature"],"31°C","Feels like 34°C"),(t["humidity"],"68%","Moderate"),(t["rain"],"35%","Possible evening showers"),(t["soil_moisture"],"24%","Below target")]):
        with col: metric(a,b,c)
    left,right=st.columns([1.35,1])
    with left:
        st.markdown(f"<div class='panel'><h3>🌾 {t['tasks']}</h3><p>• Check soil moisture before the afternoon heat</p><p>• Scout 5–10 plants per field for pest symptoms</p><p>• Review irrigation channel / pump readiness</p><p>• Record input purchases and labour costs</p></div>",unsafe_allow_html=True)
        st.markdown(f"<div class='panel'><h3>📊 Field activity</h3>",unsafe_allow_html=True)
        df=pd.DataFrame({"Week":["W1","W2","W3","W4","W5","W6"],"Field moisture (%)":[36,33,29,31,27,24],"Target (%)":[35,35,35,35,35,35]})
        fig=px.line(df,x="Week",y=["Field moisture (%)","Target (%)"],markers=True,color_discrete_sequence=["#21845b","#e0a23c"])
        fig.update_layout(height=260,margin=dict(l=5,r=5,t=10,b=5),paper_bgcolor="white",plot_bgcolor="white",legend_title_text="")
        width="stretch"
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown(f"<div class='panel'><h3>⚠️ {t['alerts']}</h3><div class='alert'><b>Water stress watch</b><br/>Soil moisture is below the target. Verify field conditions.</div><div class='alert'><b>Rain window approaching</b><br/>Avoid unnecessary spraying before expected rainfall.</div><div class='info'><b>Data status</b><br/>Weather and sensor values are sample data for evaluation.</div></div>",unsafe_allow_html=True)
        st.markdown(f"<div class='panel'><h3>🧭 {t['quick']}</h3></div>",unsafe_allow_html=True)
        for p in ["AI Crop Disease Detection","Irrigation Planning","Soil & Nutrients"]:
            if st.button("Open "+t.get("disease" if p.startswith("AI") else "irrigation" if p.startswith("Irrigation") else "soil"),key="quick"+p,use_container_width=True):
                st.session_state.page=p; st.rerun()

elif page=="Crop Management":
    hero(t["crop"],"Plan crop cycles, growth stages and field activities.")
    a,b,c=st.columns(3)
    with a: st.session_state.farm_crop=st.selectbox(t["crop_type"],crops,index=crops.index(st.session_state.farm_crop))
    with b: stage=st.selectbox(t["stage"],["Land preparation","Sowing / Transplanting","Vegetative growth","Flowering","Fruit / Grain development","Maturity / Harvest"])
    with c: st.session_state.farm_area=st.number_input(t["area"],0.5,10000.0,st.session_state.farm_area,0.5)
    d,e=st.columns(2)
    with d: planting=st.date_input(t["planting"],date.today()-timedelta(days=35))
    with e: harvest=st.date_input(t["harvest"],date.today()+timedelta(days=75))
    st.markdown("<div class='panel'><h3>🗓️ "+t["crop_tasks"]+"</h3></div>",unsafe_allow_html=True)
    task_df=pd.DataFrame([
        {"Task":"Inspect emergence / plant stand","Due":str(date.today()),"Status":"Pending"},
        {"Task":"Check weeds and field edges","Due":str(date.today()+timedelta(days=2)),"Status":"Planned"},
        {"Task":"Scout for pests and leaf symptoms","Due":str(date.today()+timedelta(days=3)),"Status":"Pending"},
        {"Task":"Review irrigation requirement","Due":str(date.today()+timedelta(days=4)),"Status":"Planned"},
    ])
    st.dataframe(task_df,use_container_width=True,hide_index=True)
    with st.expander("＋ Add a custom task"):
        newtask=st.text_input(t["task_name"]); due=st.date_input(t["due"],date.today()+timedelta(days=1),key="taskdue")
        if st.button(t["add_task"]) and newtask:
            st.success(f"Task added: {newtask} — {due}")
    st.markdown("<div class='info'>Recommendations are general crop guidance. Confirm crop calendars and pesticide/fertilizer decisions with local extension services.</div>",unsafe_allow_html=True)

elif page=="Soil & Nutrients":
    hero(t["soil"],"Combine soil-test values with crop needs to organize nutrient decisions.")
    st.info(t["soil_note"])
    a,b,c,d=st.columns(4)
    with a: ph=st.number_input(t["ph"],3.0,10.0,7.2,0.1)
    with b: n=st.number_input(t["nitrogen"]+" (mg/kg)",0,300,42)
    with c: p=st.number_input(t["phosphorus"]+" (mg/kg)",0,200,18)
    with d: k=st.number_input(t["potassium"]+" (mg/kg)",0,500,120)
    crop=st.selectbox(t["crop_select"],crops,key="soil_crop")
    if st.button("Generate soil summary"):
        notes=[]
        notes.append("pH is acidic; discuss liming only after a lab recommendation." if ph<6 else "pH is alkaline; check micronutrient availability and irrigation-water quality." if ph>7.8 else "pH is within a broadly workable range for many crops.")
        notes.append("Nitrogen reading is on the lower side in this reading; verify with a lab and crop stage." if n<40 else "Nitrogen reading is not flagged by this screening threshold.")
        notes.append("Phosphorus reading may need review against a local soil-test rating." if p<15 else "Phosphorus reading is not flagged by this screening threshold.")
        st.markdown("<div class='panel'><h3>🧪 "+t["soil_result"]+"</h3>"+"".join(f"<p>• {x}</p>" for x in notes)+"<p><b>Next step:</b> use a certified soil test and crop-specific nutrient recommendation before applying fertilizer.</p></div>",unsafe_allow_html=True)
    st.markdown("<div class='alert'>N-P-K interpretation depends on extraction method, units, soil texture and local calibration. These screening thresholds are illustrative only.</div>",unsafe_allow_html=True)

elif page=="Irrigation Planning":
    hero(t["irrigation"],"A simple rule-based planning view using crop, soil moisture, weather and water supply.")
    a,b,c=st.columns(3)
    with a: crop=st.selectbox(t["crop_select"],crops,key="irr_crop")
    with b: moisture=st.slider(t["soil_moisture"]+" (%)",0,100,24)
    with c: water=st.selectbox(t["water"],["Adequate","Limited","Very limited"])
    method=st.selectbox(t["method"],["Drip","Furrow","Basin","Sprinkler","Flood"])
    rain=st.slider(t["rain"]+" (%)",0,100,35)
    if st.button(t["calculate"]):
        if moisture<25 and rain<50: result="Inspect the root zone; irrigation may be needed soon if the field is genuinely dry."
        elif rain>=50: result="Re-check the forecast and soil before irrigating; rainfall may reduce immediate demand."
        else: result="Continue monitoring. Reassess moisture at the crop root zone during the next field check."
        if water!="Adequate": result+=" Prioritize critical growth stages and consider shorter, more efficient irrigation sets."
        st.success(result)
        st.markdown(f"<div class='panel'><h3>💧 {t['irrigation_result']}</h3><p>{result}</p><p><b>Method:</b> {method} &nbsp; • &nbsp; <b>Crop:</b> {crop}</p></div>",unsafe_allow_html=True)
    st.caption("This is not a calibrated evapotranspiration model. A future version can integrate ET₀, crop coefficient (Kc), soil texture and live weather.")

elif page=="AI Crop Disease Detection":
    hero(t["disease"],"Upload a crop image, select the visible symptoms and receive a practical field action plan.")
    st.markdown("""
    <style>
    .disease-head{background:linear-gradient(110deg,#123d2b,#267d58);padding:20px 24px;border-radius:16px;color:#fff;margin:4px 0 16px}
    .disease-head h3{color:#fff!important;margin:0 0 5px}
    .disease-card{background:#fff;border:1px solid #e4ece6;border-radius:16px;padding:18px 20px;box-shadow:0 4px 16px #173d2a0b;margin-bottom:12px}
    .disease-muted{color:#718078;font-size:.86rem}
    .result-title{font-size:1.55rem;font-weight:800;color:#174b35}
    </style>
    <div class="disease-head"><h3>🌿 Crop health assessment</h3><div>Image review · Symptom assessment · Recommended next steps</div></div>
    """, unsafe_allow_html=True)
    left,right=st.columns([1.05,1])
    with left:
        st.markdown('<div class="disease-card">', unsafe_allow_html=True)
        st.markdown("#### 1. Crop information")
        crop=st.selectbox(t["crop_select"],["Tomato","Wheat","Rice","Cotton","Chilli","Maize","Sugarcane","Onion"],key="disease_crop")
        symptom=st.selectbox("Main visible symptom",["Yellowing leaves","Brown / dark spots","White powdery coating","Leaf curling","Wilting","Holes / chewing damage","Orange / reddish powder","Unknown"],key="disease_symptom")
        uploaded=st.file_uploader("Upload leaf or crop photo",type=["jpg","jpeg","png","webp"],key="disease_upload")
        if uploaded:
            st.image(uploaded,caption="Uploaded crop image",use_container_width=True)
        analyze=st.button("🔬  Analyze crop health",use_container_width=True,type="primary")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="disease-card">
          <h4>🧭 Assessment process</h4>
          <p>01 &nbsp; Review the uploaded crop photo</p>
          <p>02 &nbsp; Assess the crop and selected symptoms</p>
          <p>03 &nbsp; Prepare a possible-condition assessment</p>
          <p>04 &nbsp; Generate practical crop-care actions</p>
          <hr/>
          <div class="disease-muted">The current assessment is symptom-guided, not a trained image-classification model. The photo helps you document field conditions. Confirm uncertain cases with a local agricultural extension officer before applying crop-protection products.</div>
        </div>
        """,unsafe_allow_html=True)
        st.markdown("""
        <div class="disease-card">
          <h4>📷 Better photo tips</h4>
          <p>• Use natural daylight and keep the leaf in focus.</p>
          <p>• Capture both the upper and lower leaf surfaces.</p>
          <p>• Include healthy and affected leaves for comparison.</p>
        </div>
        """,unsafe_allow_html=True)

    if analyze:
        if not uploaded:
            st.warning("Please upload a crop image before starting the assessment.")
        else:
            import time
            progress=st.progress(0,text="Preparing crop assessment…")
            status=st.empty()
            for step in range(1,21):
                time.sleep(0.5)
                progress.progress(step*5,text="Assessing crop symptoms…" if step<15 else "Preparing recommended actions…")
            status.success("Assessment complete.")
            progress.empty()

            condition_map={
                "Yellowing leaves":{
                    "Tomato":("Possible nutrient stress or early blight","Check whether yellowing begins on older leaves and look for concentric brown lesions. Review drainage and recent fertilizer history."),
                    "Wheat":("Possible nitrogen stress or yellow rust","Inspect leaves for yellowing patterns and orange pustules. Compare several plants across the field."),
                    "Rice":("Possible nitrogen deficiency or leaf disease","Check older leaves, field water conditions and whether lesions have distinct margins."),
                    "Cotton":("Possible nutrient stress or leaf disease","Inspect leaf undersides for insects and check whether yellowing follows the veins."),
                    "Chilli":("Possible nutrient stress or leaf spot","Check leaf undersides for mites or aphids and inspect for distinct lesions."),
                    "Maize":("Possible nutrient deficiency or leaf blight","Observe whether yellowing starts at leaf edges or follows a stripe pattern."),
                },
                "Brown / dark spots":{
                    "Tomato":("Possible early blight or bacterial leaf spot","Look for concentric rings, water-soaked margins and lower-leaf progression. Avoid overhead irrigation where practical."),
                    "Wheat":("Possible wheat leaf rust or leaf spot","Check for orange-brown pustules and inspect multiple leaves. Record whether lesions are spreading."),
                    "Rice":("Possible rice blast or brown spot","Look for diamond-shaped lesions with pale centres or round brown spots; check field history and seed source."),
                    "Cotton":("Possible Alternaria or bacterial blight","Inspect lesion edges and leaf undersides; remove badly affected debris where practical."),
                    "Chilli":("Possible Cercospora or bacterial leaf spot","Look for small circular lesions and check whether spots occur on fruit or stems too."),
                    "Maize":("Possible leaf blight or leaf spot","Note lesion shape and direction; inspect lower and upper leaves across several plants."),
                },
                "White powdery coating":{
                    "Tomato":("Possible powdery mildew","Improve airflow, avoid wetting foliage late in the day and remove heavily affected leaves if practical."),
                    "Wheat":("Possible powdery mildew","Inspect both leaf surfaces and lower canopy; avoid excessive nitrogen and monitor spread."),
                    "Rice":("Unusual symptom — verify the crop and leaf surface","Check whether the coating is fungal growth, dust or spray residue; photograph close-up and seek local advice."),
                    "Cotton":("Possible powdery mildew","Check leaf undersides and canopy density; improve airflow and monitor nearby plants."),
                    "Chilli":("Possible powdery mildew","Remove heavily affected leaves where practical and avoid dense, humid canopy conditions."),
                    "Maize":("Unusual symptom — verify before treatment","Check whether the white material wipes away and inspect for other symptoms before choosing any treatment."),
                },
                "Leaf curling":{
                    "Tomato":("Possible viral leaf curl or sap-feeding insect damage","Inspect leaf undersides for whiteflies and aphids. Remove severely affected plants only after confirming the cause; control weeds and monitor nearby plants."),
                    "Wheat":("Possible heat, water or herbicide stress","Review recent spraying, irrigation and temperature conditions; compare affected and unaffected field areas."),
                    "Rice":("Possible water stress or insect damage","Inspect for leaf folders and other insects; review water level and recent field operations."),
                    "Cotton":("Possible whitefly, aphid or environmental stress","Inspect leaf undersides and growing tips for insects; check recent spray and weather history."),
                    "Chilli":("Possible viral leaf curl associated with whiteflies","Inspect leaf undersides for whiteflies, isolate suspect plants where practical and manage weeds around the field."),
                    "Maize":("Possible water stress or herbicide injury","Review recent herbicide use, wind conditions during spraying and soil moisture."),
                },
                "Wilting":{
                    "Tomato":("Possible water stress or vascular wilt","Check root-zone moisture first; inspect stem vascular tissue and roots. Improve drainage if waterlogged and seek confirmation before treatment."),
                    "Wheat":("Possible water stress or root disease","Check soil moisture and root health; compare patches and inspect for waterlogging or root damage."),
                    "Rice":("Possible water stress or root damage","Check field water depth, root condition and whether wilting is limited to patches."),
                    "Cotton":("Possible water stress or Fusarium / Verticillium wilt","Inspect roots and stem tissue, map affected patches and avoid moving contaminated soil between fields."),
                    "Chilli":("Possible bacterial or fungal wilt, or water stress","Check root-zone moisture and stem vascular tissue; remove and safely dispose of confirmed infected plants."),
                    "Maize":("Possible drought stress or stalk/root disease","Check soil moisture, root anchorage and stalk condition; inspect whether symptoms occur in patches."),
                },
                "Holes / chewing damage":{
                    "Tomato":("Possible caterpillar or beetle feeding","Inspect leaves at dusk and check leaf undersides for eggs or larvae. Hand-pick pests where practical and use field monitoring to guide control."),
                    "Wheat":("Possible chewing insect damage","Inspect plants for larvae and feeding patterns; estimate affected area before deciding on control."),
                    "Rice":("Possible leaf folder or other chewing pest","Look for folded leaves and larvae inside; assess the percentage of affected tillers."),
                    "Cotton":("Possible caterpillar or beetle feeding","Scout terminals, squares and leaf undersides for larvae; use field counts and local thresholds."),
                    "Chilli":("Possible caterpillar or beetle feeding","Inspect buds, fruit and leaf undersides; remove visible larvae and damaged fruit where practical."),
                    "Maize":("Possible fall armyworm or other caterpillar","Look for window-pane feeding and frass in the whorl; inspect several plants per field section."),
                },
                "Orange / reddish powder":{
                    "Wheat":("Possible wheat rust","Orange or reddish powdery pustules can be consistent with rust. Inspect several leaves and arrange prompt local confirmation because rust can spread quickly."),
                    "Rice":("Possible fungal lesion or residue — verify","Photograph the affected area closely and check for distinct lesions; do not treat based on colour alone."),
                },
            }
            default_by_symptom={
                "Yellowing leaves":("Possible nutrient or environmental stress","Check soil moisture, drainage, root condition and recent fertilizer or spray history."),
                "Brown / dark spots":("Possible fungal or bacterial leaf spot","Inspect lesion shape and spread on several plants; avoid handling wet foliage and remove severely affected debris where practical."),
                "White powdery coating":("Possible powdery mildew or surface residue","Check whether the coating is powdery growth or residue and inspect both leaf surfaces."),
                "Leaf curling":("Possible insect, viral or environmental stress","Inspect leaf undersides for sap-feeding insects and review recent weather and spray history."),
                "Wilting":("Possible water stress or root / vascular disease","Check root-zone moisture, drainage and root health before changing irrigation."),
                "Holes / chewing damage":("Possible chewing insect damage","Inspect leaf undersides and growing points for eggs, larvae and fresh feeding."),
                "Orange / reddish powder":("Possible rust-like fungal symptom","Inspect multiple leaves for powdery pustules and seek prompt crop-specific confirmation."),
                "Unknown":("Unclassified crop symptom","Take clear photos of both leaf surfaces and note when symptoms began and how quickly they are spreading."),
            }
            base=condition_map.get(symptom,{}).get(crop,default_by_symptom[symptom])
            name,care=base
            st.markdown(f"""
            <div class="disease-card">
              <div class="pill">ASSESSMENT READY</div>
              <h3>🧫 {crop}: {t['result']}</h3>
              <div class="result-title">{name}</div>
              <p class="disease-muted">Based on the crop and symptom information selected above.</p>
              <hr/>
              <h4>🌱 Recommended action plan</h4>
              <p>{care}</p>
              <h4>Next steps</h4>
              <ul>
                <li>Check at least 5–10 plants in different parts of the field.</li>
                <li>Photograph affected and healthy leaves and record the date.</li>
                <li>Recheck the affected area in 24–48 hours to monitor spread.</li>
                <li>Use only crop- and disease-approved products if a local expert confirms treatment is needed; follow the product label and protective-equipment instructions.</li>
              </ul>
            </div>
            """,unsafe_allow_html=True)
            st.info("This is a preliminary symptom-based assessment, not a confirmed diagnosis from image recognition. If symptoms are severe or spreading quickly, consult your local agricultural extension service.")

elif page=="Weather Risk":
    hero(t["weather"],"Turn forecast signals into practical farm-operation checks.")
    df=pd.DataFrame({"Day":["Today","Fri","Sat","Sun","Mon","Tue","Wed"],"Max temp °C":[34,35,33,32,34,36,35],"Rain chance %":[20,15,65,75,30,10,15],"Wind km/h":[14,18,22,25,16,20,17]})
    st.dataframe(df,use_container_width=True,hide_index=True)
    fig=px.bar(df,x="Day",y="Rain chance %",color="Rain chance %",color_continuous_scale=["#d9eee1","#25845a"])
    fig.update_layout(height=280,margin=dict(l=5,r=5,t=10,b=5),paper_bgcolor="white",plot_bgcolor="white",coloraxis_showscale=False)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("<div class='panel'><h3>🌦️ "+t["weather_alert"]+"</h3><p>• Check field access and drainage ahead of the weekend rain window.</p><p>• Avoid spraying immediately before expected rainfall; follow product label and local advice.</p><p>• Schedule heat-sensitive field work during cooler hours.</p><p>• Secure loose equipment if wind speeds increase.</p></div>",unsafe_allow_html=True)
    st.caption("Forecast is sample data. Live weather integration can be added later using a weather API and farm coordinates.")

elif page=="Farm Resources & Costs":
    hero(t["resources"],"Track quantities, unit prices and indicative seasonal input budgets.")
    st.info(t["resource_note"])
    if "costs" not in st.session_state:
        st.session_state.costs=pd.DataFrame({"Input":["Seed","Fertilizer","Diesel / electricity","Labour","Crop protection"],"Quantity":[25,8,60,20,3],"Unit cost (PKR)":[850,12500,290,1800,4500]})
    edited=st.data_editor(st.session_state.costs,use_container_width=True,num_rows="dynamic",key="cost_editor")
    total=(pd.to_numeric(edited["Quantity"],errors="coerce").fillna(0)*pd.to_numeric(edited["Unit cost (PKR)"],errors="coerce").fillna(0)).sum()
    st.session_state.costs=edited
    metric(t["total"],f"PKR {total:,.0f}","Calculated from entered quantities")
    st.markdown("<div class='info'>Next iteration: supplier comparison, per-acre costing, inventory alerts, purchase records and seasonal budget export.</div>",unsafe_allow_html=True)

elif page=="Education & Training":
    hero(t["learn"],"A safe practice space for students, trainees and farm operators.")
    st.markdown(f"**{t['scenario']}**")
    st.write(t["scenario_desc"])
    crop=st.selectbox(t["crop_select"],crops,key="learn_crop")
    moisture=st.slider("Scenario soil moisture (%)",0,100,22)
    rain=st.slider("Scenario rain probability (%)",0,100,20)
    budget=st.select_slider("Available input budget",options=["Very low","Low","Medium","High"],value="Medium")
    if st.button("Run learning scenario"):
        st.markdown("<div class='panel'><h3>Scenario outcome</h3></div>",unsafe_allow_html=True)
        if moisture<25 and rain<40: st.warning("Discussion: verify soil moisture and crop stage before deciding whether to irrigate.")
        elif rain>=60: st.info("Discussion: consider postponing non-urgent irrigation and protecting field access.")
        else: st.success("Discussion: continue routine monitoring and record observations.")
        st.write(f"Budget setting: **{budget}**. Ask trainees to justify trade-offs between water, labour and input cost.")
    with st.expander("Knowledge check"):
        q=st.radio("Which action should come before applying fertilizer?",["Apply a fixed dose immediately","Review soil-test results and crop stage","Mix products without checking labels"])
        if st.button("Check answer"):
            st.success("Correct." if q=="Review soil-test results and crop stage" else "Review soil-test results and crop stage first.")

elif page=="Decision Support":
    hero(t["decision"],"Bring crop, soil, water, weather and cost signals into one decision workspace.")
    st.markdown("<div class='panel'><h3>Farm decision snapshot</h3><p><span class='pill'>FIELD SUMMARY</span></p></div>",unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        st.markdown("<div class='panel'><h3>🌱 Production signals</h3><p>Crop: Wheat (sample)</p><p>Growth stage: Vegetative (sample)</p><p>Soil moisture: 24% — review</p><p>Soil pH: 7.2 — verify locally</p></div>",unsafe_allow_html=True)
        st.markdown("<div class='panel'><h3>💰 Resource signals</h3><p>Input budget: Medium (sample)</p><p>Water availability: Limited (sample)</p><p>Labour availability: Normal (sample)</p></div>",unsafe_allow_html=True)
    with b:
        st.markdown("<div class='panel'><h3>🧭 Combined considerations</h3><ol><li>Verify moisture in the crop root zone.</li><li>Check the latest local forecast before field operations.</li><li>Prioritize critical growth-stage tasks within available water.</li><li>Record actual input and labour costs.</li></ol></div>",unsafe_allow_html=True)
        st.markdown("<div class='alert'>AgriOS organizes information; the farmer or agronomist remains the final decision-maker.</div>",unsafe_allow_html=True)
    question=st.text_area(t["question"],placeholder="e.g. What should I check before irrigating my wheat field?")
    if st.button(t["send"]) and question:
        st.info("AgriOS assistant: Start by checking the crop growth stage, root-zone soil moisture, expected rainfall and water availability. Confirm any input application with local agricultural guidance.")

elif page=="Voice Assistant":
    hero(t["voice_title"],"Urdu and Sindhi voice interaction concept for more accessible farm support.")
    st.write(t["voice_help"])
    voice_lang=st.selectbox(t["voice_lang"],["Urdu","Sindhi"])
    audio=st.audio_input(t["record"])
    typed=st.text_area("Or type your question",placeholder="اپنی فصل کے بارے میں سوال لکھیں / پنهنجي فصل بابت سوال لکو")
    if audio:
        st.audio(audio)
        st.info("Audio captured. Speech-to-text is a planned integration; this does not yet transcribe the recording.")
    if st.button(t["voice_guidance"]):
        response_ur="آبپاشی سے پہلے مٹی کی نمی، فصل کے مرحلے اور بارش کے امکان کو ضرور دیکھیں۔"
        response_sd="آبپاشي کان اڳ مٽي جي نمي، فصل جي مرحلي ۽ مينهن جي امڪان کي ضرور ڏسو."
        response=response_ur if voice_lang=="Urdu" else response_sd
        st.markdown(f"<div class='panel'><h3>🔊 {t['voice_guidance']}</h3><p style='font-size:1.15rem'>{response}</p></div>",unsafe_allow_html=True)
        st.caption("Text response is provided below. Text-to-speech and speech-to-text can be connected in the next iteration.")
    st.markdown("<div class='info'>Planned implementation: browser microphone → Urdu/Sindhi speech-to-text → AgriOS assistant → Urdu/Sindhi text-to-speech.</div>",unsafe_allow_html=True)

elif page=="Farm Settings":
    hero(t["settings"],"Set the farm profile used by AgriOS.")
    name=st.text_input("Farm name","My Farm")
    loc=st.text_input(t["location"],"Karachi, Sindh, Pakistan")
    area=st.number_input(t["area"],0.5,10000.0,st.session_state.farm_area,0.5)
    crop=st.selectbox(t["crop_type"],crops,index=crops.index(st.session_state.farm_crop))
    if st.button(t["save"]):
        st.session_state.farm_crop=crop; st.session_state.farm_area=area
        st.success("Farm profile updated for this session.")
    st.markdown("<div class='panel'><h3>System configuration</h3><p>• Weather: forecast data source required</p><p>• Disease assessment: symptom-guided screening</p><p>• Soil / irrigation: rule-based guidance</p><p>• Storage: session state only; no permanent database</p><p>• Authentication: not implemented</p></div>",unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center;color:#87948c;font-size:.75rem;padding:28px 0 10px'>{t['footer']}</div>",unsafe_allow_html=True)
