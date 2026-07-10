import streamlit as st
import pandas as pd
import html

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

# ─── 2. 웹 화면 및 반응형 GRID CSS 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 26px !important; font-weight: bold; margin-bottom: 25px; }
    
    /* 💡 [반응형 조절 핵심] 스마트폰(좁은 너비)에선 1줄, 화면이 넓어지면 2줄, 3줄로 자동 정렬 */
    .member-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 16px;
        width: 100%;
    }
    
    /* 모든 카드의 크기와 높이를 100% 동일하게 고정 */
    .member-card {
        display: flex !important;
        flex-direction: row !important;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04);
        height: 180px !important; /* 모든 카드의 세로 길이를 완벽히 통일 */
        box-sizing: border-box;
    }
    
    /* 사진 크기 고정 및 왜곡 방지 크롭 기법 */
    .photo-box {
        flex: 0 0 85px !important;
        margin-right: 14px;
        height: 115px;
    }
    .photo-box img {
        width: 85px !important;
        height: 115px !important;
        object-fit: cover !important;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    
    .info-box {
        flex: 1;
        min-width: 0;
    }
    .info-name { font-size: 16px; font-weight: bold; color: #111827; margin-bottom: 3px; }
    .info-sub { font-size: 11px; color: #4B5563; margin-bottom: 6px; line-height: 1.3; }
    
    /* 전화번호 좌우 배치를 위한 가로 정렬 플렉스 박스 */
    .tel-row {
        display: flex;
        gap: 6px;
        margin-bottom: 5px;
    }
    
    /* 실제 연락처 텍스트가 들어가는 콤팩트 버튼 디자인 */
    .btn-link {
        flex: 1;
        display: block;
        text-decoration: none !important;
        font-size: 10.5px;
        font-weight: 600;
        padding: 5px 4px;
        border-radius: 6px;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        box-sizing: border-box;
    }
    .btn-phone { background-color: #E0F2FE; color: #0369A1 !important; border: 1px solid #BAE6FD; }
    .btn-company { background-color: #F3F4F6; color: #4B5563 !important; border: 1px solid #E5E7EB; }
    .btn-email { background-color: #DCFCE7; color: #15803D !important; border: 1px solid #BBF7D0; width: 100%; }
    .btn-empty { border: none !important; background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 웅수회 모바일 회원수첩")

# 이름 검색창 (중앙 정렬)
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

# ─── 4. 회원 목록 생성 및 출력 (반응형 GRID 결합) ───
cards_html = '<div class="member-grid">'

for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan" or val_A == "":
        continue
        
    try:
        num_A = str(int(float(val_A)))
    except:
        num_A = "00"

    # 특수문자로 인해 HTML 구조가 깨지는 버그를 원천 차단하기 위한 안전 처리(Escape)
    name = html.escape(str(row[idx_D]).strip())
    hakbun = html.escape(str(row[idx_B]).strip())
    sosok = html.escape(str(row[idx_E]).strip())
    jikpup = html.escape(str(row[idx_F]).strip())
    phone = html.escape(str(row[idx_G]).strip())
    company_phone = html.escape(str(row[idx_H]).strip())
    email = html.escape(str(row[idx_I]).strip())

    # 사진 확장자 자동 추적 예외처리
    available_photos = ["00", "100", "105", "106", "107", "108", "11", "112", "17", "21", "24", "36", "47", "54"]
    if num_A in available_photos:
        if num_A in ["108", "11"]: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.JPG"
        elif num_A == "21": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.png"
        elif num_A == "24": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg"
        else: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    else:
        member_photo_url = DEFAULT_IMAGE_URL

    # 가로정렬 조건에 맞춘 전화번호 버튼 쌍 조립 (높이 균일화 보장 포함)
    phone_btn_html = ""
    if phone and phone != "nan":
        phone_btn_html += f'<a href="tel:{phone}" class="btn-link btn-phone">📞 {phone}</a>'
    else:
        phone_btn_html += '<div class="btn-link btn-empty"></div>'
        
    if company_phone and company_phone != "nan":
        phone_btn_html += f'<a href="tel:{company_phone}" class="btn-link btn-company">☎️ {company_phone}</a>'
    else:
        phone_btn_html += '<div class="btn-link btn-empty"></div>'

    # 이메일 버튼 조립
    email_btn_html = ""
    if email and email != "nan":
        email_btn_html = f'<a href="mailto:{email}" class="btn-link btn-email">✉️ {email}</a>'

    # 하나의 반응형 그리드 뼈대 안에 완성형 카드 정보를 한 장씩 누적
    cards_html += f"""
    <div class="member-card">
        <div class="photo-box">
            <img src="{member_photo_url}" 
                 onerror="this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" />
        </div>
        <div class="info-box">
            <div class="info-name">{name} <span style="font-size:12px; color:#6B7280; font-weight:normal;">({hakbun})</span></div>
            <div class="info-sub">🏢 {sosok} · {jikpup}</div>
            <div class="tel-row">
                {phone_btn_html}
            </div>
            {email_btn_html}
        </div>
    </div>
    """

cards_html += '</div>'

# ⚠️ 파이썬의 문자열 치환 안전 처리가 완비된 대형 반응형 GRID 블록을 단 한 번에 인쇄합니다.
st.markdown(cards_html, unsafe_allow_html=True)
