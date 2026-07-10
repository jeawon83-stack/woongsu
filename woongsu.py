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

# ─── 2. 웹 화면 및 스타일 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 26px !important; font-weight: bold; margin-bottom: 25px; }
    
    /* 카드 외곽 프레임 정돈 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 12px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04) !important;
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

# ─── 4. 회원 목록 출력 (파이썬 제어 다단 배치 기법) ───
# 실제 유효한 회원 리스트만 먼저 정제합니다.
valid_members = []
for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan" or val_A == "":
        continue
    valid_members.append(row)

# PC/태블릿 크기를 위해 한 줄에 3개씩 분할 선언 (모바일 브라우저 진입 시 3개의 열이 위에서 아래로 순서대로 정렬되므로 누락 차단!)
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

    # 💡 [사진 복구 핵심] 확장자가 꼬였거나 사진이 없는 경우를 파이썬 내에서 사전 감지 후 안전한 대체 주소 주입
    # 깃허브 저장소에 등록해두신 특정 번호들만 매칭하고 나머지는 안전하게 00.jpg로 강제 매핑합니다.
    # (현재 깃허브 photos 폴더에 업로드 완료된 사진 번호들 목록입니다)
    available_photos = ["00", "100", "105", "106", "107", "108", "11", "112", "17", "21", "24", "36", "47", "54"]
    
    if num_A in available_photos:
        # 깃허브 화면 확인 결과 108번과 11번은 대문자 JPG, 21번은 png, 24번은 jpeg 형식이므로 이에 맞춤 매핑
        if num_A in ["108", "11"]:
            member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.JPG"
        elif num_A == "21":
            member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.png"
        elif num_A == "24":
            member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg"
        else:
            member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    else:
        # 폴더에 사진이 없는 번호는 무조건 00.jpg 주소 적용
        member_photo_url = DEFAULT_IMAGE_URL

    # 지정된 열(0, 1, 2)에 순서대로 차곡차곡 카드를 분배
    target_col = grid_cols[col_idx % 3]
    
    with target_col:
        with st.container(border=True):
            # 카드 내부 분할: 왼쪽(사진 3.5) / 오른쪽(정보 6.5) 강제 가로 정렬
            card_left, card_right = st.columns([35, 65])
            
            with card_left:
                st.image(member_photo_url, use_container_width=True)
                
            with card_right:
                st.markdown(f"**<span style='font-size:16px;'>{name}</span>** <span style='color:#6B7280; font-size:12px;'>({hakbun})</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-size:12px; color:#4B5563; line-height:1.3;'><b>소속</b>: {sosok}<br><b>직급</b>: {jikpup}</span>", unsafe_allow_html=True)
                
                # 원터치 다이렉트 버튼 링크 구성
                if phone and phone != "nan":
                    st.link_button(f"📞 휴대폰: {phone}", f"tel:{phone}", use_container_width=True)
                if company_phone and company_phone != "nan":
                    st.link_button(f"☎️ 회사: {company_phone}", f"tel:{company_phone}", use_container_width=True)
                if email and email != "nan":
                    st.link_button(f"✉️ 이메일: {email}", f"mailto:{email}", use_container_width=True)
        
        # 카드 간 하단 여백 형성
        st.write("")
