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

# ─── 2. 웹 화면 레이아웃 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered")
st.title("📱 웅수회 모바일 회원수첩")

search_query = st.text_input("🔍 이름 검색", "")

if search_query:
    display_df = df[df[idx_D].astype(str).str.contains(search_query, na=False)]
else:
    display_df = df

# ─── 3. 깃허브 사진 경로 설정 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

# ─── 4. 회원 목록 출력 ───
for index, row in display_df.iterrows():
    if pd.isna(row[idx_A]):
        continue
        
    try:
        num_A = str(int(row[idx_A]))
        member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
    except:
        member_photo_url = DEFAULT_IMAGE_URL

    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 중요! 
        # 1. 먼저 번호.jpg (소문자) 시도
        # 2. 에러 나면 번호.JPG (대문자) 시도
        # 3. 에러 나면 번호.png 시도
        # 4. 에러 나면 번호.jpeg 시도
        # 5. 다 없으면 최종적으로 00.jpg 시도
        html_img = f"""
        <img src="{GITHUB_PHOTO_BASE_URL}{num_A}.jpg" 
             onerror="this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.JPG'; 
                      this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.png'; 
                      this.onerror=null; this.src='{GITHUB_PHOTO_BASE_URL}{num_A}.jpeg'; 
                      this.onerror=null; this.src='{DEFAULT_IMAGE_URL}';" 
             style="width:100%; max-width:120px; border-radius:8px; display:block; margin:auto;" />
        """
        st.markdown(html_img, unsafe_allow_html=True)
        
    with col2:
        st.subheader(f"{row[idx_D]} ({row[idx_B]})")
        st.markdown(f"**소속:** {row[idx_E]} / **직급:** {row[idx_F]}")
        
        phone_html = ""
        if pd.notna(row[idx_G]) and str(row[idx_G]).strip() != "":
            phone_html += f'<a href="tel:{row[idx_G]}" style="text-decoration:none; color:#007BFF; font-weight:bold; display:inline-block; margin-bottom:5px;">📞 휴대폰: {row[idx_G]}</a><br>'
        
        if pd.notna(row[idx_H]) and str(row[idx_H]).strip() != "":
            phone_html += f'<a href="tel:{row[idx_H]}" style="text-decoration:none; color:#555555; font-weight:bold; display:inline-block; margin-bottom:5px;">☎️ 회사: {row[idx_H]}</a><br>'
        
        email_html = ""
        if pd.notna(row[idx_I]) and str(row[idx_I]).strip() != "":
            email_html += f'<a href="mailto:{row[idx_I]}" style="text-decoration:none; color:#28A745; font-weight:bold;">✉️ 이메일: {row[idx_I]}</a>'
            
        if phone_html:
            st.markdown(phone_html, unsafe_allow_html=True)
        if email_html:
            st.markdown(email_html, unsafe_allow_html=True)
            
    st.divider()