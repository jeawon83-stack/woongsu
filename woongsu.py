import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    # 데이터 파괴를 방지하기 위해 모든 셀 데이터를 문자열 취급하고 줄바꿈 기호를 사전에 박멸합니다.
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
    
    /* 💡 [조건 1] HTML 없이 모든 테두리 카드의 세로 높이를 강제로 완전 일치 고정 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 12px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04) !important;
        height: 195px !important;
        box-sizing: border-box !important;
    }
    
    /* 컴포넌트 간 불필요한 공백 제거 */
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

# ─── 4. [완벽 반응형] 1줄 ~ 3줄 크기 가변 제어 로직 ───
# st.columns([1,1,1]) 구조는 컴퓨터 화면용이며, 
# 스마트폰 세로 모드 진입 시 브라우저 너비를 감지해 우측 열들이 알아서 아래 줄로 흘러내려가므로 
# 스마트폰에서는 순서대로 완벽한 1줄 정렬이 되고, PC에서는 3줄 다단 정렬이 완벽하게 이루어집니다!
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

    # 사진 확장자 추적 매핑
    available_photos = ["00", "100", "105", "106", "107", "108", "11", "112", "17", "21", "24", "36", "47", "54"]
    if num_A in available_photos:
        if num_A in ["108", "11"]: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.JPG"
        elif num_A == "21": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.png"
        elif num_A == "24": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg"
        else: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    else:
        member_photo_url = DEFAULT_IMAGE_URL

    # 반응형 가변 열 배정
    target_col = grid_cols[col_idx % 3]
    
    with target_col:
        # 순수 파이썬 독립 컨테이너 개시 (HTML 파괴 원천 불가)
        with st.container(border=True):
            # 대레이아웃 분할: 왼쪽 사진(35) : 오른쪽 정보(65) 강제 가로 고정
            card_left, card_right = st.columns([35, 65])
            
            with card_left:
                # 00번 사진 비율에 맞춰 모든 이미지를 균일화하여 출력하는 내장 컴포넌트
                st.image(member_photo_url, use_container_width=True, fallback=DEFAULT_IMAGE_URL)
                
            with card_right:
                # 이름 및 학번
                st.markdown(f"**<span style='font-size:16px;'>{name}</span>** <span style='color:#6B7280; font-size:12px;'>({hakbun})</span>", unsafe_allow_html=True)
                
                # 💡 [요청조건 1] 소속과 직급을 한 줄에 가로로 이쁘게 표현
                st.markdown(f"<span style='font-size:11px; color:#4B5563;'>🏢 {sosok} · {jikpup}</span>", unsafe_allow_html=True)
                st.write("") # 버튼 분리를 위한 미세 간격
                
                # 💡 [요청조건 2] 휴대폰과 회사 번호 버튼을 한 줄에 좌우로 나란히 배치
                tel_col1, tel_col2 = st.columns(2)
                with tel_col1:
                    if phone and phone != "nan" and phone != "":
                        st.link_button(f"📞 {phone}", f"tel:{phone}", use_container_width=True)
                    else:
                        st.write("") # 칸 균형 유지를 위한 빈 구역 확보
                with tel_col2:
                    if company_phone and company_phone != "nan" and company_phone != "":
                        st.link_button(f"☎️ {company_phone}", f"tel:{company_phone}", use_container_width=True)
                    else:
                        st.write("")
                
                # 💡 [요청조건 3] 그 바로 밑에 이메일 주소를 단독 가로로 배치
                if email and email != "nan" and email != "":
                    st.link_button(f"✉️ {email}", f"mailto:{email}", use_container_width=True)
        
        # 하단 카드 정돈용 간격 형성
        st.write("")
