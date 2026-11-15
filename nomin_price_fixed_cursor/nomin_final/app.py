from pathlib import Path
import pandas as pd
import streamlit as st
st.set_page_config(page_title='Хэмнэлттэй сагс | Номин',page_icon='🛒',layout='wide')

st.markdown("""
<style>
/* ONLY RED, YELLOW, BLACK AND WHITE */

.stApp {
    background: #FFFFFF !important;
    color: #111111 !important;
}


/* RED SIDEBAR */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: #E52528 !important;
    color: #FFFFFF !important;
}

/* WHITE SIDEBAR TEXT */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #FFFFFF !important;
}

/* KEEP INPUT TEXT BLACK */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

/* WHITE DROPDOWN WITH BLACK TEXT */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #111111 !important;
}


section[data-testid="stSidebar"] {
    border-right: 3px solid #E52528 !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #E52528 !important;
    font-weight: 800 !important;
}

/* TEXT */
.stApp p,
.stApp label,
.stApp span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #111111 !important;
}

/* NUMBER INPUT - WHITE WITH BLACK TEXT */
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] input {
    background: #FFFFFF !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

div[data-testid="stNumberInput"] div[data-baseweb="input"] {
    border: 2px solid #111111 !important;
    border-radius: 12px !important;
}

div[data-testid="stNumberInput"] button {
    background: #FFD600 !important;
    color: #111111 !important;
}

div[data-testid="stNumberInput"] button svg {
    fill: none !important;
    stroke: #111111 !important;
}

/* DROPDOWN */
div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 2px solid #111111 !important;
    border-radius: 12px !important;
    color: #111111 !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] svg {
    color: #111111 !important;
    fill: #111111 !important;
}

/* DROPDOWN OPTIONS */
div[role="listbox"],
div[role="option"] {
    background: #FFFFFF !important;
    color: #111111 !important;
}

/* RADIO BUTTONS */
div[data-testid="stRadio"] label {
    color: #111111 !important;
}

div[data-testid="stRadio"] input:checked + div {
    background: #E52528 !important;
}

/* RECIPE CARDS */
div[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 2px solid #FFD600 !important;
    border-radius: 16px !important;
    overflow: hidden;
    margin-bottom: 12px;
}

div[data-testid="stExpander"] summary {
    background: #FFD600 !important;
    color: #111111 !important;
    font-weight: 700 !important;
}

div[data-testid="stExpander"] summary * {
    color: #111111 !important;
}

div[data-testid="stExpander"] details,
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #FFFFFF !important;
    color: #111111 !important;
}

/* PRICE BOXES */
div[data-testid="stMetric"] {
    background: #FFD600 !important;
    border: 2px solid #111111 !important;
    border-radius: 16px !important;
    padding: 18px !important;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

/* BUTTONS */
.stButton > button {
    background: #FFD600 !important;
    color: #111111 !important;
    border: 2px solid #111111 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background: #E52528 !important;
    color: #FFFFFF !important;
}

/* LINKS */
a {
    color: #E52528 !important;
    font-weight: 700 !important;
}

/* CAPTIONS */
div[data-testid="stCaptionContainer"],
div[data-testid="stCaptionContainer"] * {
    color: #111111 !important;
}

/* TOP BAR */
header[data-testid="stHeader"] {
    background: #FFFFFF !important;
}

/* ALL ICONS INSIDE INPUTS */
div[data-baseweb="input"] svg,
div[data-baseweb="select"] svg {
    color: #111111 !important;
}

</style>
""", unsafe_allow_html=True)
ROOT=Path(__file__).parent
@st.cache_data
def load():
 d=pd.read_csv(ROOT/'data/products.csv',dtype=str).fillna('')
 d['price_mnt']=pd.to_numeric(d.price_mnt,errors='coerce')
 return d
raw=load()
P=raw[(raw.status=='verified') & raw.price_mnt.notna() & (raw.price_mnt>0)].copy()
# Ingredient groups reflect the user's own categorization, not inferred product titles.
KEY={'beef':'Үхрийн мах','mutton':'Хонины мах','pork':'Гахайн мах','chicken':'Тахианы мах','sausage':'Хиам','egg':'Өндөг','flour':'Гурил','noodle':'Гоймон','bread':'Талх','rice':'Цагаан будаа','instant':'Бэлэн гоймон','buckwheat':'Гурвалжин будаа','onion':'Сонгино','potato':'Төмс','garlic':'Сармис','cucumber':'Өргөст хэмх','carrot':'Лууван','cabbage':'Байцаа','tomato':'Улаан лооль','pepper':'Амтат чинжүү','oil':'Ургамлын тос','blackpepper':'Хар перец','tomatosauce':'Улаан лоолийн сүмс','salt':'Давс','soysauce':'Шар буурцгийн сүмс'}
# Recipe ingredient quantities are not used to fabricate prices. Full product packages are purchased.
RECIPES=[
('🥟 Бууз','Махтай',4,75,['flour','beef','onion','salt'],'Гурил зуурч амраана. Махаа жижиглэн татаж сонгино, давстай холино. Шанзаа гурилд чимхэж 15–20 минут жигнэнэ.'),
('🥟 Хуушуур','Махтай',4,65,['flour','mutton','onion','oil','salt'],'Гурил зуурч, мах сонгиноор шанз хийнэ. Нимгэн элдэж хавтгай чимхээд тосонд шарна.'),
('🍜 Цуйван','Махтай',4,55,['flour','beef','onion','carrot','cabbage','oil','salt'],'Мах ногоогоо хуурч, элдсэн гурилаа хэрчин дээр нь жигнэж болгоно.'),
('🍲 Гурилтай шөл','Махтай',4,45,['flour','mutton','onion','carrot','salt'],'Мах, сонгиноо буцалгаж, хэрчсэн гурил, лууван нэмээд чанана.'),
('🥣 Банштай шөл','Махтай',4,55,['flour','beef','onion','salt'],'Махтай жижиг банш чимхэж, шөлөнд чанаж болгоно.'),
('🍚 Будаатай хуурга','Махтай',3,35,['rice','beef','onion','carrot','oil','salt'],'Будаагаа агшааж, мах ногоотойгоо хуурч холино.'),
('🍗 Тахиатай будаа','Махтай',3,40,['chicken','rice','onion','carrot','oil','salt'],'Тахианы махыг болгож, ногоотой хуурч будаатай холино.'),
('🥘 Гахайн махтай ногооны хуурга','Махтай',3,40,['pork','onion','carrot','pepper','oil','soysauce'],'Гахайн мах, ногоогоо хэрчиж сайтар болтол хуурна.'),
('🍝 Гахайн махтай гоймон','Махтай',3,35,['pork','noodle','onion','tomatosauce','oil'],'Гоймон чанаж, гахайн махтай сүмс бэлтгэн холино.'),
('🍳 Өндөгтэй будаа','Цагаан хоолтон',2,25,['egg','rice','onion','oil','salt'],'Будаагаа агшааж, өндөг сонгинотой хуурна.'),
('🥔 Төмсний хуурга','Веган',2,30,['potato','onion','oil','salt'],'Төмс сонгиноо хэрчээд тосонд болтол хуурна.'),
('🥬 Ногоотой шөл','Веган',3,35,['potato','carrot','onion','cabbage','salt'],'Ногоогоо хэрчиж буцалсан усанд зөөлөртөл чанана.'),
('🥟 Ногоотой бууз','Веган',3,65,['flour','potato','carrot','onion','salt'],'Гурил зуурч, жижиглэсэн ногоогоор шанз бэлтгээд жигнэнэ.'),
('🥟 Ногоотой хуушуур','Веган',3,60,['flour','potato','carrot','onion','oil','salt'],'Ногооны шанзаа гурилд хавчуулж тосонд шарна.'),
('🍚 Ногоотой будаа','Веган',3,30,['rice','carrot','onion','oil','salt'],'Будаагаа агшааж, хуурсан ногоотой холино.'),
('🥣 Гурвалжин будаатай ногоо','Веган',3,30,['buckwheat','carrot','onion','oil','salt'],'Гурвалжин будааг чанаж хуурсан ногоотой холино.'),
('🍲 Өндөгтэй ногооны шөл','Цагаан хоолтон',2,30,['egg','potato','carrot','onion','salt'],'Ногоогоо чанаж өндөг нэмэн болгоно.'),
('🥪 Хиамтай талх','Махтай',2,10,['bread','sausage','cucumber'],'Талх, хиам, өргөст хэмхээр сэндвич хийнэ.'),
]

def fmt(x):return f'₮{int(x):,}'
def options(key):return P[P.user_category==KEY[key]].sort_values('price_mnt')
def show_product(r):
 st.markdown(f"**{r['name']}** — {fmt(r['price_mnt'])} · [Номин дээр нээх]({r['url']})")
st.title('🌷 Хэмнэлттэй сагс 🛒')
st.caption('💗 Номин дэлгүүрээс төсөвтөө тохирсон амттай сонголтоо олоорой!')
with st.sidebar:
 st.header('Миний сонголт')
 budget=st.number_input('Өнөөдөр хэдэн төгрөг зарцуулах вэ?',min_value=1000,max_value=1000000,value=50000,step=1000)
 diet=st.selectbox('Хоолны сонголт',['Бүгд','Махтай','Цагаан хоолтон','Веган'])
 mode=st.radio('Юу авах вэ?',['🍲 Хоол','🍬 Амттан','🥤 Ундаа','🛒 Бүх бүтээгдэхүүн'])
 st.caption(f'🌼 Бараа: {len(P)} / {len(raw)}')

a,b,c=st.columns(3);a.metric('Төсөв',fmt(budget));b.metric('Баталгаажсан бүтээгдэхүүн',len(P));c.metric('Жор',len(RECIPES))
if P.empty:
 st.error('Одоогоор баталгаажсан үнэ алга. Эхлээд Cursor терминалд `python scrape_products.py` ажиллуулж, data/products.csv-г шалгаарай. Үнэ зохиож харуулахгүй.')
 st.dataframe(raw[['user_category','url','status']],hide_index=True,use_container_width=True)
elif mode=='🍲 Хоол':
 st.subheader('Монгол болон бусад хоолны санаанууд')
 show_missing=st.checkbox('Орц нь дутуу жоруудыг ч харуулах',value=True)
 dishes=[]
 for title,tag,serves,mins,keys,method in RECIPES:
  if diet=='Веган' and tag!='Веган':continue
  if diet=='Цагаан хоолтон' and tag=='Махтай':continue
  if diet=='Махтай' and tag!='Махтай':continue
  chosen={k:options(k) for k in keys}
  missing=[k for k,opts in chosen.items() if opts.empty]
  total=sum(float(opts.iloc[0].price_mnt) for opts in chosen.values() if not opts.empty)
  if missing and not show_missing:continue
  if not missing and total>budget:continue
  dishes.append((bool(missing),total,title,tag,serves,mins,chosen,missing,method))
 for missing_flag,total,title,tag,serves,mins,chosen,missing,method in sorted(dishes,key=lambda x:(x[0],x[1])):
  with st.expander(f'{title} · '+(f'⚠️ {len(missing)} орц дутуу' if missing else fmt(total))):
   st.caption(f'{tag} · {serves} хүн · ~{mins} мин')
   if missing:st.warning('Бүх орцын үнэ бүрдээгүй учраас энэ жорыг төсөвт багтана гэж батлах боломжгүй.')
   else:
    c1,c2=st.columns(2);c1.metric('Сагсны нийт үнэ',fmt(total));c2.metric('Үлдэх мөнгө',fmt(budget-total))
   for k,opts in chosen.items():
    if opts.empty:st.write(f'❌ {KEY[k]} — баталгаажсан бүтээгдэхүүн алга')
    else:
     choice=opts.iloc[0];st.markdown(f"✅ **{KEY[k]}**: {choice['name']} — {fmt(choice.price_mnt)} · [Барааны хуудас]({choice.url})")
   st.write('**Хийх арга:**',method)
 if not dishes:st.warning('Энэ төсөв болон хоолны сонголтод бүрэн тохирох жор олдсонгүй.')
else:
 cats=({'Чипс','Жигнэмэг','Чихэр','Шоколад','Самар'} if mode=='🍬 Амттан' else {'Ус','Газтай ундаа','Тараг','Жүүс','Сүү'} if mode=='🥤 Ундаа' else set(P.user_category))
 subset=P[P.user_category.isin(cats)].copy()
 subset=subset[subset.price_mnt<=budget].sort_values('price_mnt')
 st.subheader(f'Таны төсөвт багтах бүтээгдэхүүн: {len(subset)}')
 if subset.empty:st.caption('🌸 Энэ сонголтод тохирох бараа олдсонгүй.')
 for _,r in subset.iterrows():show_product(r)
 st.download_button('Бүтээгдэхүүний CSV татах',data=subset.to_csv(index=False).encode('utf-8-sig'),file_name='nomin_products.csv',mime='text/csv')
