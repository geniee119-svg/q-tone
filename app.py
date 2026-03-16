import streamlit as st
import re
from datetime import date, timedelta
import streamlit.components.v1 as components  # 복사 버튼 기능을 위해 추가

# 1. 웹 앱 설정 및 디자인 커스텀
st.set_page_config(page_title="큐톤 데이터 생성기", layout="wide")

st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {
        font-family: 'Pretendard', sans-serif !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
    }
    hr {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 메인 화면 상단: 편성 시작일 선택
start_date = st.date_input("편성 시작일 선택", date.today())
fixed_length = "2" 
st.markdown("---")

# 3. 데이터 입력 구역
input_text = st.text_area("로그 데이터 입력", height=350, placeholder="로그 텍스트 전체를 복사해서 붙여넣으세요.")

# 4. 버튼 영역: 입력 및 초기화
col1, col2, _ = st.columns([1, 1, 8])

with col1:
    process_btn = st.button("입력", type="primary")

with col2:
    if st.button("초기화"):
        st.rerun()

# 5. 데이터 가공 로직
if process_btn:
    if input_text.strip():
        lines = input_text.split('\n')
        out_times = []
        excel_rows = []
        
        current_date = start_date
        prev_hour = -1

        for line in lines:
            if line.strip() and 'OUT' in line:
                match = re.search(r'(\d{2}):(\d{2}):(\d{2})(\.\d{2})?', line)
                if match:
                    h_str, m_str, s_str, _ = match.groups()
                    h = int(h_str)
                    if prev_hour != -1 and h < prev_hour:
                        current_date += timedelta(days=1)
                    
                    time_display = f"{h_str}:{m_str}:{s_str}"
                    out_times.append(time_display)
                    excel_rows.append(f"{current_date}\t{h_str}\t{m_str}\t{s_str}\t{fixed_length}")
                    prev_hour = h

        # 6. 결과 출력
        if excel_rows:
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.markdown("**OUT 원본 데이터**")
                st.text("\n".join(out_times))
                
            with res_col2:
                # 결과 텍스트 준비
                final_result = "\n".join(excel_rows)
                
                # 상단 헤더와 복사 버튼 배치
                copy_col1, copy_col2 = st.columns([3, 1])
                with copy_col1:
                    st.markdown("**홈페이지 업로드용 데이터**")
                with copy_col2:
                    # JavaScript 복사 버튼 생성
