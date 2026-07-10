import streamlit as st
import pandas as pd
import requests

# ─── 1. 구글 시트 데이터 로드 ───
# 방법 1 또는 방법 2로 얻은 주소를 여기에 넣으세요!
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL)
    
    # 구글 시트의 정확한 열 인덱스 매핑 (A=0, B=1, C=2, D=3...)
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

# ─── 2. 웹 화면 레이아웃 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered")
st.title("📱 웅수회 모바일 회원수첩")

# 검색 기능 (D열인 '이름'을 기준으로 검색)
search_query = st.text_input("🔍 이름 검색", "")

# 검색어가 있으면 필터링
if search_query:
    display_df = df[df[idx_D].astype(str).str.contains(search_query, na=False)]
else:
    display_df = df

# ─── 3. 깃허브 사진 경로 설정 ───
# ⚠️ 본인의 깃허브 아이디와 저장소(Repository) 이름으로 꼭 변경하세요!
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/eawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

# ─── 4. 회원 목록 출력 ───
for index, row in display_df.iterrows():
    # 번호(A열)가 비어있는 행은 패스합니다.
    if pd.isna(row[idx_A]):
        continue
        
    # A열 번호 기반 사진 주소 생성 (예: 1 -> 1.jpg)
    try:
        num_A = str(int(row[idx_A]))
        member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    except:
        member_photo_url = DEFAULT_IMAGE_URL

    # 레이아웃 구성 (사진 1 : 정보 2 비율)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # html 태그를 직접 사용하여 사진이 없을 때(에러 발생 시) 자동으로 00.jpg를 보여주도록 설정
        html_img = f"""
        <img src="{member_photo_url}" 
             onerror="this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" 
             style="width:100%; max-width:120px; border-radius:8px; display:block; margin:auto;" />
        """
        st.markdown(html_img, unsafe_allow_html=True)
        
    with col2:
        # 이름(D)과 학번(B) 표기
        st.subheader(f"{row[idx_D]} ({row[idx_B]})")
        
        # 소속(E)과 직급(F) 표기
        st.markdown(f"**소속:** {row[idx_E]} / **직급:** {row[idx_F]}")
        
        # 전화번호 설정 (G열: 전화번호1 / H열: 전화번호(회사))
        phone_html = ""
        if pd.notna(row[idx_G]) and str(row[idx_G]).strip() != "":
            phone_html += f'<a href="tel:{row[idx_G]}" style="text-decoration:none; color:#007BFF; font-weight:bold; display:inline-block; margin-bottom:5px;">📞 휴대폰: {row[idx_G]}</a><br>'
        
        if pd.notna(row[idx_H]) and str(row[idx_H]).strip() != "":
            phone_html += f'<a href="tel:{row[idx_H]}" style="text-decoration:none; color:#555555; font-weight:bold; display:inline-block; margin-bottom:5px;">☎️ 회사: {row[idx_H]}</a><br>'
        
        # 이메일(I) 설정
        email_html = ""
        if pd.notna(row[idx_I]) and str(row[idx_I]).strip() != "":
            email_html += f'<a href="mailto:{row[idx_I]}" style="text-decoration:none; color:#28A745; font-weight:bold;">✉️ 이메일: {row[idx_I]}</a>'
            
        if phone_html:
            st.markdown(phone_html, unsafe_allow_html=True)
        if email_html:
            st.markdown(email_html, unsafe_allow_html=True)
            
    st.divider()