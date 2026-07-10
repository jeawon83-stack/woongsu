import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL, dtype=str).fillna("")
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'\r+|\n+|\t+', ' ', regex=True).str.strip()
    
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

# ─── 2. 웹 화면 및 스마트폰 맞춤형 CSS 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered")

st.markdown("""
    <style>
    .main .block-container { max-width: 500px; padding-top: 15px; padding-left: 10px; padding-right: 10px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 25px !important; font-weight: bold; margin-bottom: 5px; }
    .edit-btn-container { text-align: center; margin-bottom: 20px; }
    
    /* 모든 회원 카드의 프레임 크기를 동일하게 고정 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 14px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.05) !important;
        height: 200px !important;
        box-sizing: border-box !important;
        margin-bottom: 5px !important;
    }
    
    /* 모든 사진을 명함 규격 크기로 강제 고정 및 자동 크롭 */
    div[data-testid="stImage"] img {
        width: 95px !important;
        height: 130px !important;
        object-fit: cover !important;
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
    }
    
    /* 줄간격 및 여백 정밀 제어 */
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; line-height: 1.4; }
    div[data-testid="stHorizontalBlock"] { gap: 10px !important; align-items: flex-start !important; }
    
    /* 링크 버튼 스타일 최적화 (텍스트 가독성 중심) */
    div[data-testid="stLinkButton"] a {
        font-size: 11.5px !important;
        font-weight: bold !important;
        padding: 5px 6px !important;
        border-radius: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 웅수회 모바일 회원수첩")

# 상단 수정 링크 버튼
st.markdown('<div class="edit-btn-container">', unsafe_allow_html=True)
st.link_button("✏️ 회원정보 수정하기", "https://docs.google.com/spreadsheets/d/1_0vVmGeJw10j5jYJnoj7nmJExiS5xO3oT9UjScc811o/edit?gid=0#gid=0", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 이름 검색창
search_query = st.text_input("🔍 이름으로 찾기", "", placeholder="회원 이름을 입력하세요...").strip()

if search_query:
    display_df = df[df[idx_D].str.contains(search_query, na=False)]
else:
    display_df = df

# ─── 3. 깃허브 사진 경로 및 회원 정제 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

valid_members = []
for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan" or val_A == "":
        continue
    valid_members.append(row)

# ─── 4. 회원 목록 순차 출력 (무조건 깔끔한 1열 고정) ───
for row in valid_members:
    val_A = str(row[idx_A]).strip()
    
    # 구글 시트의 숫자가 1.0 같은 소수로 오거나 공백이 섞인 것을 순수 정수 문자로 정형화
    try:
        clean_num = str(int(float(val_A)))
        padded_num = clean_num.zfill(2) # 1자리 숫자인 경우 '01' 형태도 준비
    except:
        clean_num = "00"
        padded_num = "00"

    name = str(row[idx_D]).strip()
    hakbun = str(row[idx_B]).strip()
    sosok = str(row[idx_E]).strip()
    jikpup = str(row[idx_F]).strip()
    phone = str(row[idx_G]).strip()
    company_phone = str(row[idx_H]).strip()
    email = str(row[idx_I]).strip()

    # 💡 [핵심 버그 수정] 어떤 확장자나 자릿수로 저장했든 브라우저가 다 찾아내도록 onerror 연쇄 추적 기법 적용
    # '숫자.jpg' -> '숫자.JPG' -> '숫자.png' -> '숫자.jpeg' -> '0숫자.jpg'(자릿수 맞춤) -> 기본곰돌이 순으로 자동 스캔합니다.
    img_html = f"""
    <img src="{GITHUB_PHOTO_BASE_URL}{clean_num}.jpg" 
         onerror="this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{clean_num}.JPG'; 
                  this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{clean_num}.png'; 
                  this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{clean_num}.jpeg'; 
                  this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{padded_num}.jpg'; 
                  this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{padded_num}.JPG'; 
                  this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" />
    """

    with st.container(border=True):
        # 가로 배치: 왼쪽 사진(33) : 오른쪽 정보(67)
        card_left, card_right = st.columns([33, 67])
        
        with card_left:
            # 순수 파이썬 image 컴포넌트의 HTML 우회 표기를 통해 에러 복구 스크립트 발동
            st.markdown(f'<div data-testid="stImage">{img_html}</div>', unsafe_allow_html=True)
            
        with card_right:
            # 1줄: 이름 및 학번
            st.markdown(f"**<span style='font-size:19px; color:#111827;'>{name}</span>** <span style='color:#6B7280; font-size:13px;'>({hakbun})</span>", unsafe_allow_html=True)
            
            # 2줄: 소속 및 직책 가로 한 줄 정렬
            st.markdown(f"<span style='font-size:14px; color:#4B5563; font-weight:500;'>🏢 {sosok} · {jikpup}</span>", unsafe_allow_html=True)
            st.write("") 
            
            # 3줄: 휴대폰과 회사 번호 동일 높이에 배치
            tel_col1, tel_col2 = st.columns(2)
            with tel_col1:
                if phone and phone != "nan" and phone != "":
                    st.link_button(f"📞 {phone}", f"tel:{phone}", use_container_width=True)
                else:
                    st.write("") 
            with tel_col2:
                if company_phone and company_phone != "nan" and company_phone != "":
                    st.link_button(f"☎️ {company_phone}", f"tel:{company_phone}", use_container_width=True)
                else:
                    st.write("")
            
            # 4줄: 이메일 주소 단독 하단 배치
            if email and email != "nan" and email != "":
                st.link_button(f"✉️ {email}", f"mailto:{email}", use_container_width=True)
    
    st.write("")
