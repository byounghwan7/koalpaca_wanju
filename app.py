
import streamlit as st
import os
import sys

# 이 파일은 Streamlit Cloud 배포를 위한 진입점입니다.
if __name__ == "__main__":
    print("KoAlpaca 토양 정보 챗봇을 시작합니다...")
    
    # app_koalpaca.py 실행
    import subprocess
    subprocess.run(["streamlit", "run", "app_koalpaca.py", "--server.port=5000", "--server.address=0.0.0.0"])
    