import streamlit as st
import pandas as pd
import requests

# ─── 1. 구글 시트 데이터 로드 및 전처리 ───
# 구글 시트의 '웹에 게시(CSV)' 주소 또는 API 주소를 입력하세요.
# 뒤에 '&gid=0'과 같이 시트 ID를 명시할 수 있습니다.
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/gviz/tq?tqx=out:csv"

try:
    # 전체 데이터를 읽어옵니다.
    df = pd.read_csv(SHEET_URL)
    
    # ⚠️ 구글 시트의 첫 번째 행(헤더) 이름에 맞게 아래 'col_mapping'을 수정해주세요.
    # 시트의 열 순서대로 0부터 시작하므로, 안전하게 인덱스(위치) 번호로 열을 추출합니다.
    # A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8
    
    # 필요한 열 인덱스 정의 (A열은 사진 매칭용, 나머지는 표기용)
    idx_A = df.columns[0] # 연번
    idx_B = df.columns[1] # B열
    idx_D = df.columns[3] # D열
    idx_E = df.columns[4] # E열
    idx_F = df.columns[5] # F열
    idx_G = df.columns[6] # G열
    idx_H = df.columns[7] # H열
    idx_I = df.columns[8] # I열

except Exception as e:
    st.error("구글 시트를 불러오는 중 오류가 발생했습니다. URL을 확인해주세요.")
    st.stop()

# ─── 2. 웹 화면 레이아웃 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered")
st.title("📱 웅수회 모바일 회원수첩")
st.write("회원 이름을 검색하거나 아래 목록에서 확인하세요.")

# 검색 기능 (B열인 이름을 기준으로 검색)
search_query = st.text_input("🔍 이름 검색", "")

# ─── 3. 데이터 필터링 및 출력 ───
# 검색어가 있으면 필터링
if search_query:
    display_df = df[df[idx_B].astype(str).str.contains(search_query, na=False)]
else:
    display_df = df

# 기본 이미지 및 깃허브 사진 경로 설정
# ⚠️ 본인의 깃허브 아이디와 저장소(Repository) 이름으로 변경하세요.
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/YOUR_GITHUB_ID/YOUR_REPO_NAME/main/photos/"
DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"

# 회원 목록을 카드 형태로 루프 출력
for index, row in display_df.iterrows():
    # 연번 가져오기 (소수점 제거를 위해 정수형 변환 후 문자열 처리)
    try:
        num_A = str(int(row[idx_A]))
        member_photo_url = f"{GITHUB_PHOTO_BASE_URL}{num_A}.jpg"
        
        # 깃허브에 해당 번호의 사진이 실제로 존재하는지 체크 (HTTP 200)
        response = requests.head(member_photo_url)
        if response.status_code != 200:
            member_photo_url = DEFAULT_IMAGE_URL
    except:
        # 연번이 비어있거나 에러가 나면 기본 이미지 처리
        member_photo_url = DEFAULT_IMAGE_URL

    # 모바일 최적화를 위해 주석/사진 구역 분할 (사진 1 : 정보 2 비율)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(member_photo_url, use_container_width=True)
        
    with col2:
        # B열(이름)과 D열(기수/학번 등) 표기
        st.subheader(f"{row[idx_B]} ({row[idx_D]})")
        
        # E, F열 (소속, 직위) 표기
        st.markdown(f"**소속:** {row[idx_E]} / **직위:** {row[idx_F]}")
        
        # G, H열 (일반전화, 휴대전화) - 스마트폰 전화걸기 링크 생성
        phone_html = ""
        if pd.notna(row[idx_H]): # H열(휴대전화 CP) 우선 연동
            phone_html += f'<a href="tel:{row[idx_H]}" style="text-decoration:none; color:#007BFF; font-weight:bold;">📞 전화하기 ({row[idx_H]})</a><br>'
        elif pd.notna(row[idx_G]): # H열이 없고 G열(일반전화)이 있으면 연동
            phone_html += f'<a href="tel:{row[idx_G]}" style="text-decoration:none; color:#007BFF; font-weight:bold;">📞 일반전화 ({row[idx_G]})</a><br>'
        
        # I열 (이메일) - 스마트폰 이메일 발송 링크 생성
        email_html = ""
        if pd.notna(row[idx_I]):
            email_html += f'<a href="mailto:{row[idx_I]}" style="text-decoration:none; color:#28A745; font-weight:bold;">✉️ 이메일 보내기</a>'
            
        # HTML 렌더링 적용
        if phone_html:
            st.markdown(phone_html, unsafe_allow_html=True)
        if email_html:
            st.markdown(email_html, unsafe_allow_html=True)
            
    st.divider() # 회원 간 구분선