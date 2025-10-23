# Excel読み書き実装ガイド

## 対象ファイル
`utils/excel_handler.py`

## このモジュールの役割
- Excelファイルの読み込み（備考行を保持）
- Excelファイルの書き込み（3シート）
- BytesIOバッファの生成

---

## 実装する関数

### 1. read_excel_with_comment()

#### 目的
備考行（1行目）を保持しながらExcelを読み込む

#### シグネチャ
```python
def read_excel_with_comment(file) -> tuple[pd.DataFrame, str]:
    """
    Excelファイルを読み込み、備考行とデータを返す
    
    Args:
        file: Streamlitのアップロードファイル or ファイルパス
    
    Returns:
        tuple: (DataFrame, 備考行の文字列)
    
    Raises:
        ValueError: ファイル読み込みエラー
    """
```

#### 実装
```python
import pandas as pd
import openpyxl

def read_excel_with_comment(file):
    """
    Excelファイルを読み込み、備考行とデータを返す
    """
    try:
        # openpyxlで備考行を取得
        wb = openpyxl.load_workbook(file)
        ws = wb.active
        comment_row = ws[1][0].value if ws[1][0].value else ""

        # ファイルポインタをリセット（ファイルオブジェクトの場合のみ）
        if hasattr(file, 'seek'):
            file.seek(0)

        # pandasで本データを読み込み（2行目をヘッダー）
        df = pd.read_excel(file, header=1)

        return df, comment_row

    except Exception as e:
        raise ValueError(f"Excelファイルの読み込みエラー: {str(e)}")
```

---

### 2. write_excel_with_sheets()

#### 目的
3つのシートを持つExcelファイルをBytesIOに書き込む

#### シグネチャ
```python
def write_excel_with_sheets(
    sheet1_df: pd.DataFrame,
    sheet1_comment: str,
    sheet2_df: pd.DataFrame,
    sheet2_comment: str,
    sheet3_df: pd.DataFrame,
    sheet3_comment: str
) -> BytesIO:
    """
    3シートのExcelファイルを作成
    
    Args:
        sheet1_df: シート1のDataFrame
        sheet1_comment: シート1の備考行
        sheet2_df: シート2のDataFrame
        sheet2_comment: シート2の備考行
        sheet3_df: シート3のDataFrame
        sheet3_comment: シート3の備考行
    
    Returns:
        BytesIO: Excelファイルのバイナリ
    """
```

#### 実装
```python
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def write_excel_with_sheets(
    sheet1_df, sheet1_comment,
    sheet2_df, sheet2_comment,
    sheet3_df, sheet3_comment
):
    """
    3シートのExcelファイルを作成
    """
    output = BytesIO()

    # まずpandasでベースを作成（1行目に備考行用スペースを空けてデータを書き込む）
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sheet1_df.to_excel(writer, sheet_name='前回データ', index=False, startrow=1)
        sheet2_df.to_excel(writer, sheet_name='今回データ', index=False, startrow=1)
        sheet3_df.to_excel(writer, sheet_name='比較データ', index=False, startrow=1)

    # openpyxlで備考行を1行目に追加
    output.seek(0)
    wb = load_workbook(output)

    # 各シートの1行目に備考行を書き込む
    for sheet_name, comment in [
        ('前回データ', sheet1_comment),
        ('今回データ', sheet2_comment),
        ('比較データ', sheet3_comment)
    ]:
        ws = wb[sheet_name]
        ws['A1'] = comment

    # BytesIOに保存
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return output
```

---

## テストコード例

### tests/test_excel_handler.py
```python
import sys
sys.path.append('..')

from utils.excel_handler import read_excel_with_comment, write_excel_with_sheets
import pandas as pd

def test_read_excel():
    """
    読み込みテスト
    """
    file_path = 'tests/sample_data/sample_前回データ.xlsx'
    
    df, comment = read_excel_with_comment(file_path)
    
    print(f"備考行: {comment}")
    print(f"データ行数: {len(df)}")
    print(f"カラム: {list(df.columns)}")
    print("\n最初の3行:")
    print(df.head(3))
    
    assert len(df) > 0, "データが読み込めていません"
    assert 'stationid' in df.columns, "stationidカラムがありません"

def test_write_excel():
    """
    書き込みテスト
    """
    # サンプルデータ作成
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'C': [5, 6], 'D': [7, 8]})
    df3 = pd.DataFrame({'E': [9, 10], 'F': [11, 12]})
    
    output = write_excel_with_sheets(
        df1, "備考1",
        df2, "備考2",
        df3, "備考3"
    )
    
    # ファイルとして保存（確認用）
    with open('test_output.xlsx', 'wb') as f:
        f.write(output.getvalue())
    
    print("✅ test_output.xlsxに出力されました")

if __name__ == '__main__':
    test_read_excel()
    test_write_excel()
```

---

## 実装時のチェックリスト

- [ ] openpyxl, pandasをimport
- [ ] 備考行を正しく取得（1行目のA列セル）
- [ ] header=1でデータを読み込み
- [ ] BytesIOを使用して出力
- [ ] ファイルポインタを必要に応じてreset（hasattr(file, 'seek')でチェック）
- [ ] エラーハンドリングを実装

---

## 次のステップ

**07_計算モジュール実装ガイド.md を読んで、calculator.pyを実装してください**