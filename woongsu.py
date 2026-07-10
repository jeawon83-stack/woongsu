import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
# 제공해주신 '웹에 게시(CSV)' 주소를 적용했습니다.
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL)
    
    # 구글 시트 열 인덱스 매핑 (A=0, B=1, C=2, D=3...)
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
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    .title-area { text-align: center; margin-bottom: 25px; }
    .title-text { font-size: 26px; font-weight: bold; color: #1E3A8A; }
    
    /* 반응형 그리드 컨테이너 */
    .member-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 16px;
        width: 100%;
    }
    
    /* 개별 회원 카드 스타일 */
    .member-card {
        display: flex;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04);
        height: 150px;
    }
    .photo-box {
        flex: 0 0 85px;
        margin-right: 12px;
    }
    .photo-box img {
        width: 85px;
        height: 115px;
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
    
    /* 버튼 스타일 */
    .btn-link {
        display: inline-flex;
        align-items: center;
        text-decoration: none !important;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 6px;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    .btn-phone { background-color: #E0F2FE; color: #0369A1 !important; }
    .btn-company { background-color: #F3F4F6; color: #4B5563 !important; }
    .btn-email { background-color: #DCFCE7; color: #15803D !important; }
    </style>
    """, unsafe_allow_html=True)

# 상단 타이틀
st.markdown('<div class="title-area"><span class="title-text">📱 웅수회 모바일 회원수첩</span></div>', unsafe_allow_html=True)

# 이름 검색창
left_space, search_col, right_space = st.columns([1, 2, 1])
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
cards_html = '<div class="member-grid">'

for index, row in display_df.iterrows():
    if pd.isna(row[idx_A]):
        continue
        
    try:
        # 소수점 제거 후 문자열로 안전하게 변환
        num_A = str(int(float(row[idx_A])))
    except:
        continue

    # 전화번호 및 이메일 문자열 처리 (공백 및 nan 제거)
    phone = str(row[idx_G]).strip() if pd.notna(row[idx_G]) else ""
    company_phone = str(row[idx_H]).strip() if pd.notna(row[idx_H]) else ""
    email = str(row[idx_I]).strip() if pd.notna(row[idx_I]) else ""

    # 버튼 생성
    buttons_html = ""
    if phone and phone != "nan" and phone != "":
        buttons_html += f'<a href="tel:{phone}" class="btn-link btn-phone">휴대폰</a>'
    if company_phone and company_phone != "nan" and company_phone != "":
        buttons_html += f'<a href="tel:{company_phone}" class="btn-link btn-company">회사</a>'
    if email and email != "nan" and email != "":
        buttons_html += f'<a href="mailto:{email}" class="btn-link btn-email">이메일</a>'

    # 카드 구조 누적
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
            <div class="info-name">{row[idx_D]} <span style="font-size:13px; color:#6B7280; font-weight:normal;">({row[idx_B]})</span></div>
            <div class="info-sub">
                <b>소속</b> : {row[idx_E]}<br>
                <b>직급</b> : {row[idx_F]}
            </div>
            <div style="margin-top: 2px;">
                {buttons_html}
            </div>
        </div>
    </div>
    """

cards_html += '</div>'

# 최종 화면 렌더링
st.markdown(cards_html, unsafe_allow_html=True)
