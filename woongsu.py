import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL, dtype=str).fillna("")
    
    idx_A = df.columns[0] # 번호 (A)
    idx_B = df.columns[1] # 학번 (B)
    idx_D = df.columns[3] # 이름 (D)
    idx_E = df.columns[4] # 소속 (E)
    idx_F = df.columns[5] # 직급 (F)
    idx_G = df.columns[6] # 전화번호 1 (G)
    idx_H = df.columns[7] # 전화번호(회사) (H)
    idx_I = df.columns[8] # 이메일 (I)

except Exception as e:
    st.error("구글 시트를 불러오는 중 오류가 발생했습니다. URL을 확인해주세요.")
    st.stop()

# ─── 2. 웹 화면 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 1000px; padding-top: 20px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 26px !important; font-weight: bold; margin-bottom: 25px; }
    
    /* 카드 디자인 테두리 효과 설정 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 10px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 웅수회 모바일 회원수첩")

# 이름 검색창
left_space, search_col, right_space = st.columns([1, 4, 1])
with search_col:
    search_query = st.text_input("🔍 이름으로 찾기", "", placeholder="회원 이름을 입력하세요...").strip()

# 검색어 필터링
if search_query:
    display_df = df[df[idx_D].str.contains(search_query, na=False)]
else:
    display_df = df

# ─── 3. 깃허브 사진 경로 설정 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

# ─── 4. 회원 목록 출력 (100% 안전한 파이썬 레이아웃) ───
for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan" or val_A == "":
        continue
        
    try:
        num_A = str(int(float(val_A)))
    except:
        num_A = "00"

    name = str(row[idx_D]).strip()
    hakbun = str(row[idx_B]).strip()
    sosok = str(row[idx_E]).strip()
    jikpup = str(row[idx_F]).strip()
    phone = str(row[idx_G]).strip()
    company_phone = str(row[idx_H]).strip()
    email = str(row[idx_I]).strip()

    # 개별 컨테이너 카드 생성
    with st.container(border=True):
        # 스마트폰 최적화: 무조건 왼쪽(사진 3.5), 오른쪽(정보 6.5) 분할
        card_left, card_right = st.columns([35, 65])
        
        with card_left:
            # 💡 [해결 조치] 버전을 타는 fallback 대신 HTML 이미지 기법을 활용하여 사진 자동 대체
            img_html = f"""
            <img src="{GITHUB_PHOTO_BASE_URL}{num_A}.jpg" 
                 onerror="this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.JPG'; 
                          this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.png'; 
                          this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg'; 
                          this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" 
                 style="width:100%; height:120px; object-fit:cover; border-radius:8px; border:1px solid #E5E7EB;" />
            """
            st.markdown(img_html, unsafe_allow_html=True)
            
        with card_right:
            st.markdown(f"**<span style='font-size:16px;'>{name}</span>** <span style='color:#6B7280; font-size:12px;'>({hakbun})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:12px; color:#4B5563; line-height:1.3;'><b>소속</b>: {sosok}<br><b>직급</b>: {jikpup}</span>", unsafe_allow_html=True)
            
            # 실제 연락처 다이렉트 버튼 배치
            if phone and phone != "nan":
                st.link_button(f"📞 휴대폰: {phone}", f"tel:{phone}", use_container_width=True)
                
            if company_phone and company_phone != "nan":
                st.link_button(f"☎️ 회사: {company_phone}", f"tel:{company_phone}", use_container_width=True)
                
            if email and email != "nan":
                st.link_button(f"✉️ 이메일: {email}", f"mailto:{email}", use_container_width=True)
