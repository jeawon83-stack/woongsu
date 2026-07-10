import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
# ⚠️ 본인의 구글 시트 웹 게시(CSV) 주소를 여기에 넣어주세요!
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
# 넓은 화면에서도 시원하게 보이도록 레이아웃을 'wide'로 설정합니다.
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

# 반응형 그리드 레이아웃 스타일 정의
st.markdown("""
    <style>
    /* 전체 콘텐츠 중앙 정렬 및 최대 너비 제한 (너무 퍼지는 것 방지) */
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    .title-area { text-align: center; margin-bottom: 25px; }
    .title-text { font-size: 26px; font-weight: bold; color: #1E3A8A; }
    
    /* 핵심: 반응형 그리드 컨테이너 */
    /* 화면 너비에 따라 카드가 최소 320px을 유지하며 한 줄에 1개~3개로 자동 조절됩니다. */
    .member-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 16px;
        width: 100%;
    }
    
    /* 개별 회원 카드 스타일 (무조건 좌측 사진 / 우측 정보 고정) */
    .member-card {
        display: flex;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04);
        height: 150px; /* 카드 높이를 통일하여 정렬을 깔끔하게 유지 */
    }
    .photo-box {
        flex: 0 0 85px; /* 사진 공간 너비 고정 */
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
        min-width: 0; /* 텍스트 넘침 방지 */
    }
    .info-name { font-size: 17px; font-weight: bold; color: #111827; margin-bottom: 2px; }
    .info-sub { font-size: 12px; color: #4B5563; margin-bottom: 6px; line-height: 1.4; }
    
    /* 바로 연결 버튼 스타일 */
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

# 이름 검색창 (넓은 화면을 고려하여 중앙에 적당한 크기로 배치하기 위해 컬럼 분할)
left_space, search_col, right_space = st.columns([1, 2, 1])
with search_col:
    search_query = st.text_input("🔍 이름으로 찾기", "", placeholder="회원 이름을 입력하세요...")

# 검색어 필터링 리스트
if search_query:
    display_df = df[df[idx_D].astype(str).str.contains(search_query, na=False)]
else:
    display_df = df

# ─── 3. 깃허브 사진 경로 설정 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

# ─── 4. 회원 목록 출력 (반응형 그리드 적용) ───
# 그리드 시작 태그
cards_html = '<div class="member-grid">'

for index, row in display_df.iterrows():
    if pd.isna(row[idx_A]):
        continue
        
    try:
        num_A = str(int(row[idx_A]))
    except:
        continue

    # 전화번호 및 이메일 데이터 정리
    phone = str(row[idx_G]).strip() if pd.notna(row[idx_G]) else ""
    company_phone = str(row[idx_H]).strip() if pd.notna(row[idx_H]) else ""
    email = str(row[idx_I]).strip() if pd.notna(row[idx_I]) else ""

    # 버튼 HTML 동적 생성
    buttons_html = ""
    if phone and phone != "nan":
        buttons_html += f'<a href="tel:{phone}" class="btn-link btn-phone">휴대폰</a>'
    if company_phone and company_phone != "nan":
        buttons_html += f'<a href="tel:{company_phone}" class="btn-link btn-company">회사</a>'
    if email and email != "nan":
        buttons_html += f'<a href="mailto:{email}" class="btn-link btn-email">이메일</a>'

    # 개별 회원 카드를 그리드 내부에 하나씩 축적
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

# 그리드 닫기 태그 및 렌더링
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)