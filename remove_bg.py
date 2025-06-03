from flask import Flask, request, send_file, abort
from rembg import remove, new_session
from flask_cors import CORS
import io, os

app = Flask(__name__)
CORS(app)

@app.route("/remove-background", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return {"error": "No image file provided"}, 400

    file = request.files["image"]
    app.logger.info(f"Received file: {file.filename}")
    if file.filename == "":
        return {"error": "No selected file"}, 400

    # 1) 입력 이미지 바이트 읽기
    img_bytes = file.read()

    model_name = "u2net"  # 여기에 모델 이름을 넣자
    session = new_session(model_name)

    # 2) rembg 로 배경 제거 (bytes → bytes)
    result_bytes = remove(img_bytes, session=session)

    # 3) BytesIO 로 감싸기
    buf = io.BytesIO(result_bytes)
    buf.seek(0)

    # 4) 원본 파일명에서 확장자 제거하고, .png 로 다운로드 이름 지정
    name, _ = os.path.splitext(file.filename)
    download_name = f"{name}.png"  # rembg 결과는 투명 배경 PNG

    # 5) send_file 로 응답
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=True,
        download_name=download_name
    )

if __name__ == "__main__":
    app.run(debug=True)
