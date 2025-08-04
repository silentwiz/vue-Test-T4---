import pandas as pd
import matplotlib.pyplot as plt
import json
import sys
import os
import io
import base64

# 일본어 폰트 설정
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.unicode_minus'] = False

# 파일 경로 설정
base_dir = os.path.dirname(__file__)
# 임시로 answers2.csv를 사용하도록 변경
csv_file_path = os.path.join(base_dir, 'answers2.csv')
questions_file_path = os.path.join(base_dir, 'questions.json')

try:
    # 질문 매핑 파일 읽기
    with open(questions_file_path, 'r', encoding='utf-8') as f:
        question_map = json.load(f)

    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path)

    # userName 열 제외 및 answers.csv에 있는 질문 키만 필터링
    question_keys = [col for col in df.columns if col != 'userName' and col in question_map]

    # 분석할 질문이 없는 경우 처리
    if not question_keys:
        print(json.dumps({"message": "分析する項目がありません"}))
        sys.exit(0)

    # 그래프 생성
    fig, axes = plt.subplots(len(question_keys), 1, figsize=(10, len(question_keys) * 5), squeeze=False)

    for i, key in enumerate(question_keys):
        ax = axes[i, 0]

        # 'interfaces' 열은 여러 값이 ';'로 구분되어 있으므로 특별 처리
        if key == 'interfaces':
            counts = df[key].dropna().str.split(';').explode().str.strip().value_counts()
        else:
            counts = df[key].dropna().value_counts()

        question_title = question_map.get(key, key)

        if counts.empty:
            ax.set_title(f'{question_title}', fontsize=12)
            ax.text(0.5, 0.5, 'データがありません。', ha='center', va='center', transform=ax.transAxes)
            ax.set_axis_off() # 데이터가 없으면 축을 숨김
        else:
            answer_labels = set(counts.index.map(lambda x: str(x).strip()))

            # 답변이 'はい'와 'いいえ'로만 구성되어 있는지 확인
            if answer_labels.issubset({'はい', 'いいえ'}):
                # 원 그래프 생성
                colors = ['#0072B2' if label == 'はい' else '#D55E00' for label in counts.index]
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})
                ax.set_title(f'{question_title}', fontsize=14, pad=20)
                ax.axis('equal')  # 원형을 유지
            else:
                # 막대 그래프 생성 (기존 로직)
                color_palette = ['#009E73', '#F0E442', '#CC79A7', '#56B4E9', '#999999']
                colors = []
                other_answers = [label for label in counts.index if str(label).strip() not in ['はい', 'いいえ']]
                other_color_map = {answer: color_palette[i % len(color_palette)] for i, answer in enumerate(other_answers)}

                for label in counts.index:
                    stripped_label = str(label).strip()
                    if stripped_label == 'はい':
                        colors.append('#0072B2')
                    elif stripped_label == 'いいえ':
                        colors.append('#D55E00')
                    else:
                        colors.append(other_color_map.get(label, '#999999'))

                counts.plot(kind='barh', ax=ax, color=colors)
                ax.set_title(f'{question_title}', fontsize=12)
                ax.set_xlabel('回答数')
                ax.set_ylabel('')
                ax.tick_params(axis='y', labelsize=10)

    plt.tight_layout(pad=3.0) # 그래프 간 간격 조정

    # 이미지를 메모리 내 버퍼에 저장
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Base64로 인코딩
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # JSON으로 출력
    print(json.dumps({"plotImage": image_base64}))

except FileNotFoundError:
    print(json.dumps({"error": f"answers.csvが見つかりません。 ({csv_file_path})"}))
    sys.exit(1)
except pd.errors.EmptyDataError:
    print(json.dumps({"message": "まだ誰もアンケートに答えていません。"}))
    sys.exit(0)
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
