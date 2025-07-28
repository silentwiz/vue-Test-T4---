import sys
import json
import random
from datetime import datetime
import io 
import base64 
import matplotlib.pyplot as plt 

plt.switch_backend('Agg') 

def main():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 1, 5, 3]

    fig, ax = plt.subplots() 
    ax.plot(x, y)
    ax.set_title("Sample Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    # 3. 그래프를 BytesIO 객체에 PNG 형식으로 저장 (파일로 저장하지 않음)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig) # 그래프를 그린 후에는 항상 닫아서 메모리 누수 방지

    # 4. BytesIO 객체의 내용을 Base64 문자열로 인코딩
    buf.seek(0) # 버퍼의 시작으로 커서 이동
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # 5. 응답 데이터에 Base64 이미지 문자열 포함
    data_to_return = {
        "message": "python load success",
        "nowTime": str(datetime.now()),
        "randomNumber": random.randint(1000, 9999),
        "plotImage": image_base64 # 그래프 이미지 Base64 문자열 추가
    }
    
    print(json.dumps(data_to_return))

if __name__ == '__main__':
    main()