import os
import streamlit as st
import pandas as pd
import time

# 참고: 실제 구현에서는 huggingface_hub 패키지가 필요합니다
# from huggingface_hub import hf_hub_download, snapshot_download

# KoAlpaca 모델 관리 클래스 
class KoAlpacaModelManager:
    """KoAlpaca 모델 관리 클래스"""
    
    # 싱글톤 인스턴스
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """싱글톤 인스턴스 반환"""
        if cls._instance is None:
            cls._instance = KoAlpacaModelManager()
        return cls._instance
    
    def __init__(self):
        """초기화 - 모델 로딩 상태 설정"""
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        
        # 모델 정보
        self.model_info = {
            "koalpaca-small": {
                "repo_id": "beomi/KoAlpaca-65B-v1.1",
                "model_files": ["pytorch_model.bin", "config.json", "tokenizer.json", "tokenizer_config.json"],
                "path": "models/koalpaca-small",
                "context_size": 2048
            }
        }
    
    def download_model(self, model_name="koalpaca-small"):
        """모델 파일 다운로드 시도"""
        st.info("KoAlpaca 모델은 큰 용량으로 인해 실제 다운로드는 비활성화되었습니다.")
        st.info("실제 구현 시에는 Hugging Face에서 모델을 다운로드하거나 사전 설치해야 합니다.")
        
        # 실제 구현에서는 아래 코드를 활성화할 수 있습니다.
        """
        try:
            repo_id = self.model_info[model_name]["repo_id"]
            local_dir = self.model_info[model_name]["path"]
            
            os.makedirs(local_dir, exist_ok=True)
            
            with st.spinner(f"KoAlpaca 모델 다운로드 중... ({model_name})"):
                for file in self.model_info[model_name]["model_files"]:
                    hf_hub_download(
                        repo_id=repo_id,
                        filename=file,
                        local_dir=local_dir
                    )
                st.success(f"모델 다운로드 완료: {model_name}")
                return True
                
        except Exception as e:
            st.error(f"모델 다운로드 실패: {str(e)}")
            return False
        """
        
        # 데모 목적으로 성공했다고 가정
        return True
        
    def load_model(self, model_name="koalpaca-small"):
        """KoAlpaca 모델 로드"""
        # 데모 환경에서는 실제 로드 대신 성공했다고 가정
        try:
            # 실제 구현에서는 아래와 같이 모델을 로드합니다.
            """
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            model_path = self.model_info[model_name]["path"]
            
            # 모델 다운로드 확인 및 시도
            if not os.path.exists(model_path) or not os.listdir(model_path):
                if not self.download_model(model_name):
                    return False
            
            # 토크나이저 및 모델 로드
            with st.spinner(f"KoAlpaca 모델을 로드하는 중... ({model_name})"):
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path, 
                    torch_dtype=torch.float16, 
                    low_cpu_mem_usage=True
                )
                if torch.cuda.is_available():
                    self.model = self.model.cuda()
                self.is_loaded = True
                st.success(f"KoAlpaca 모델 로드 완료: {model_name}")
                return True
            """
            
            # 데모 목적으로 로드에 성공했다고 가정
            time.sleep(2)  # 로딩 시간 시뮬레이션
            self.is_loaded = True
            st.success(f"KoAlpaca 모델 로드 완료: {model_name} (데모 모드)")
            return True
            
        except Exception as e:
            st.error(f"모델 로드 실패: {str(e)}")
            return False
    
    def generate_response(self, prompt, max_tokens=300, temperature=0.7):
        """응답 생성"""
        if not self.is_loaded:
            return "모델이 로드되지 않았습니다. 먼저 모델을 로드해주세요."
            
        try:
            # 실제 구현에서는 아래와 같이 모델로 응답을 생성합니다.
            """
            import torch
            
            with st.spinner("KoAlpaca 모델이 응답을 생성하는 중..."):
                start_time = time.time()
                
                # 입력 인코딩
                inputs = self.tokenizer(prompt, return_tensors="pt")
                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                # 응답 생성
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.9,
                    do_sample=True,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.pad_token_id
                )
                
                # 결과 디코딩
                result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                # 프롬프트 제거하고 응답만 반환
                response = result[len(prompt):].strip()
                
                end_time = time.time()
                st.session_state.response_time = f"{end_time - start_time:.2f} 초"
                
                return response
            """
            
            # 데모 목적의 응답 생성
            time.sleep(1)  # 응답 생성 시간 시뮬레이션
            
            # 일부 미리 정의된 응답 (토양 관련)
            if "토색" in prompt.lower() or "토양 색" in prompt.lower():
                response = """
토색은 토양의 색깔을 의미합니다. 토양의 색깔은 토양의 구성 성분과 특성을 나타내는 중요한 지표입니다.

토색의 주요 특징:
1. 토양의 색은 먼셀 컬러 시스템으로 측정하며, 색상, 명도, 채도로 표현합니다.
2. 토색을 통해 유기물 함량, 광물 함량, 배수 상태 등을 추정할 수 있습니다.

주요 토색과 의미:
- 검은색/짙은 갈색: 유기물 함량이 높음, 비옥한 토양
- 붉은색/적갈색: 철 산화물 함량이 높음, 배수가 잘됨
- 회색/청회색: 환원 상태, 배수 불량
- 황갈색: 배수 양호, 철 화합물 함유
- 밝은 색/회백색: 규소, 점토, 탄산염, 석고 등 함유

토색은 농업에서 작물 재배 적합성을 평가하는 데 중요한 요소입니다.
"""
            elif "토양통" in prompt.lower() or "석천" in prompt.lower():
                response = """
토양통은 토양 분류 체계에서 사용하는 기본 단위입니다. 같은 토양통에 속하는 토양은 비슷한 특성을 가집니다.

석천 토양통은 다음과 같은 특성이 있습니다:
- 양토 또는 사양토로 구성
- 배수 상태가 양호하거나 매우 양호함
- 유효토심은 50-100cm로 보통 수준
- 주로 산성암을 모재로 함
- 산악지나 구릉지에 주로 분포

이러한 특성으로 석천 토양통은 다양한 작물 재배에 적합합니다.
"""
            elif "토성" in prompt.lower():
                response = """
토성(Soil Texture)은 토양의 물리적 특성을 나타내는 것으로, 모래, 미사, 점토의 비율에 따라 결정됩니다.

주요 토성 분류:
- 사토(Sand): 모래 함량이 높음, 배수 양호, 보수력 낮음
- 양토(Loam): 모래, 미사, 점토가 균형적으로 분포, 이상적인 토양 구조
- 식토(Clay): 점토 함량이 높음, 배수 불량, 보수력 높음
- 사양토(Sandy Loam): 모래가 많고 점토가 적은 양토
- 미사질양토(Silty Loam): 미사가 많은 양토

완주군 지역은 주로 양토와 사양토가 분포하고 있어 농업에 유리한 조건을 갖추고 있습니다.
"""
            else:
                response = f"""
안녕하세요, 저는 토양 정보 전문가입니다. '{prompt.strip()}'에 대한 질문이군요.

토양에 관한 질문을 구체적으로 해주시면 더 정확한 정보를 제공해드릴 수 있습니다.
예를 들어 토색, 토성, 배수 등 특정 토양 특성이나 지역에 대해 질문해주세요.

완주군 지역의 토양은 주로 석천, 고천 등의 토양통으로 이루어져 있으며, 
양호한 배수와 적절한 유효토심을 가진 곳이 많습니다.
"""
            
            st.session_state.response_time = "1.2 초 (데모 모드)"
            return response.strip()
            
        except Exception as e:
            return f"응답 생성 중 오류 발생: {str(e)}"

def create_koalpaca_prompt(instruction, input_text=""):
    """KoAlpaca 모델용 프롬프트 생성"""
    if input_text:
        prompt = f"### 명령어:\n{instruction}\n\n### 입력:\n{input_text}\n\n### 응답:\n"
    else:
        prompt = f"### 명령어:\n{instruction}\n\n### 응답:\n"
    return prompt

def create_context_koalpaca(user_query, knowledge_base, csv_data=None):
    """
    KoAlpaca 모델용 컨텍스트 생성 (chatbot.py의 create_context 대체)
    
    Args:
        user_query (str): 사용자 질문
        knowledge_base (str): 추출된 문서 텍스트
        csv_data (pandas.DataFrame, optional): 처리된 CSV 데이터
        
    Returns:
        str: 생성된 컨텍스트
    """
    # 초기 컨텍스트
    context = ""
    
    # 토색 관련 질문인지 확인
    if "토색" in user_query.lower() or "흙 색깔" in user_query.lower() or "토양 색" in user_query.lower():
        context = """
토색(Soil Color)은 토양의 색깔을 의미합니다. 토양의 색은 유기물 함량, 광물질, 배수 상태 등 토양의 특성을 반영합니다.
주요 토색과 의미:
- 검은색/짙은 갈색: 유기물 함량이 높음
- 붉은색/적갈색: 철 산화물 함량이 높음, 배수 양호
- 회색/청회색: 환원 상태, 배수 불량
- 황갈색: 배수 양호, 철 화합물 함유
- 밝은 색/회백색: 규소, 점토, 탄산염, 석고 등 함유
"""
    # 토양통 관련 질문인지 확인
    elif "토양통" in user_query.lower() or "석천" in user_query.lower() or "남계" in user_query.lower() or "고천" in user_query.lower():
        context = """
토양통은 토양 분류의 기본 단위로, 같은 특성을 가진 토양을 하나의 그룹으로 분류한 것입니다.
완주군 지역에는 석천, 남계, 고천 등의 토양통이 분포합니다.
- 석천: 양토, 사양질, 배수 양호, 산성암 기원
- 남계: 사양토, 사질, 배수 양호, 변성암 기원
- 고천: 사양토, 사양질, 배수 매우양호, 변성암 기원
"""
    # 토성 관련 질문인지 확인
    elif "토성" in user_query.lower() or "양토" in user_query.lower() or "사양토" in user_query.lower():
        context = """
토성은 토양의 물리적 특성으로, 모래, 미사, 점토의 비율에 따라 결정됩니다.
주요 토성:
- 사토: 모래 함량 높음, 배수 양호, 보수력 낮음
- 양토: 모래, 미사, 점토 균형적 분포, 이상적 토양
- 식토: 점토 함량 높음, 배수 불량, 보수력 높음
- 사양토: 모래가 많은 양토, 배수 양호
"""
    # 주소 관련 질문인지 확인
    elif "완주" in user_query.lower() or "삼례" in user_query.lower() or "주소" in user_query.lower():
        context = """
완주군은 전라북도에 위치한 지역으로, 다양한 토양 특성을 가지고 있습니다.
삼례읍의 토양은 주로 석천, 남계, 고천 토양통으로 구성되어 있으며, 
대체로 사양토에서 양토의 토성을 가지고 있고 배수 상태는 양호합니다.
"""
    # 기본 컨텍스트
    else:
        context = """
토양은 식물이 자라는 기반이 되는 자연체로, 다양한 특성을 가집니다.
주요 토양 특성에는 토색, 토성, 구조, 배수, 유효토심, 비옥도 등이 있습니다.
토양은 농업, 환경, 생태계에 중요한 영향을 미치는 자원입니다.
"""
    
    # CSV 데이터에서 관련 정보 추가
    if csv_data is not None:
        context += "\n토양 조사 데이터 요약:\n"
        context += f"총 레코드 수: {len(csv_data)}\n"
        
        # 토양통 분포 확인
        if '토양통명' in csv_data.columns:
            soil_types = csv_data['토양통명'].value_counts()
            context += f"주요 토양통: {', '.join(soil_types.index[:3])}\n"
        
        # 토성 분포 확인
        if '표토토성' in csv_data.columns:
            texture_types = csv_data['표토토성'].value_counts()
            context += f"주요 표토토성: {', '.join(texture_types.index[:3])}\n"
    
    # 현재 문서에서 키워드 검색하여 추가정보 얻기
    if knowledge_base:
        relevant_snippets = []
        
        # 검색 키워드 생성
        search_terms = []
        for word in user_query.lower().split():
            if len(word) > 2:
                search_terms.append(word)
        
        # 특별 키워드
        if "토색" in user_query.lower():
            search_terms.extend(["토색", "색깔", "색상"])
        if "토성" in user_query.lower():
            search_terms.extend(["토성", "양토", "사토", "점토"])
            
        # 문서 내용 검색
        if search_terms:
            paragraphs = knowledge_base.split('\n\n')
            for para in paragraphs:
                if any(term in para.lower() for term in search_terms):
                    if len(para) > 20:  # 너무 짧은 문단 제외
                        relevant_snippets.append(para)
        
        # 관련 내용 추가
        if relevant_snippets:
            context += "\n\n문서에서 발견된 관련 정보:\n"
            # 너무 많은 정보가 추가되지 않도록 제한
            for snippet in relevant_snippets[:3]:
                context += snippet + "\n\n"
    
    return context

def get_chat_response_koalpaca(user_query, knowledge_base, csv_data=None):
    """
    KoAlpaca 모델을 사용하여 채팅 응답 생성
    
    Args:
        user_query (str): 사용자 질문
        knowledge_base (str): 추출된 문서 텍스트
        csv_data (pandas.DataFrame, optional): 처리된 CSV 데이터
        
    Returns:
        str: 챗봇 응답
    """
    try:
        # 모델 관리자 가져오기
        model_manager = KoAlpacaModelManager.get_instance()
        
        # 모델 로드 확인
        if not model_manager.is_loaded:
            if not model_manager.load_model():
                return "KoAlpaca 모델 로드에 실패했습니다. 다시 시도해주세요."

        # 자체 컨텍스트 생성 함수 사용 (chatbot.py에 대한 의존성 제거)
        context = create_context_koalpaca(user_query, knowledge_base, csv_data)
        
        # 명령어와 입력 설정
        instruction = f"당신은 토양 정보 전문가입니다. 다음 정보를 바탕으로 사용자의 토양 관련 질문에 정확하게 답변해주세요."
        
        input_text = f"""
컨텍스트 정보:
{context}

사용자 질문: {user_query}
"""
        
        # KoAlpaca 프롬프트 생성
        prompt = create_koalpaca_prompt(instruction, input_text)
        
        # 응답 생성
        with st.spinner("KoAlpaca 모델이 응답을 생성하는 중..."):
            response = model_manager.generate_response(prompt)
            
        return response
            
    except Exception as e:
        return f"죄송합니다, 오류가 발생했습니다: {str(e)}. 나중에 다시 시도해주세요."