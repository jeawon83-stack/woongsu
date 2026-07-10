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

# ─── 2. 웹 화면 및 글로벌 CSS 스타일 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 1200px; padding-top: 20px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 26px !important; font-weight: bold; margin-bottom: 25px; }
    
    /* 카드 외곽 테두리 디자인 */
    .css-card {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px;
        background-color: #ffffff;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 웅수회 모바일 회원수첩")

# 이름 검색창 (스마트폰 크기에 최적화)
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

# ─── 4. 회원 목록 출력 (안전한 좌/우 분할 Grid 방식) ───
# PC/태블릿에서는 3열 분할, 스마트폰 세로 모드에서는 자동으로 1열 배치가 됩니다.
grid_cols = st.columns(3)

col_idx = 0
for index, row in display_df.iterrows():
    if pd.isna(row[idx_A]):
        continue
        
    try:
        num_A = str(int(float(row[idx_A])))
    except:
        continue

    # 데이터 추출 및 공백 제거
    name = str(row[idx_D]).strip()
    hakbun = str(row[idx_B]).strip()
    sosok = str(row[idx_E]).strip()
    jikpup = str(row[idx_F]).strip()
    phone = str(row[idx_G]).strip() if pd.notna(row[idx_G]) else ""
    company_phone = str(row[idx_H]).strip() if pd.notna(row[idx_H]) else ""
    email = str(row[idx_I]).strip() if pd.notna(row[idx_I]) else ""

    # 3개의 대열에 차례대로 카드를 분배 (모바일에서는 누락 없이 1줄로 순서대로 정렬됩니다)
    target_col = grid_cols[col_idx % 3]
    
    with target_col:
        # 카드 프레임 시작
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        
        # 💡 [핵심 구현] 내부를 좌측(사진 3.5 비율) : 우측(정보 6.5 비율)로 고정 분할
        card_left, card_right = st.columns([35, 65])
        
        with card_left:
            # 대소문자 확장자 에러를 방지하는 HTML 이미지 삽입
            img_html = f"""
            <img src="{GITHUB_PHOTO_BASE_URL}{num_A}.jpg" 
                 onerror="this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.JPG'; 
                          this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.png'; 
                          this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg'; 
                          this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" 
                 style="width:100%; height:120px; object-fit:cover; border-radius:8px; border:1px solid #E5E7EB;" />
            """
            st.markdown(img_html, unsafe_allow_html=True)
            
        with card_right:
            # 우측 정보 영역 출력
            st.markdown(f"**<span style='font-size:16px;'>{name}</span>** <span style='color:#6B7280; font-size:12px;'>({hakbun})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:12px; color:#4B5563; line-height:1.3;'><b>소속</b>: {sosok}<br><b>직급</b>: {jikpup}</span>", unsafe_allow_html=True)
            
            # 실제 번호 링크 버튼 구성 (터치 시 바로 연결)
            if phone and phone != "nan" and phone != "":
                st.markdown(f'<a href="tel:{phone}" style="display:block; text-decoration:none; font-size:11px; font-weight:600; padding:4px 5px; background-color:#E0F2FE; color:#0369A1; border-radius:4px; margin-top:3px; text-align:center; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">📞 {phone}</a>', unsafe_allow_html=True)
            if company_phone and company_phone != "nan" and company_phone != "":
                st.markdown(f'<a href="tel:{company_phone}" style="display:block; text-decoration:none; font-size:11px; font-weight:600; padding:4px 5px; background-color:#F3F4F6; color:#4B5563; border-radius:4px; margin-top:3px; text-align:center; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">☎️ {company_phone}</a>', unsafe_allow_html=True)
            if email and email != "nan" and email != "":
                st.markdown(f'<a href="mailto:{email}" style="display:block; text-decoration:none; font-size:11px; font-weight:600; padding:4px 5px; background-color:#DCFCE7; color:#15803D; border-radius:4px; margin-top:3px; text-align:center; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">✉️ {email}</a>', unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    col_idx += 1
