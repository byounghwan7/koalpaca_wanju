# Streamlit Cloud 배포 가이드 (KoAlpaca 토양 챗봇)

이 가이드는 KoAlpaca 기반 토양 정보 챗봇을 Streamlit Cloud에 배포하는 방법을 설명합니다.

## 1. GitHub 저장소 준비

1. GitHub 계정에 새 저장소를 생성합니다.
2. 다음 파일들을 저장소에 업로드합니다:
   - `app_koalpaca.py` (메인 Streamlit 애플리케이션)
   - `koalpaca_chatbot.py` (KoAlpaca 챗봇 구현)
   - `pdf_processor.py` (PDF 처리 모듈)
   - `csv_processor.py` (CSV 처리 모듈)
   - `utils.py` (유틸리티 함수)
   - `requirements.txt` (이 프로젝트의 `streamlit_cloud_requirements.txt` 파일을 이름 변경)
   - `.streamlit/config.toml` (Streamlit 설정)
   - `data/` 폴더 (데이터 파일, 필요한 경우)

## 2. 데이터 파일 준비

1. 다음 파일을 `data/` 폴더에 업로드합니다:
   - `KSIC_9rd_handbook.pdf`
   - `chatbot_wanju.csv`

   또는 GitHub의 용량 제한으로 인해 PDF나 대용량 파일이 문제가 된다면:
   
   - 코드에서 데이터 파일 경로를 수정하여 `attached_assets/` 대신 `data/` 폴더를 사용하게 합니다.
   - 큰 파일의 경우 외부 저장소(Google Drive, AWS S3 등)에 업로드하고 애플리케이션 시작 시 다운로드할 수 있습니다.

## 3. Streamlit Cloud 설정

1. [Streamlit Cloud](https://streamlit.io/cloud)에 로그인합니다.
2. "Deploy an app" 버튼을 클릭합니다.
3. GitHub 저장소를 연결하고 다음 정보를 입력합니다:
   - Repository: 여러분의 GitHub 저장소 URL
   - Branch: main (또는 배포하려는 브랜치)
   - Main file path: `app_koalpaca.py`
   - Python 버전 선택: 3.10

4. Advanced Settings에서:
   - 필요한 경우 비밀 환경 변수를 설정합니다.
   - 필요하면 패키지 의존성이 설치될 때까지 기다리는 시간을 늘립니다.

5. "Deploy!" 버튼을 클릭합니다.

## 4. 배포 후 확인

1. 배포가 완료되면 제공된 URL로 애플리케이션에 접근할 수 있습니다.
2. 모든 기능이 예상대로 작동하는지 확인합니다:
   - 모델 로드 기능
   - 질문 응답 기능
   - PDF 및 CSV 데이터 처리

## 5. 문제 해결

1. 배포 로그를 확인하여 오류를 찾습니다.
2. 가장 흔한 문제:
   - 의존성 설치 실패: `requirements.txt`에 누락된 패키지가 있는지 확인합니다.
   - 파일 경로 오류: 파일 경로가 올바른지 확인합니다.

## 6. 맞춤 설정 (선택사항)

1. 도메인 연결: Streamlit Cloud에서 Custom Domain 설정을 통해 자신만의 도메인을 연결할 수 있습니다.
2. 주기적인 업데이트: GitHub 저장소를 업데이트하면 Streamlit Cloud는 자동으로 앱을 재배포합니다.

---

## 참고: GitHub에 업로드하기 전 수정할 사항들

1. `app_koalpaca.py`에서 데이터 파일 경로 수정:
   ```python
   # 변경 전
   pdf_path = "attached_assets/KSIC_9rd_handbook.pdf"
   csv_path = "attached_assets/chatbot_wanju.csv"
   
   # 변경 후
   pdf_path = "data/KSIC_9rd_handbook.pdf"
   csv_path = "data/chatbot_wanju.csv"
   ```

2. `use_column_width` 매개변수를 `use_container_width`로 변경 (경고 메시지 제거):
   ```python
   # 변경 전
   sample_cols[i % 2].image(url, use_column_width=True, caption=f"토양 샘플 {i+1}")
   
   # 변경 후
   sample_cols[i % 2].image(url, use_container_width=True, caption=f"토양 샘플 {i+1}")
   ```

3. 실제 배포를 위해서 KoAlpaca 모델 관련 코드를 수정하여 실제 모델을 사용할지, 현재처럼 시뮬레이션 모드로 실행할지 결정해야 합니다.