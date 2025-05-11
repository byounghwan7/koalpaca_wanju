import streamlit as st
# Set page config (must be first Streamlit command)
st.set_page_config(
    page_title="토양 정보 챗봇 (KoAlpaca 기반)",
    page_icon="🌱",
    layout="wide"
)

import pandas as pd
import os
import tempfile
import base64

from pdf_processor import extract_text_from_pdf
from csv_processor import process_csv_data
from utils import get_soil_image_url
from koalpaca_chatbot import get_chat_response_koalpaca, KoAlpacaModelManager

# Initialize session state variables
if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = ""
if 'csv_data' not in st.session_state:
    st.session_state.csv_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = ""
if 'response_time' not in st.session_state:
    st.session_state.response_time = ""
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# App title
st.title("🐨 토양 정보 챗봇 (KoAlpaca 기반)")

# 모델 초기화
model_manager = KoAlpacaModelManager.get_instance()

# 기본 데이터 로드 (미리 업로드된 파일)
if not st.session_state.pdf_content and not st.session_state.csv_data:
    with st.spinner("사전 업로드된 데이터 로드 중..."):
        # 1. PDF 파일 로드
        pdf_path = "attached_assets/KSIC_9rd_handbook.pdf"
        if os.path.exists(pdf_path):
            extracted_text = extract_text_from_pdf(pdf_path)
            st.session_state.pdf_content = extracted_text
            st.session_state.knowledge_base = extracted_text
            st.success(f"기초 토양조사 매뉴얼 로드 완료!")
        elif os.path.exists("data/KSIC_9rd_handbook.pdf"):  # Streamlit Cloud 배포용 경로
            extracted_text = extract_text_from_pdf("data/KSIC_9rd_handbook.pdf")
            st.session_state.pdf_content = extracted_text
            st.session_state.knowledge_base = extracted_text
            st.success(f"기초 토양조사 매뉴얼 로드 완료!")
        
        # 2. CSV 파일 로드
        csv_path = "data/chatbot_wanju_reduced.csv"  # 축소된 CSV 파일 사용
        if os.path.exists(csv_path):
            try:
                csv_data = pd.read_csv(csv_path)
                cleaned_data = process_csv_data(csv_data)
                st.session_state.csv_data = cleaned_data
                
                # Update knowledge base with CSV data summary
                if cleaned_data is not None:
                    csv_summary = f"CSV 데이터 요약:\n총 레코드: {len(cleaned_data)}\n컬럼: {', '.join(cleaned_data.columns)}\n"
                    csv_sample = cleaned_data.head(5).to_string()
                    st.session_state.knowledge_base += "\n\n" + csv_summary + csv_sample
                
                st.success(f"완주군 토양 데이터 로드 완료!")
            except Exception as e:
                st.error(f"CSV 파일 처리 오류: {str(e)}")

# Sidebar for file uploads and model loading
with st.sidebar:
    st.header("설정")
    
    # 모델 로드 버튼
    st.subheader("KoAlpaca 모델 설정")
    st.info("KoAlpaca는 한국어에 최적화된 언어 모델로, 토양 관련 질문에 한국어로 응답할 수 있습니다.")
    
    if st.button("모델 로드"):
        with st.spinner("KoAlpaca 모델 로드 중..."):
            if model_manager.load_model():
                st.session_state.model_loaded = True
                st.success("KoAlpaca 모델 로드 완료!")
            else:
                st.error("모델 로드 실패")
    
    st.divider()
    
    st.header("문서 업로드")
    
    # Upload PDF
    pdf_file = st.file_uploader("토양 조사 PDF 업로드", type=["pdf"])
    if pdf_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_file_path = tmp_file.name
        
        with st.spinner("PDF 처리 중..."):
            extracted_text = extract_text_from_pdf(tmp_file_path)
            st.session_state.pdf_content = extracted_text
            st.session_state.knowledge_base = extracted_text
            st.success(f"PDF 처리 완료: {pdf_file.name}")
        
        # Clean up temp file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
    
    # Upload CSV
    csv_file = st.file_uploader("토양 특성 CSV 업로드", type=["csv"])
    if csv_file is not None:
        try:
            with st.spinner("CSV 처리 중..."):
                csv_data = process_csv_data(csv_file)
                st.session_state.csv_data = csv_data
                
                # Update knowledge base with CSV data summary
                if csv_data is not None:
                    csv_summary = f"CSV 데이터 요약:\n총 레코드: {len(csv_data)}\n컬럼: {', '.join(csv_data.columns)}\n"
                    csv_sample = csv_data.head(5).to_string()
                    st.session_state.knowledge_base += "\n\n" + csv_summary + csv_sample
                
                st.success(f"CSV 처리 완료: {csv_file.name}")
        except Exception as e:
            st.error(f"CSV 파일 처리 오류: {str(e)}")
    
    # Display soil images
    st.subheader("토양 샘플")
    soil_sample_urls = [
        "https://pixabay.com/get/gceac3a9ce515b90e239f181006e66ad4c0d6953cd04742a4fd986d5fc83ca36cad5f6bd380211bd3c749899079602437c6169d22a35bc76a732a4bc528c37c73_1280.jpg",
        "https://pixabay.com/get/gd8c78dee3bbb5a01621e67faca20fc2b809dfe883bbf2a1a73eeb04242f0db5505b46dc551fe4e109a98feb81139e2b2ee545413e1f601d5fa027139821a00aa_1280.jpg",
    ]
    
    sample_cols = st.columns(2)
    for i, url in enumerate(soil_sample_urls[:2]):
        sample_cols[i % 2].image(url, use_container_width=True, caption=f"토양 샘플 {i+1}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    st.header("토양 정보 챗")
    
    # 모델 상태 표시
    model_status = "✅ 준비됨" if st.session_state.model_loaded else "⚠️ 모델 로드 필요"
    st.markdown(f"**KoAlpaca 모델 상태:** {model_status}")
    
    # 모델 로드 알림
    if not st.session_state.model_loaded:
        st.warning("왼쪽 사이드바에서 '모델 로드' 버튼을 클릭하세요.")
        
        # 문제 해결 가이드
        with st.expander("모델 로드에 관한 참고사항"):
            st.markdown("""
            ### KoAlpaca 모델 사용 안내
            
            KoAlpaca는 스탠포드의 Alpaca를 한국어에 맞게 파인튜닝한 모델입니다.
            
            이 데모 버전에서는 실제 모델 파일을 다운로드하지 않고 시뮬레이션된 응답을 제공합니다.
            실제 구현에서는 Hugging Face에서 모델을 다운로드하여 사용해야 합니다.
            
            KoAlpaca 모델은 한국어 토양 관련 질문에 더 자연스러운 응답을 제공할 수 있습니다.
            """)
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Assistant:** {message['content']}")
    
    # User input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("토양 특성에 대해 질문하세요:", placeholder="질문을 입력하세요...")
        submit_button = st.form_submit_button("전송")
        
        if submit_button and user_input:
            # Check if model is loaded
            if not st.session_state.model_loaded:
                st.warning("먼저 모델을 로드해야 합니다. 사이드바에서 '모델 로드' 버튼을 클릭하세요.")
            else:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get response from KoAlpaca chatbot
                with st.spinner("생각 중..."):
                    if st.session_state.knowledge_base:
                        response = get_chat_response_koalpaca(
                            user_input, 
                            st.session_state.knowledge_base, 
                            st.session_state.csv_data
                        )
                    else:
                        response = "토양 조사 PDF 또는 CSV 파일을 업로드하여 질문을 시작하세요."
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # 응답 시간 표시
                if 'response_time' in st.session_state and st.session_state.response_time:
                    st.info(f"응답 생성 시간: {st.session_state.response_time}")
                
                # Refresh the page to show the updated chat
                st.rerun()

with col2:
    # Data preview section
    st.header("데이터 미리보기")
    
    # Display PDF content preview
    if st.session_state.pdf_content:
        with st.expander("PDF 내용 미리보기", expanded=False):
            st.text_area("추출된 텍스트", st.session_state.pdf_content[:1000] + "...", height=200, disabled=True)
    
    # Display CSV data preview
    if st.session_state.csv_data is not None:
        with st.expander("CSV 데이터 미리보기", expanded=False):
            st.dataframe(st.session_state.csv_data.head(10))
    
    # Search by address section
    st.subheader("주소로 검색")
    address_search = st.text_input("토양 정보를 찾을 주소 입력:")
    
    if address_search and st.session_state.csv_data is not None:
        # Search for address in CSV data
        try:
            filtered_data = st.session_state.csv_data[
                st.session_state.csv_data.apply(
                    lambda row: address_search.lower() in str(row).lower(), axis=1
                )
            ]
            
            if not filtered_data.empty:
                st.success(f"'{address_search}'에 대한 {len(filtered_data)}개 결과 발견")
                st.dataframe(filtered_data)
                
                # Display a random soil image based on the address
                soil_image = get_soil_image_url(address_search)
                if soil_image:
                    st.image(soil_image, caption="관련 토양 유형", use_container_width=True)
            else:
                st.warning(f"'{address_search}'에 대한 결과를 찾을 수 없습니다")
        except Exception as e:
            st.error(f"주소 검색 오류: {str(e)}")
    
    # Instructions section
    st.subheader("사용 방법")
    st.markdown("""
    1. 왼쪽 사이드바에서 KoAlpaca 모델 로드
    2. 토양 조사 PDF 문서 업로드
    3. 주소별 토양 데이터가 있는 CSV 파일 업로드
    4. 챗에서 토양 특성에 관한 질문
    5. 특정 주소 검색하여 토양 정보 찾기
    
    질문 예시:
    - 토색이 뭐야?
    - 전라북도 완주군 삼례읍의 토양 특성은 어떤가요?
    - 석천 토양통의 특징이 무엇인가요?
    - 양토와 사양토의 차이점은 무엇인가요?
    - 완주군에서 배수가 양호한 지역은 어디인가요?
    """)

# Footer
st.markdown("---")
st.caption("토양 정보 챗봇 - KoAlpaca 및 Streamlit 기반")