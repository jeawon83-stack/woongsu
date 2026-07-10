import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    # 시트를 읽어올 때 모든 데이터를 문자열로 안전하게 처리하고 앞뒤 공백을 제거합니다.
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

# 화면 여백 조정 및 카드 테두리 효과를 위한 최소한의 스타일만 주입
st.markdown("""
    <style>
    .main .block-container { max-width: 1000px; padding-top: 20px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 26px !important; font-weight: bold; margin-bottom: 25px; }
    /* 개별 카드 구역 테두리 스타일 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 10px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 10px !important;
    }
    /* 버튼 텍스트 정렬 */
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

# ─── 4. 회원 목록 출력 (순수 파이썬 레이아웃) ───
# 스마트폰 누락을 해결하기 위해 강제 분할 열을 쓰지 않고, 
# 각 회원을 순수 파이썬의 독립된 테두리 박스(Container)로 감싸 아래로 차례대로 출력합니다.
for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan":
        continue
        
    try:
        # 번호 포맷팅 (소수점이 붙어있다면 제거)
        num_A = str(int(float(val_A)))
    except:
        num_A = "00"

    # 데이터 추출 및 공백 정돈
    name = str(row[idx_D]).strip()
    hakbun = str(row[idx_B]).strip()
    sosok = str(row[idx_E]).strip()
    jikpup = str(row[idx_F]).strip()
    phone = str(row[idx_G]).strip()
    company_phone = str(row[idx_H]).strip()
    email = str(row[idx_I]).strip()

    # 사진 주소 조립
    member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"

    # 하나의 독립된 카드 박스 생성 (HTML이 아니므로 절대 안 깨짐)
    with st.container(border=True):
        # 💡 [왼쪽 사진 / 오른쪽 정보] 화면 고정 분할
        card_left, card_right = st.columns([3, 7])
        
        with card_left:
            # 안전하게 Streamlit 내장 이미지 컴포넌트 사용
            st.image(member_photo_url, use_container_width=True, fallback=DEFAULT_IMAGE_URL)
            
        with card_right:
            # 회원 기본 인적사항 출력
            st.subheader(f"{name} ({hakbun})")
            st.caption(f"**소속** : {sosok} | **직급** : {jikpup}")
            
            # 실제 연락처 정보가 노출되는 터치식 다이렉트 링크 버튼 구성
            if phone and phone != "nan":
                st.link_button(f"📞 휴대폰: {phone}", f"tel:{phone}", use_container_width=True)
                
            if company_phone and company_phone != "nan":
                st.link_button(f"☎️ 회사: {company_phone}", f"tel:{company_phone}", use_container_width=True)
                
            if email and email != "nan":
                st.link_button(f"✉️ 이메일: {email}", f"mailto:{email}", use_container_width=True)
