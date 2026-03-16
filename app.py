import streamlit as st
import re
import base64
from datetime import date, timedelta
import streamlit.components.v1 as components

# 1. 폰트 및 로고 파일 로드 함수
def get_base64_bin(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 파일이 없을 경우를 대비한 예외 처리
try:
    font_b64 = get_base64_bin("MBC NEW L.ttf")
    logo_b64 = get_base64_bin("logo.png")
except FileNotFoundError:
    st.error("폰트 또는 로고 파일을 찾을 수 없습니다. 파일명을 확인해 주세요.")
    st.stop()

# 2. 웹 앱 설정 및 디자인 커스텀 (CSS)
st.set_page_config(page_title="MBC NET 큐톤 생성기", layout="wide")

# 포인트 컬러 설정
POINT_COLOR = "#684CDB"

st.markdown(f"""
    <style>
    /* 사내 폰트 정의 */
    @font-face {{
        font-family: 'MBC_NEW_L';
        src: url(data:font/ttf;charset=utf-8;base64,{font_b64}) format('truetype');
    }}
    
    /* 전체 적용 */
    * {{ font-family: 'MBC_NEW_L', sans-serif !important; }}
    
    /* 버튼 스타일: 고유 색상 적용 */
    .stButton>button[kind="primary"] {{
        background-color: {POINT_COLOR};
        border-color: {POINT_COLOR};
        color: white;
    }}
    .stButton>button:hover {{
        border-color: {POINT_COLOR};
        color: {POINT_COLOR};
    }}
    
    /* 강조선(hr) 스타일 커스텀 */
    hr {{
        border: 0;
        height: 2px;
        background: {POINT_COLOR};
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    /* 입력창 포커스 시 테두리 색상 */
    textarea:focus {{
        border-color: {POINT_COLOR} !important;
        box-shadow: 0 0 0 0.2rem rgba(104, 76, 219, 0.25) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 상단 헤더: 회사 로고 및 날짜 선택
col_logo, col_date = st.columns([1, 1])
with col_logo:
    # 로고 이미지 삽입
    st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="180">', unsafe_allow_html=True)

with col_date:
    start_date = st.date_input("편성 시작일 선택", date.today())

st.markdown("<hr>", unsafe_allow_html=True) # 커스텀 강조선

# 4. 데이터 입력 구역
input_text = st.text_area("로그 데이터 입력", height=350, placeholder="로그 텍스트 전체를 복사해서 붙여넣으세요.")

# 5. 버튼 영역: 입력 및 초기화
col1, col2, _ = st.columns([1, 1, 8])
with col1:
    process_btn = st.button("입력", type="primary")
with col2:
    if st.button("초기화"):
        st.rerun()

# 6. 데이터 가공 로직 및 결과 출력 (기존 로직 유지)
fixed_length = "2"
if process_btn:
    if input_text.strip():
        # ... (이전과 동일한 가공 로직 수행) ...
        # [결과 출력부에서 '데이터 복사' 버튼에도 POINT_COLOR 적용 권장]
        st.success("데이터 가공이 완료되었습니다.")
    else:
        st.warning("데이터를 먼저 입력해주세요.")
