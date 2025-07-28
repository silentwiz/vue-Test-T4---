import pandas as pd
import sys

def read_csv_content_by_header(file_path):
    """
    CSV 파일의 각 헤더(열)에 해당하는 내용을 순차적으로 출력합니다.

    Args:
        file_path (str): CSV 파일의 경로.
    """
    try:
        # CSV 파일을 읽습니다. 첫 번째 행을 헤더로 인식합니다.
        df = pd.read_csv(file_path)
        
        print(f"CSV 파일 '{file_path}'의 내용 (헤더별):")
        print("-" * 50)

        # 각 컬럼(헤더)에 대해 반복합니다.
        for column_name in df.columns:
            print(f"- {column_name}")
            # 해당 컬럼의 모든 값을 반복하며 출력합니다.
            for value in df[column_name]:
                # 값에 줄바꿈이나 공백이 많을 경우를 대비하여 .strip() 사용
                # None 또는 NaN 값은 'None'으로 표시
                display_value = str(value).strip() if pd.notna(value) else "None"
                print(f"  {display_value}")
            print("-" * 50) # 각 헤더 내용 구분선
            
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다. 경로를 확인해 주세요: {file_path}", file=sys.stderr)
    except pd.errors.EmptyDataError:
        print(f"오류: CSV 파일이 비어 있습니다: {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}", file=sys.stderr)

if __name__ == "__main__":
    # answers.csv 파일의 경로를 지정합니다.
    # 이 스크립트가 server.cjs와 같은 디렉토리에 있다고 가정합니다.
    csv_file_path = 'answers.csv' 
    
    read_csv_content_by_header(csv_file_path)
