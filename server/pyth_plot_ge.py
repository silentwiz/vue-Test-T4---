import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import json
import sys
import os
import io
import base64

plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.unicode_minus'] = False

base_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(base_dir, 'answers.csv')
questions_file_path = os.path.join(base_dir, 'questions.json')

try:
    with open(questions_file_path, 'r', encoding='utf-8') as f:
        question_map = json.load(f)

    df = pd.read_csv(csv_file_path)
    question_keys = [col for col in df.columns if col != 'userName' and col in question_map]
    if not question_keys:
        print(json.dumps({"message": "分析する項目がありません"}))
        sys.exit(0)
    
    # 그래프 크기를 매우 크게 설정 - 웹에서 읽기 쉽도록
    fig, axes = plt.subplots(len(question_keys), 1, figsize=(20, len(question_keys) * 9), squeeze=False)
    
    # 서브플롯 간격을 매우 크게 조정
    plt.subplots_adjust(hspace=1.2)

    for i, key in enumerate(question_keys):
        ax = axes[i, 0]

        if key == 'interfaces':
            counts = df[key].dropna().str.split(';').explode().str.strip().value_counts()
        else:
            counts = df[key].dropna().value_counts()

        question_title = question_map.get(key, key)

        if counts.empty:
            ax.set_title(f'{question_title}', fontsize=24, pad=30, fontweight='bold')
            ax.text(0.5, 0.5, 'データがありません。', ha='center', va='center', transform=ax.transAxes, fontsize=20)
            ax.set_axis_off()
        else:
            answer_labels = set(counts.index.map(lambda x: str(x).strip()))

            if answer_labels.issubset({'はい', 'いいえ'}):
                colors = ['#0072B2' if label == 'はい' else '#D55E00' for label in counts.index]
                
                wedges, texts, autotexts = ax.pie(counts, labels=counts.index, autopct='%1.1f%%', 
                                                 startangle=90, colors=colors, 
                                                 textprops={'fontsize': 18},
                                                 radius=0.8)  # 파이차트 크기 증가
                
                for autotext in autotexts:
                    autotext.set_fontsize(20)
                    autotext.set_fontweight('bold')
                    autotext.set_color('white')
                
                for text in texts:
                    text.set_fontsize(18)
                    text.set_fontweight('bold')
                
                ax.set_title(f'{question_title}', fontsize=24, pad=50, fontweight='bold')
                ax.axis('equal')
            else:
                # 색상 팔레트
                color_palette = [
                    '#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377', 
                    '#BBBBBB', '#88CCEE', '#44AA99', '#999933', '#AA4499', '#DDCC77'
                ]
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
                        colors.append(other_color_map.get(label, '#BBBBBB'))
                        
                bars = ax.barh(range(len(counts)), counts.values, color=colors)
                
                ax.set_yticks(range(len(counts)))
                ax.set_yticklabels(counts.index, fontsize=16, fontweight='bold')
                
                ax.set_title(f'{question_title}', fontsize=24, pad=40, fontweight='bold')
                ax.set_xlabel('回答数', fontsize=18, fontweight='bold')
                ax.tick_params(axis='x', labelsize=16)
                
                ax.grid(axis='x', linestyle='--', alpha=0.6, zorder=0)
                ax.set_axisbelow(True)

                for j, (bar, value) in enumerate(zip(bars, counts.values)):
                    ax.text(value + max(counts.values) * 0.01, 
                           bar.get_y() + bar.get_height() / 2, 
                           f'{int(value)}', 
                           va='center', 
                           ha='left', 
                           fontsize=18,
                           fontweight='bold')
                
                ax.set_xlim(0, max(counts.values) * 1.15)
                ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    
    plt.tight_layout(pad=6.0)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.2)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close() 
    
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