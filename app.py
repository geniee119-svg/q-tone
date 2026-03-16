import streamlit as st
import re
from datetime import date, timedelta

# 1. 웹 앱 설정 (페이지 제목 및 아이콘 설정)
st.set_page_config(
    page_title="Cue-tone Data Generator",
    page_icon=":material/analytics:", # Material 아이콘 사용
    layout="wide"
)

# 2. 고도화된 인터페이스 디자인 (CSS 주입)
# Pretendard 글꼴 및 최적화된 디자인 적용
st.markdown("""
    <style>
    /* 전체 글꼴 설정 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {
        font-family: 'Pretendard', sans-serif !important;
    }

    /* 헤더 스타일 조정 */
    .stHeadingContainer h1 {
        font-size: 2.2rem;
        color: #1E1E1E;
        padding-bottom: 0.5rem;
    }
    
    /* 탭(Tab) 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #E0E0E0;
    }
    .stTabs [data-baseweb="tab"] {
        padding-bottom: 0.8rem;
        font-weight: 600;
        font-size: 1.1rem;
        background-color: transparent !important;
    }
    
    /* 버튼 커스텀 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    /* 입력 버튼 (Primary) */
    .stButton>button[kind="primary"] {
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #45a049;
        border: none;
    }
    
    /* 코드 박스 스타일 */
    .stCodeBlock {
        border-radius: 8px;
        border: 1px solid #E0E0E0;
    }
    
    /* 하단 구분선 */
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 고정값 설정
fixed_length = "2" 

# 세션 상태 초기화 (결과 저장을 위해 필요)
if 'result_text' not in st.session_state:
    st.session_state['result_text'] = ""
if 'out_original' not in st.session_state:
    st.session_state['out_original'] = ""

# --- 메인 인터페이스 ---

st.title(":material/schedule: 큐톤 데이터 가공")

# 탭 구조: 가공기(Generator)와 Instructions/Logs 분리
tab1, tab2 = st.tabs([":material/history_edu: 가공 엔진", ":material/description: 사용법 및 로그"])

with tab1:
    # 3. 입력 구역 레이아웃
    col_config, col_input = st.columns([1, 2], gap="large")
    
    with col_config:
        st.subheader(":material/event_note: 설정 및 입력")
        start_date = st.date_input("📅 편성 시작일 선택", date.today())
        
        # 버튼 영역: 가로 배치
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            process_btn = st.button("데이터 가공", type="primary")
        with btn_col2:
            if st.button("초기화"):
                # 세션 상태 초기화 및 페이지 새로고침
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()
                
    with col_input:
        st.subheader(":material/edit_document: 로그 데이터 입력")
        input_text = st.text_area(
            "로그 전체를 복사해서 넣어주세요", 
            height=280, 
            placeholder=" IN  01:00:00 SO범퍼... OUT 01:00:10...",
            label_visibility="collapsed"
        )

# 4. 데이터 가공 로직
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
                    
                    # 자정 감지: 날짜 자동 변경
                    if prev_hour != -1 and h < prev_hour:
                        current_date += timedelta(days=1)
                    
                    time_display = f"{h_str}:{m_str}:{s_str}"
                    out_times.append(time_display)
                    
                    # 홈페이지 업로드용 형식 (탭 구분)
                    excel_rows.append(f"{current_date}\t{h_str}\t{m_str}\t{s_str}\t{fixed_length}")
                    prev_hour = h
                    
        # 결과를 세션 상태에 저장 (JS에서 접근하기 위함)
        if excel_rows:
            st.session_state['result_text'] = "\n".join(excel_rows)
            st.session_state['out_original'] = "\n".join(out_times)
            st.success(f"총 {len(excel_rows)}개의 데이터를 가공했습니다.")
        else:
            st.warning("로그에서 OUT 데이터를 찾을 수 없습니다.")
    else:
        st.warning("데이터를 먼저 입력해주세요.")

# 5. 결과 출력 구역 (탭 아래에 항상 표시)
if st.session_state['result_text']:
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 2], gap="large")
    
    with res_col1:
        st.markdown(":material/text_rotation_none: **OUT 원본 리스트**")
        st.code(st.session_state['out_original'], language=None)
        
    with res_col2:
        # --- 눈에 띄는 데이터 복사 버튼 추가 ---
        header_col, copy_col = st.columns([3, 1])
        
        with header_col:
            st.markdown(":material/database_upload: **홈페이지 업로드용 데이터**")
            
        with copy_col:
            # JavaScript를 이용한 강력한 복사 버튼 주입
            # text_to_copy를 session_state에서 안전하게 가져옴
            text_to_copy = st.session_state['result_text']
            # 코드 내의 역따옴표 처리를 위한 치환
            safe_text = text_to_copy.replace("`", "\\`") 

            st.components.html(f"""
                <button id="mainCopyBtn" style="
                    width: 100%;
                    padding: 8px;
                    background-color: #6C5CE7;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 600;
                    font-size: 0.9rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: all 0.2s;
                ">
                    <span style="font-size: 1rem; color: #white;">content_copy</span> 데이터 복사
                </button>
                <script>
                    document.getElementById('mainCopyBtn').addEventListener('click', () => {{
                        navigator.clipboard.writeText(`{safe_text}`).then(() => {{
                            const btn = document.getElementById('mainCopyBtn');
                            btn.style.backgroundColor = '#4CAF50';
                            btn.innerHTML = '<span style="font-size: 1.1rem;">check_circle</span> 복사 완료!';
                            setTimeout(() => {{
                                btn.style.backgroundColor = '#6C5CE7';
                                btn.innerHTML = '<span style="font-size: 1rem;">content_copy</span> 데이터 복사';
                            }}, 2000);
                        }}).catch(err => {{
                            console.error('복사 실패:', err);
                        }});
                    }});
                </script>
            """, height=50)

        # 실제 코드 출력
        st.code(st.session_state['result_text'], language=None)

with tab2:
    st.info("여기에 사용법이나 지난 로그 기록 등을 추가할 수 있습니다.")
