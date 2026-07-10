import streamlit as st
import pandas as pd
import html

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL, dtype=str).fillna("")
    # 데이터 깨짐 방지용 정형화 전처리
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'\r+|\n+|\t+', ' ', regex=True).str.strip()
    
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

# ─── 2. 스마트폰 전용 명함첩 테두리 격자 CSS 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered")

st.markdown("""
    <style>
    .main .block-container { max-width: 480px; padding-top: 15px; padding-left: 8px; padding-right: 8px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 24px !important; font-weight: bold; margin-bottom: 5px; }
    
    .edit-btn-container { text-align: center; margin-bottom: 20px; }
    
    /* 💡 전체 회원첩 컨테이너 (바깥 파란색 실선 테두리) */
    .notebook-container {
        border: 2px solid #2B579A;
        border-radius: 4px;
        background-color: #ffffff;
        width: 100%;
        box-sizing: border-box;
    }
    
    /* 💡 개별 회원 명함 블록 (하단 테두리 실선) */
    .member-row {
        display: flex;
        border-bottom: 2px solid #2B579A;
        width: 100%;
        height: 140px; /* 명함첩 규격 고정 */
        box-sizing: border-box;
    }
    .member-row:last-child {
        border-bottom: none;
    }
    
    /* 💡 좌측 사진 영역 (우측 실선 테두리) */
    .photo-area {
        flex: 0 0 100px;
        border-right: 1px solid #2B579A;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #fafafa;
        overflow: hidden;
    }
    .photo-area img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* 💡 우측 정보 격자 영역 */
    .info-grid {
        flex: 1;
        display: flex;
        flex-direction: column;
        height: 100%;
        font-size: 12px;
        color: #111827;
    }
    
    /* 각 행 구조 정의 */
    .row-line {
        display: flex;
        border-bottom: 1px solid #2B579A;
        align-items: center;
        box-sizing: border-box;
    }
    
    /* 이름 행 (단독 1행 배치) */
    .name-line {
        height: 35px;
        padding-left: 10px;
        background-color: #ffffff;
        font-size: 16px;
        font-weight: bold;
    }
    .name-line .hakbun {
        font-size: 13px;
        color: #6B7280;
        font-weight: normal;
        margin-left: 5px;
    }
    
    /* 소속 / 직위 2분할 행 */
    .sub-info-line {
        height: 32px;
    }
    
    /* 전화번호 격자 행 */
    .tel-line {
        height: 38px;
    }
    
    /* 이메일 행 (맨 아래) */
    .email-line {
        height: 35px;
        border-bottom: none;
    }
    
    /* 격자 내부 라벨(소속, 직위 등) 스타일 */
    .grid-label {
        flex: 0 0 45px;
        background-color: #f3f4f6;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        border-right: 1px solid #2B579A;
        font-size: 11px;
    }
    
    /* 격자 내부 실제 데이터값 스타일 */
    .grid-value {
        flex: 1;
        height: 100%;
        display: flex;
        align-items: center;
        padding-left: 8px;
        padding-right: 4px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .border-right-blue {
        border-right: 1px solid #2B579A;
    }
    
    /* 원터치 전화/이메일 클릭 링크 스타일 */
    .click-link {
        color: #0056b3 !important;
        text-decoration: none !important;
        font-weight: 500;
        width: 100%;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 웅수회 모바일 회원수첩")

# 상단 수정 링크 버튼
st.markdown('<div class="edit-btn-container">', unsafe_allow_html=True)
st.link_button("✏️ 회원정보 수정하기", "https://docs.google.com/spreadsheets/d/1_0vVmGeJw10j5jYJnoj7nmJExiS5xO3oT9UjScc811o/edit?gid=0#gid=0", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 이름 검색창
search_query = st.text_input("🔍 이름으로 찾기", "", placeholder="회원 이름을 입력하세요...").strip()

if search_query:
    display_df = df[df[idx_D].str.contains(search_query, na=False)]
else:
    display_df = df

# ─── 3. 깃허브 사진 경로 및 회원 추출 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

valid_members = []
for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan" or val_A == "":
        continue
    valid_members.append(row)

# ─── 4. 명함첩 렌더링 개시 ───
# 전체 리스트를 하나의 큰 파란색 수첩 컨테이너 구조로 감싸 출력합니다.
notebook_html = '<div class="notebook-container">'

for row in valid_members:
    try:
        num_A = str(int(float(row[idx_A])))
    except:
        num_A = "00"

    # 특수문자가 HTML 문법을 깨부수지 못하게 안전 이스케이프 가공
    name = html.escape(str(row[idx_D]).strip())
    hakbun = html.escape(str(row[idx_B]).strip())
    sosok = html.escape(str(row[idx_E]).strip())
    jikpup = html.escape(str(row[idx_F]).strip())
    phone = html.escape(str(row[idx_G]).strip())
    company_phone = html.escape(str(row[idx_H]).strip())
    email = html.escape(str(row[idx_I]).strip())

    # 사진 매칭 확장자 분기 처리
    available_photos = ["00", "100", "105", "106", "107", "108", "11", "112", "17", "21", "24", "36", "47", "54"]
    if num_A in available_photos:
        if num_A in ["108", "11"]: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.JPG"
        elif num_A == "21": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.png"
        elif num_A == "24": member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg"
        else: member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    else:
        member_photo_url = DEFAULT_IMAGE_URL

    # 원터치 전화걸기 및 이메일 링크 구조 처리
    phone_html = f'<a href="tel:{phone}" class="click-link">{phone}</a>' if phone and phone != "nan" else "-"
    company_html = f'<a href="tel:{company_phone}" class="click-link">{company_phone}</a>' if company_phone and company_phone != "nan" else "-"
    email_html = f'<a href="mailto:{email}" class="click-link">{email}</a>' if email and email != "nan" else "-"

    # 오른쪽 인쇄 예시 그림과 동일한 격자 테이블 형태 구현
    notebook_html += f"""
    <div class="member-row">
        <!-- 좌측 사진 구역 -->
        <div class="photo-area">
            <img src="{member_photo_url}" onerror="this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" />
        </div>
        
        <!-- 우측 4단 격자 정보 구역 -->
        <div class="info-grid">
            <!-- 1행: 이름 및 학번 (소속 위에 노출 조건 충족) -->
            <div class="row-line name-line">
                {name} <span class="hakbun">({hakbun})</span>
            </div>
            
            <!-- 2행: 소속 및 직위 격자 분할 -->
            <div class="row-line sub-info-line">
                <div class="grid-label">소속</div>
                <div class="grid-value border-right-blue">{sosok}</div>
                <div class="grid-label">직위</div>
                <div class="grid-value">{jikpup}</div>
            </div>
            
            <!-- 3행: TEL(회사) 및 CP(휴대폰) 격자 분할 -->
            <div class="row-line tel-line">
                <div class="grid-label">TEL</div>
                <div class="grid-value border-right-blue">{company_html}</div>
                <div class="grid-label">CP</div>
                <div class="grid-value">{phone_html}</div>
            </div>
            
            <!-- 4행: 이메일 단독 행 -->
            <div class="row-line email-line">
                <div class="grid-label">e-mail</div>
                <div class="grid-value">{email_html}</div>
            </div>
        </div>
    </div>
    """

notebook_html += '</div>'

# 최종 가공된 수첩 인쇄
st.markdown(notebook_html, unsafe_allow_html=True)
