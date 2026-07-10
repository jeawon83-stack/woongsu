import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL)
    
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

# ─── 2. 웹 화면 및 반응형 CSS 스타일 설정 ───
# 전체 화면을 하나로 묶고 모바일과 PC 모두 수용하는 순수 CSS Grid 시스템을 적용합니다.
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 26px !important; font-weight: bold; margin-bottom: 25px; }
    
    /* 💡 [누락 방지 핵심] 컴퓨터/태블릿에서는 다단(2~3줄), 스마트폰에서는 1줄로 예외 없이 전체 행을 무조건 출력 */
    .member-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
        gap: 16px;
        width: 100%;
    }
    
    /* 카드 디자인: 무조건 왼쪽(사진), 오른쪽(정보) 구조 강제 고정 */
    .member-card {
        display: flex !important;
        flex-direction: row !important; /* 가로 정렬 고정 */
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04);
        height: 155px;
        box-sizing: border-box;
    }
    .photo-box {
        flex: 0 0 85px !important; /* 사진 크기 고정 */
        margin-right: 14px;
    }
    .photo-box img {
        width: 85px;
        height: 120px;
        object-fit: cover;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    .info-box {
        flex: 1;
        min-width: 0;
    }
    .info-name { font-size: 17px; font-weight: bold; color: #111827; margin-bottom: 2px; }
    .info-sub { font-size: 12px; color: #4B5563; margin-bottom: 6px; line-height: 1.4; }
    
    /* 실제 번호와 주소가 완전히 노출되는 콤팩트 버튼 */
    .btn-link {
        display: block;
        text-decoration: none !important;
        font-size: 11px;
        font-weight: 600;
        padding: 5px 8px;
        border-radius: 6px;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        text-align: center;
    }
    .btn-phone { background-color: #E0F2FE; color: #0369A1 !important; }
    .btn-company { background-color: #F3F4F6; color: #4B5563 !important; }
    .btn-email { background-color: #DCFCE7; color: #15803D !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 웅수회 모바일 회원수첩")

# 이름 검색창 (Streamlit 내장 컬럼 기능을 최소화하여 검색창 위치만 정렬)
left_space, search_col, right_space = st.columns([1, 4, 1])
with search_col:
    search_query = st.text_input("🔍 이름으로 찾기", "", placeholder="회원 이름을 입력하세요...")

# 검색어 필터링
if search_query:
    display_df = df[df[idx_D].astype(str).str.contains(search_query, na=False)]
else:
    display_df = df

# ─── 3. 깃허브 사진 경로 설정 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

# ─── 4. 회원 목록 생성 및 출력 ───
# 전체 회원을 하나의 그리드 컨테이너 안에 순서대로 쏟아부어 모바일 누락을 완벽히 해결합니다.
cards_html = '<div class="member-grid">'

for index, row in display_df.iterrows():
    if pd.isna(row[idx_A]):
        continue
        
    try:
        num_A = str(int(float(row[idx_A])))
    except:
        continue

    # 데이터 문자열 정리
    name = str(row[idx_D]).strip()
    hakbun = str(row[idx_B]).strip()
    sosok = str(row[idx_E]).strip()
    jikpup = str(row[idx_F]).strip()
    
    phone = str(row[idx_G]).strip() if pd.notna(row[idx_G]) else ""
    company_phone = str(row[idx_H]).strip() if pd.notna(row[idx_H]) else ""
    email = str(row[idx_I]).strip() if pd.notna(row[idx_I]) else ""

    # 버튼 구성 (실제 주소 및 번호 노출)
    buttons_html = ""
    if phone and phone != "nan" and phone != "":
        buttons_html += f'<a href="tel:{phone}" class="btn-link btn-phone">📞 휴대폰: {phone}</a>'
    if company_phone and company_phone != "nan" and company_phone != "":
        buttons_html += f'<a href="tel:{company_phone}" class="btn-link btn-company">☎️ 회사: {company_phone}</a>'
    if email and email != "nan" and email != "":
        buttons_html += f'<a href="mailto:{email}" class="btn-link btn-email">✉️ {email}</a>'

    # 하나의 텍스트 안에서 좌측 사진 박스와 우측 정보 박스를 CSS로 완전 통제
    cards_html += f"""
    <div class="member-card">
        <div class="photo-box">
            <img src="{GITHUB_PHOTO_BASE_URL}{num_A}.jpg" 
                 onerror="this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.JPG'; 
                          this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.png'; 
                          this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg'; 
                          this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" />
        </div>
        <div class="info-box">
            <div class="info-name">{name} <span style="font-size:13px; color:#6B7280; font-weight:normal;">({hakbun})</span></div>
            <div class="info-sub">
                <b>소속</b> : {sosok}<br>
                <b>직급</b> : {jikpup}
            </div>
            <div>
                {buttons_html}
            </div>
        </div>
    </div>
    """

cards_html += '</div>'

# ⚠️ Streamlit의 간섭을 완전히 차단하고 준비된 반응형 카드를 한 번에 화면에 인쇄합니다.
st.markdown(cards_html, unsafe_allow_html=True)
