import streamlit as st
import re
from datetime import date, timedelta

# 1. 웹 앱 기본 설정 및 제목
st.set_page_config(page_title="큐톤", layout="wide")
st.title("📺 큐톤 데이터 생성기")
st.markdown("---")

# 2. 사이드바: 편성일 선택 및 고정값 설정
# [날짜 입력창을 메인화면으로 이동]
st.header("📅 데이터 설정")
start_date = st.date_input("편성 시작일 선택", date.today())
start_date = st.sidebar.date_input("편성 시작일 선택", date.today())
fixed_length = "2"  # 큐톤은 무조건 2분 고정

# 3. 메인 화면 구성
st.info(f"날짜: **{start_date}** ")
input_text = st.text_area("로그 데이터를 아래에 붙여넣으세요.", height=350, placeholder="로그 텍스트 전체를 복사해서 넣어주세요...")

# 4. 데이터 가공 로직
if st.button("🚀 입력"):
    if input_text.strip():
        lines = input_text.split('\n')
        out_times = []
        excel_rows = []
        
        current_date = start_date
        prev_hour = -1

        for line in lines:
            # 💡 'OUT'이 포함된 줄만 필터링하여 가공합니다.
            if line.strip() and 'OUT' in line:
                # 타임코드 추출 (HH:MM:SS.ss 또는 HH:MM:SS)
                match = re.search(r'(\d{2}):(\d{2}):(\d{2})(\.\d{2})?', line)
                if match:
                    h_str, m_str, s_str, _ = match.groups()
                    h = int(h_str)
                    
                    # 💡 자정 감지: 이전 시간(prev_hour)보다 현재 시간(h)이 작으면 날짜 변경
                    if prev_hour != -1 and h < prev_hour:
                        current_date += timedelta(days=1)
                    
                    # 시:분:초 형식 저장
                    time_display = f"{h_str}:{m_str}:{s_str}"
                    out_times.append(time_display)
                    
                    # 홈페이지 업로드용 형식: 날짜 \t 시 \t 분 \t 초 \t 2
                    excel_rows.append(f"{current_date}\t{h_str}\t{m_str}\t{s_str}\t{fixed_length}")
                    
                    # 비교를 위해 현재 시(Hour) 저장
                    prev_hour = h

        # 5. 결과 출력 레이아웃
        if excel_rows:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("✅ OUT 원본 데이터")
                st.text("\n".join(out_times))
                
            with col2:
                st.subheader("📊 홈페이지 업로드")
                # 탭 구분 텍스트 생성
                final_result = "\n".join(excel_rows)
                st.code(final_result, language=None)
                st.success(f"총 {len(excel_rows)}개의 데이터를 가공했습니다. 위 박스의 복사 버튼을 누르세요!")
        else:
            st.warning("로그에서 'OUT' 타임코드를 찾을 수 없습니다. 형식을 확인해주세요.")
    else:
        st.warning("먼저 데이터를 입력해주세요.")