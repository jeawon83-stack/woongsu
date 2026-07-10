import streamlit as st
import pandas as pd
import html

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
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    /* 전체 레이아웃 너비 조절 */
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    .title-area { text-align: center; margin-bottom: 25px; }
    .title-text { font-size: 26px; font-weight: bold; color: #1E3A8A; }
    
    /* [완벽 방어] 스마트폰에서는 1줄, 태블릿/PC에서는 화면 크기에 맞춰 2~3줄 자동 정렬 */
    .member-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
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
        height: 160px; /* 번호 텍스트 노출을 고려해 높이를 소폭 확장 */
        box-sizing: border-box;
    }
    .photo-box {
        flex: 0 0 85px;
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
    .info-name { font-size: 17px; font-weight: bold; color: #111827; margin-bottom: 3px; }
    .info-sub { font-size: 12px; color: #4B5563; margin-bottom: 8px; line-height: 1.4; }
    
    /* 실제 번호와 이메일 주소가 들어간 모바일 맞춤형 버튼 스타일 */
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
        text-overflow: ellipsis; /* 번호가 너무 길면 잘리도록 안전 조치 */
    }
    .btn-phone { background-color: #E0F2FE; color: #0369A1 !important; }
    .btn-company { background-color: #F3F4F6; color: #4B5563 !important; }
    .btn-email { background-color: #DCFCE7; color: #15803D !important; }
    </style>
    """, unsafe_allow_html=True)

# 상단 타이틀
st.markdown('<div class="title-area"><span class="title-text">📱 웅수회 모바일 회원수첩</span></div>', unsafe_allow_html=True)

# 이름 검색창 (스마트폰 크기에 맞춤)
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
cards_html = '<div class="member-grid">'

for index, row in display_df.iterrows():
    if pd.isna(row[idx_A]):
        continue
        
    try:
        num_A = str(int(float(row[idx_A])))
    except:
        continue

    # 💡 [핵심 교정] 데이터에 포함된 특수문자나 따옴표를 완전히 안전하게 이스케이프 처리하여 HTML 파괴 원천 차단
    name = html.escape(str(row[idx_D]).strip())
    hakbun = html.escape(str(row[idx_B]).strip())
    sosok = html.escape(str(row[idx_E]).strip())
    jikpup = html.escape(str(row[idx_F]).strip())
    
    phone = str(row[idx_G]).strip() if pd.notna(row[idx_G]) else ""
    company_phone = str(row[idx_H]).strip() if pd.notna(row[idx_H]) else ""
    email = str(row[idx_I]).strip() if pd.notna(row[idx_I]) else ""

    # 버튼 영역 생성 (실제 번호와 주소를 텍스트로 삽입)
    buttons_html = ""
    if phone and phone != "nan" and phone != "":
        buttons_html += f'<a href="tel:{phone}" class="btn-link btn-phone">📞 {phone}</a>'
    if company_phone and company_phone != "nan" and company_phone != "":
        buttons_html += f'<a href="tel:{company_phone}" class="btn-link btn-company">☎️ {company_phone}</a>'
    if email and email != "nan" and email != "":
        buttons_html += f'<a href="mailto:{email}" class="btn-link btn-email">✉️ {email}</a>'

    # 카드 HTML 구조 결합
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
            <div style="margin-top: 2px;">
                {buttons_html}
            </div>
        </div>
    </div>
    """

cards_html += '</div>'

# 안전하게 최종 통합 렌더링
st.markdown(cards_html, unsafe_allow_html=True)
