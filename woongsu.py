import streamlit as st
import pandas as pd
import json
import urllib.request

# ─── 1. 구글 시트 데이터 로드 ───
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDxJ4wueTgRCsj36rDDw85VryB9To0yJ3gVQEcgrCqBE5uw89hboJdWJstpn3NuaLqT8ubarHcAumz/pub?output=csv"

try:
    df = pd.read_csv(SHEET_URL, dtype=str).fillna("")
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

# ─── 2. 웹 화면 및 스마트폰 맞춤형 CSS 설정 ───
st.set_page_config(page_title="웅수회 회원수첩", layout="centered")

st.markdown("""
    <style>
    .main .block-container { max-width: 500px; padding-top: 15px; padding-left: 10px; padding-right: 10px; }
    h1 { text-align: center; color: #1E3A8A; font-size: 25px !important; font-weight: bold; margin-bottom: 5px; }
    .edit-btn-container { text-align: center; margin-bottom: 20px; }

    /* PC(넓은 화면)에서는 본문 폭을 넓혀서 3열이 여유있게 보이도록 */
    @media (min-width: 900px) {
        .main .block-container { max-width: 1150px; padding-left: 30px; padding-right: 30px; }
    }

    /* 회원 카드들을 감싸는 최상위 블록만 그리드로 전환
       (:has 선택자로 "카드가 직계 자식인 블록"만 정확히 타겟팅 → 카드 내부 레이아웃엔 영향 없음) */
    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stVerticalBlockBorderWrapper"]) {
        display: grid;
        grid-template-columns: 1fr;   /* 모바일/좁은 화면: 1열 */
        gap: 14px;
    }
    @media (min-width: 900px) {
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stVerticalBlockBorderWrapper"]) {
            grid-template-columns: repeat(2, 1fr);  /* PC/넓은 화면: 2열 */
        }
    }

    /* 모든 회원 카드의 프레임 크기를 동일하게 고정 (내용물에 따라 일그러지지 않음) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 14px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.05) !important;
        height: 200px !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }
    
    /* 모든 사진을 00번 규격과 완벽히 동일한 명함 크기로 강제 고정 및 자동 크롭 */
    div[data-testid="stImage"] img {
        width: 95px !important;
        height: 130px !important;
        object-fit: cover !important;
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
    }
    
    /* 줄간격 및 여백 정밀 제어 */
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; line-height: 1.4; }
    div[data-testid="stHorizontalBlock"] { gap: 10px !important; align-items: flex-start !important; }
    
    /* 링크 버튼 스타일 최적화 (텍스트 가독성 중심) */
    div[data-testid="stLinkButton"] a {
        font-size: 11.5px !important;
        font-weight: bold !important;
        padding: 5px 6px !important;
        border-radius: 6px !important;
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

# ─── 3. 깃허브 사진 경로 및 회원 정제 ───
GITHUB_PHOTO_BASE_URL = "https://raw.githubusercontent.com/jeawon83-stack/woongsu/main/photos/"
FALLBACK_DEFAULT_IMAGE_URL = f"{GITHUB_PHOTO_BASE_URL}00.jpg"  # API 실패 시 최후 대비용

def _normalize_key(base_name: str):
    """'05' -> '5' 처럼 앞자리 0을 없앤 숫자 형태 키를 반환. 숫자가 아니면 None."""
    try:
        return str(int(float(base_name.strip())))
    except (ValueError, AttributeError):
        return None

@st.cache_data(ttl=3600)  # 1시간 캐시: 매번 GitHub API를 호출하지 않도록
def get_photo_map():
    """
    GitHub의 photos 폴더 안에 실제로 존재하는 파일 목록을 읽어와서
    {회원번호 문자열: raw 이미지 URL} 형태의 매핑을 만든다.
    확장자(jpg/JPG/png/jpeg 등)와 대소문자, 앞자리 0 유무를 자동으로 흡수한다.
    """
    api_url = "https://api.github.com/repos/jeawon83-stack/woongsu/contents/photos"
    photo_map = {}
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "woongsu-app"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            files = json.loads(resp.read().decode())

        for f in files:
            if f.get("type") != "file":
                continue
            fname = f.get("name", "")
            raw_url = f.get("download_url")
            if "." not in fname or not raw_url:
                continue
            base = fname.rsplit(".", 1)[0].strip()  # 확장자 제거한 파일명(=회원번호로 가정)

            photo_map[base] = raw_url               # 원본 표기 그대로 ("05" 등)
            norm = _normalize_key(base)
            if norm is not None:
                photo_map[norm] = raw_url            # 앞자리 0 없앤 표기 ("5")
    except Exception:
        # API 호출 실패(네트워크/레이트리밋 등) 시 빈 매핑 반환 -> 전원 기본 이미지로 대체됨
        pass
    return photo_map

photo_map = get_photo_map()
DEFAULT_IMAGE_URL = photo_map.get("00", FALLBACK_DEFAULT_IMAGE_URL)

valid_members = []
for index, row in display_df.iterrows():
    val_A = str(row[idx_A]).strip()
    if not val_A or val_A == "nan" or val_A == "":
        continue
    valid_members.append(row)

# ─── 4. 회원 목록 순차 출력 (무조건 깔끔한 1열 고정) ───
with st.container():
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

        # 사진 매칭: GitHub photos 폴더 실제 파일 목록(photo_map)에서 회원번호로 조회
        # 확장자/대소문자/앞자리0 여부와 무관하게 자동으로 찾아준다.
        member_photo_url = photo_map.get(num_A, DEFAULT_IMAGE_URL)

        with st.container(border=True):
            # 가로 배치: 왼쪽 사진(33) : 오른쪽 정보(67)
            card_left, card_right = st.columns([33, 67])
        
            with card_left:
                st.image(member_photo_url, use_container_width=True)
            
            with card_right:
                # 1줄: 이름 및 학번 (글씨 크기 확대)
                st.markdown(f"**<span style='font-size:19px; color:#111827;'>{name}</span>** <span style='color:#6B7280; font-size:13px;'>({hakbun})</span>", unsafe_allow_html=True)
            
                # 2줄: 소속 및 직책 가로 한 줄 정렬 (글씨 크기 확대)
                st.markdown(f"<span style='font-size:14px; color:#4B5563; font-weight:500;'>🏢 {sosok} · {jikpup}</span>", unsafe_allow_html=True)
                st.write("") # 미세 세로 간격 조정
            
                # 3줄: 휴대폰과 회사 번호 동일 높이에 배치
                tel_col1, tel_col2 = st.columns(2)
                with tel_col1:
                    if phone and phone != "nan" and phone != "":
                        st.link_button(f"📞 {phone}", f"tel:{phone}", use_container_width=True)
                    else:
                        st.write("") 
                with tel_col2:
                    if company_phone and company_phone != "nan" and company_phone != "":
                        st.link_button(f"☎️ {company_phone}", f"tel:{company_phone}", use_container_width=True)
                    else:
                        st.write("")
            
                # 4줄: 이메일 주소 단독 하단 배치
                if email and email != "nan" and email != "":
                    st.link_button(f"✉️ {email}", f"mailto:{email}", use_container_width=True)

# ─── 5. 사진 매칭 진단 패널 (평소엔 접혀 있음, 관리 편의용) ───
with st.expander("🛠️ 사진 매칭 확인 (관리자용)"):
    if not photo_map:
        st.warning("photos 폴더 목록을 GitHub API에서 불러오지 못했습니다. 잠시 후 새로고침 해보세요.")
    else:
        unmatched = [
            f"{str(r[idx_D]).strip()} ({str(int(float(r[idx_A]))) if str(r[idx_A]).strip() not in ('', 'nan') else '?'})"
            for r in valid_members
            if photo_map.get(
                str(int(float(r[idx_A]))) if str(r[idx_A]).strip() not in ("", "nan") else "00",
                None
            ) is None
        ]
        if unmatched:
            st.write(f"사진이 매칭되지 않아 기본 이미지로 표시된 회원 ({len(unmatched)}명):")
            st.write(", ".join(unmatched))
            st.caption("→ GitHub photos 폴더에 '회원번호.확장자' 형식(예: 36.jpg)으로 사진을 올리면 자동 반영됩니다.")
        else:
            st.success("전체 회원 사진이 정상적으로 매칭되었습니다.")