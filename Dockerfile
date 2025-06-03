# 1) 베이스 이미지: 경량 Python 3.11
FROM python:3.11-slim

# 2) 컨테이너 내부 작업 디렉터리 설정
WORKDIR /app

# 3) 로컬 requirements.txt 복사 후 pip install (캐시 없이 설치)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) (선택) rembg 모델 캐시를 미리 생성하려면 주석 해제
# RUN python - <<EOF
# from rembg import new_session
# new_session("silueta")
# EOF

# 5) 애플리케이션 코드 복사
COPY remove_bg.py .

# 6) 환경 변수 설정 (PORT는 Render가 자동으로 주입)
ENV PORT 5000

# CMD를 배열 형태가 아닌 sh -c "..." 형태로 바꾸면, $PORT를 해석합니다.
CMD ["sh", "-c", "gunicorn remove_bg:app --bind 0.0.0.0:$PORT --workers 1"]
