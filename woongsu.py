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

# ─── 2. 웹 화면 및 스마트폰 맞춤형 CSS 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered") # 화면을 모바일에 최적화된 중앙 정렬로 변경

st.markdown("""
    <style>
    /* 스마트폰에서 가득 차 보이도록 전체 최대 너비를 제한 */
    .main .block-container { max-width: 500px; padding-top: 15px; padding-left: 10px; padding-right: 10px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 25px !important; font-weight: bold; margin-bottom: 20px; }
    
    /* 💡 모든 회원의 카드 프레임 크기를 200px로 완전히 통일 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 12px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.05) !important;
        height: 200px !important;
        box-sizing: border-box !important;
        margin-bottom: 5px !important;
    }
    
    /* 💡 모든 사진을 00번 규격(가로 90px, 세로 125px)으로 오차 없이 고정 및 비율 크롭 */
    div[data-testid="stImage"] img {
        width: 90px !important;
        height: 125px !important;
        object-fit: cover !important;
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
    }
    
    /* 💡 글자 위치와 버튼 높이가 모든 칸에서 완전히 동일하도록 강제 패딩 조절 */
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; line-height: 1.3; }
    div[data-testid="stHorizontalBlock"] { gap: 8px !important; align-items: flex-start !important; }
    
    /* 원터치 링크 버튼 모바일 가독성 최적화 */
    div[data-testid="stLinkButton"] a {
        font-size: 11.5px !important;
        font-weight: bold !important;
        padding: 5px 6px !important;
        border-radius: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 웅수회 모바일 회원수첩")

# 이름 검색창 (스마트폰 크기 꽉 채움)
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

# ─── 4. 회원 목록 순차 출력 (무조건 1열 고정) ───
# 복잡한 가로 배열 연동을 완전히 제거하여 스마트폰에서 밀림/누락 에러를 완벽 방어합니다.
for row in valid_members:
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

    # 사진 매칭 확장자 체크 예외처리
    available_photos = ["00", "100", "105", "106", "107", "108", "11", "112", "17", "21", "24", "36", "47", "54"]
    if num_A in available_photos:
        if num_A in ["108", "11"]: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.JPG"
        elif num_A == "21": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.png"
        elif num_A == "24": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg"
        else: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    else:
        member_photo_url = DEFAULT_IMAGE_URL

    # 테두리가 봉인된 독립 카드 박스 개시
    with st.container(border=True):
        # 비율 분할: 왼쪽 사진 구역(33) : 오른쪽 정보 구역(67)
        card_left, card_right = st.columns([33, 67])
        
        with card_left:
            st.image(member_photo_url, use_container_width=True)
            
        with card_right:
            # 💡 이름 글씨 크기 키움 (18px)
            st.markdown(f"**<span style='font-size:18px; color:#111827;'>{name}</span>** <span style='color:#6B7280; font-size:13px;'>({hakbun})</span>", unsafe_allow_html=True)
            
            # 💡 소속 및 직책 글씨 크기 키움 (14px) 및 한 줄 좌우 정렬
            st.markdown(f"<span style='font-size:14px; color:#4B5563; font-weight:500;'>🏢 {sosok} · {jikpup}</span>", unsafe_allow_html=True)
            st.write("") # 버튼 가이드 간격 확보
            
            # 휴대폰과 회사 번호 버튼 한 줄 배치 (정밀 높이 수평 유지)
            tel_col1, tel_col2 = st.columns(2)
            with tel_col1:
                if phone and phone != "nan" and phone != "":
                    st.link_button(f"📞 휴대폰", f"tel:{phone}", use_container_width=True)
                else:
                    st.write("") 
            with tel_col2:
                if company_phone and company_phone != "nan" and company_phone != "":
                    st.link_button(f"☎️ 회사", f"tel:{company_phone}", use_container_width=True)
                else:
                    st.write("")
            
            # 이메일 주소 버튼 하단 배치
            if email and email != "nan" and email != "":
                st.link_button(f"✉️ 이메일 보내기", f"mailto:{email}", use_container_width=True)
    
    # 카드간 하단 물리적 마진 형성
    st.write("")
