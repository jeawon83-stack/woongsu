import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL, dtype=str).fillna("")
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'\r+|\n+', ' ', regex=True).str.strip()
    
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

# ─── 2. 웹 화면 및 카드 프레임 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 26px !important; font-weight: bold; margin-bottom: 25px; }
    
    /* 모든 테두리 카드의 세로 높이를 강제로 완전 일치 고정 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 12px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04) !important;
        height: 195px !important;
        box-sizing: border-box !important;
    }
    
    /* 💡 [핵심 추가] 어떠한 사진이 들어와도 00번 이미지 규격(가로 85px, 세로 115px)으로 고정 및 강제 크롭 */
    div[data-testid="stImage"] img {
        width: 85px !important;
        height: 115px !important;
        object-fit: cover !important; /* 비율 유지하며 사각형 틀에 맞춤, 넘치는 부분 자동 컷 */
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
    }
    
    /* 컴포넌트 간 불필요한 여백 최소화 */
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; line-height: 1.3; }
    div[data-testid="stHorizontalBlock"] { gap: 6px !important; }
    
    /* 버튼 폰트 및 패딩 모바일 최적화 */
    div[data-testid="stLinkButton"] a {
        font-size: 11px !important;
        padding: 4px 5px !important;
    }
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

# ─── 3. 깃허브 사진 경로 및 회원 정제 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

valid_members = []
for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan" or val_A == "":
        continue
    valid_members.append(row)

# ─── 4. 반응형 다단 레이아웃 매핑 ───
grid_cols = st.columns(3)

for col_idx, row in enumerate(valid_members):
    try:
        num_A = str(int(float(row[idx_A])))
    except:
        num_A = "00"

    name = str(row[idx_D]).strip()
    hakbun = str(row[idx_B]).strip()
    sosok = str(row[idx_E]).strip()
    jikpup = str(row[idx_F]).strip()
    phone = str(row[idx_G]).strip()
    company_phone = str(row[idx_H]).strip()
    email = str(row[idx_I]).strip()

    # 사진 확장자 정확하게 추적 매핑
    available_photos = ["00", "100", "105", "106", "107", "108", "11", "112", "17", "21", "24", "36", "47", "54"]
    if num_A in available_photos:
        if num_A in ["108", "11"]: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.JPG"
        elif num_A == "21": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.png"
        elif num_A == "24": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg"
        else: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    else:
        member_photo_url = DEFAULT_IMAGE_URL

    # 가변 반응형 열 배정
    target_col = grid_cols[col_idx % 3]
    
    with target_col:
        with st.container(border=True):
            # 대레이아웃 분할: 왼쪽 사진(35) : 오른쪽 정보(65) 강제 가로 고정
            card_left, card_right = st.columns([35, 65])
            
            with card_left:
                # 💡 안전한 내장 컴포넌트에 상단 CSS가 입혀져 00번과 100% 동일한 크기로 고정 출력됩니다.
                st.image(member_photo_url, use_container_width=True)
                
            with card_right:
                # 이름 및 학번
                st.markdown(f"**<span style='font-size:16px;'>{name}</span>** <span style='color:#6B7280; font-size:12px;'>({hakbun})</span>", unsafe_allow_html=True)
                
                # 소속과 직급 한 줄 가로 정렬
                st.markdown(f"<span style='font-size:11px; color:#4B5563;'>🏢 {sosok} · {jikpup}</span>", unsafe_allow_html=True)
                st.write("") 
                
                # 휴대폰과 회사 번호 버튼 한 줄 배치
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
                
                # 이메일 주소 하단 배치
                if email and email != "nan" and email != "":
                    st.link_button(f"✉️ {email}", f"mailto:{email}", use_container_width=True)
        
        st.write("")
