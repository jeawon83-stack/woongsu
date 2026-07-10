import streamlit as st
import pandas as pd

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL, dtype=str).fillna("")
    # 안전을 위해 모든 텍스트의 줄바꿈 기호를 사전에 공백으로 전처리
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

# ─── 2. 스마트폰 전용 명함첩 테두리 격자 설정 (순수 CSS) ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered")

st.markdown("""
    <style>
    .main .block-container { max-width: 480px; padding-top: 15px; padding-left: 8px; padding-right: 8px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 24px !important; font-weight: bold; margin-bottom: 5px; }
    .edit-btn-container { text-align: center; margin-bottom: 20px; }
    
    /* 💡 순수 파이썬 테두리 박스 컴포넌트의 높이를 210px로 일치시키고 내부 격자 선을 깔끔하게 구현 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #2B579A !important;
        border-radius: 6px !important;
        padding: 0px !important; /* 내부 패딩을 없애 격자 선이 테두리에 밀착되게 설정 */
        background-color: #ffffff !important;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.05) !important;
        height: 210px !important;
        box-sizing: border-box !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }
    
    /* 좌측 사진용 정밀 왜곡 방지 프레임 설정 */
    div[data-testid="stImage"] img {
        width: 100% !important;
        height: 206px !important; /* 카드 전체 높이에 맞춤 */
        object-fit: cover !important;
        border-radius: 0px !important;
    }
    
    /* 텍스트 컴포넌트 여백 최소화 */
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; line-height: 1.3; }
    div[data-testid="stHorizontalBlock"] { gap: 0px !important; }
    
    /* 격자 내부 텍스트 및 라벨 서식 */
    .table-label {
        font-size: 11px;
        font-weight: bold;
        color: #111827;
        background-color: #F3F4F6;
        text-align: center;
        padding: 5px 2px;
        border-right: 1px solid #2B579A;
        border-bottom: 1px solid #2B579A;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .table-value {
        font-size: 12px;
        color: #111827;
        padding: 5px 6px;
        border-bottom: 1px solid #2B579A;
        height: 28px;
        display: flex;
        align-items: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .no-bottom-border { border-bottom: none !important; }
    .border-right-blue { border-right: 1px solid #2B579A !important; }
    
    /* 원터치 링크 버튼의 테두리와 배경을 투명화하여 실제 표 안의 텍스트처럼 표현 */
    div[data-testid="stLinkButton"] a {
        font-size: 12px !important;
        font-weight: bold !important;
        color: #0056b3 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
        text-align: left !important;
        justify-content: flex-start !important;
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

# ─── 4. 회원 목록 순차 출력 (순수 파이썬 Grid 구조) ───
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

    # 💡 HTML 태그 완전히 전멸시킨 순수 파이썬 컨테이너 레이아웃 가동
    with st.container(border=True):
        # 대분할: 좌측 사진 구역(30) : 우측 정보 구역(70) 연동 및 우측 실선 구분선 형성
        card_left, space_line, card_right = st.columns([30, 1, 69])
        
        with card_left:
            st.image(member_photo_url, use_container_width=True)
            
        with space_line:
            # 좌측 사진과 우측 격자 사이를 단단히 채워주는 세로 파란 실선 기둥 효과
            st.markdown('<div style="border-right: 2px solid #2B579A; height: 210px;"></div>', unsafe_allow_html=True)
            
        with card_right:
            # 1행: 이름 및 학번 단독 표시 행
            st.markdown(f'<div class="table-value" style="font-size:17px; font-weight:bold; height:38px;">{name} <span style="font-size:13px; color:#6B7280; font-weight:normal; margin-left:5px;">({hakbun})</span></div>', unsafe_allow_html=True)
            
            # 2행: 소속 및 직위 격자 2분할 행
            row2_c1, row2_c2, row2_c3, row2_c4 = st.columns([18, 32, 18, 32])
            with row2_c1: st.markdown('<div class="table-label">소속</div>', unsafe_allow_html=True)
            with row2_c2: st.markdown(f'<div class="table-value border-right-blue">{sosok}</div>', unsafe_allow_html=True)
            with row2_c3: st.markdown('<div class="table-label">직위</div>', unsafe_allow_html=True)
            with row2_c4: st.markdown(f'<div class="table-value">{jikpup}</div>', unsafe_allow_html=True)
            
            # 3행: TEL 및 CP 연락처 원터치 다이렉트 배치 행
            row3_c1, row3_c2, row3_c3, row3_c4 = st.columns([18, 32, 18, 32])
            with row3_c1: st.markdown('<div class="table-label">TEL</div>', unsafe_allow_html=True)
            with row3_c2:
                if company_phone and company_phone != "nan":
                    st.link_button(company_phone, f"tel:{company_phone}", use_container_width=True)
                else:
                    st.markdown('<div class="table-value border-right-blue">-</div>', unsafe_allow_html=True)
            with row3_c3: st.markdown('<div class="table-label">CP</div>', unsafe_allow_html=True)
            with row3_c4:
                if phone and phone != "nan":
                    st.link_button(phone, f"tel:{phone}", use_container_width=True)
                else:
                    st.markdown('<div class="table-value">-</div>', unsafe_allow_html=True)
                    
            # 4행: 이메일 단독 배치 행 (마지막 줄이므로 바닥 테두리 제거 선언)
            row4_c1, row4_c2 = st.columns([18, 82])
            with row4_c1: st.markdown('<div class="table-label no-bottom-border">e-mail</div>', unsafe_allow_html=True)
            with row4_c2:
                if email and email != "nan":
                    st.link_button(email, f"mailto:{email}", use_container_width=True)
                else:
                    st.markdown('<div class="table-value no-bottom-border">-</div>', unsafe_allow_html=True)
