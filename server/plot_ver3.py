import pandas as pd
import os
import matplotlib.pyplot as plt
import japanize_matplotlib
import io
import base64
import json
from collections import Counter

# Get the absolute path to the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the CSV file
path_csv = os.path.join(script_dir, 'answers.csv')

def create_pie_chart(df, column_name, order, colors):
    """Creates a pie chart from a given DataFrame column and returns a base64 encoded image."""
    if column_name not in df.columns:
        return None
    
    counts = df[column_name].value_counts()
    word_count = [counts.get(label, 0) for label in order]
    
    plt.figure(figsize=(4, 4))
    plt.pie(word_count, labels=order, autopct='%1.1f%%', startangle=90, counterclock=False, colors=colors)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title(f"{column_name} の結果")
    plt.axis('equal')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return img_base64

def create_bar_chart(df, column_name, order, colors):
    """Creates a bar chart from a given DataFrame column and returns a base64 encoded image."""
    if column_name not in df.columns:
        return None
        
    word_count = df[column_name].value_counts().reindex(order).fillna(0)
    
    plt.figure(figsize=(10, 6))
    plt.bar(word_count.index, word_count.values, color=colors)
    plt.title(f"「{column_name}」列の出現回数")
    plt.xlabel(column_name)
    plt.ylabel("出現回数")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return img_base64

def create_interfaces_bar_chart(df, column_name, colors):
    """Creates a bar chart for the 'interfaces' column and returns a base64 encoded image."""
    if column_name not in df.columns:
        return None

    interface_series = df[column_name].dropna()
    all_interfaces = []
    for item in interface_series:
        parts = [part.strip() for part in str(item).split(',')]
        all_interfaces.extend(parts)

    interface_counts = Counter(all_interfaces)
    sorted_counts = dict(sorted(interface_counts.items(), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_counts.keys(), sorted_counts.values(), color=colors[:len(sorted_counts)])
    plt.xlabel('Interfaces')
    plt.ylabel('Count')
    plt.title('Frequency of Each Interface')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return img_base64

def main():
    """Main function to generate all plots and print as JSON."""
    try:
        # Define column names to handle rows with extra commas, based on the max number of fields observed
        column_names = [
            'userName', 'needSupport', 'specificSituation', 'isSocial', 'whoneed',
            'interfaces', 'needMaintenance', 'precisionOrStrength', 'otherComments',
            'extra1', 'extra2', 'extra3'
        ]
        # Read CSV, skipping the original header row and using our defined column names
        # This prevents errors from lines with more fields than the header
        df = pd.read_csv(path_csv, encoding='utf-8-sig', names=column_names, skiprows=1)
    except FileNotFoundError:
        print(json.dumps({"error": f"CSV file not found at {path_csv}"}))
        return
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return

    images = {}

    # Generate charts
    images['needSupport'] = create_pie_chart(df, 'needSupport', ['はい', 'いいえ'], ['red', 'blue'])
    images['specificSituation'] = create_bar_chart(df, 'specificSituation', ['学校', '職場', '工場', '公園', '病院', '家', '空'], ['red', 'blue', 'green', 'orange', 'purple', 'black', 'gray'])
    images['needInterfaces'] = create_pie_chart(df, 'needInterfaces', ['はい', 'いいえ', '分からない'], ['red', 'blue', 'yellow'])
    images['interfaces'] = create_interfaces_bar_chart(df, 'interfaces', ['red', 'blue', 'green', 'orange', 'purple', 'black'])
    images['societalNecessity'] = create_pie_chart(df, 'societalNecessity', ['はい', 'いいえ', '分からない'], ['red', 'blue', 'yellow'])
    images['needMaintenance'] = create_pie_chart(df, 'needMaintenance', ['はい', 'いいえ'], ['red', 'blue'])
    images['isSocial'] = create_pie_chart(df, 'isSocial', ['はい', 'いいえ'], ['red', 'blue'])

    # Print all images as a single JSON object
    print(json.dumps(images, indent=4))

if __name__ == '__main__':
    main()