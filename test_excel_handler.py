"""
excel_handler.py の動作確認テスト
"""

import sys
sys.path.append('.')

from utils.excel_handler import read_excel_with_comment, write_excel_with_sheets
import pandas as pd

def test_read_excel():
    """
    読み込みテスト
    """
    print("=" * 50)
    print("【テスト1】Excelファイルの読み込み")
    print("=" * 50)

    file_path = 'tests/sample_data/sample_前回データ.xlsx'

    df, comment = read_excel_with_comment(file_path)

    print(f"備考行: {comment}")
    print(f"データ行数: {len(df)}")
    print(f"カラム数: {len(df.columns)}")
    print(f"カラム: {list(df.columns[:5])}...")  # 最初の5列のみ表示
    print("\n最初の3行:")
    print(df.head(3))

    assert len(df) > 0, "[NG] データが読み込めていません"
    assert 'stationid' in df.columns, "[NG] stationidカラムがありません"
    assert 'railroad' in df.columns, "[NG] railroadカラムがありません"

    print("\n[OK] 読み込みテスト成功")
    return df, comment

def test_write_excel(df, comment):
    """
    書き込みテスト
    """
    print("\n" + "=" * 50)
    print("【テスト2】Excelファイルの書き込み")
    print("=" * 50)

    # サンプルデータ作成（実際のデータを使用）
    df1 = df.head(5)
    df2 = df.head(5)
    df3 = pd.DataFrame({
        'stationid': [1, 2, 3],
        'name': ['東京', '新宿', '渋谷'],
        'railroad': ['JR山手線', 'JR山手線', 'JR山手線']
    })

    output = write_excel_with_sheets(
        df1, comment,
        df2, "今回データのサンプル",
        df3, "比較データのサンプル"
    )

    # ファイルとして保存（確認用）
    with open('test_output.xlsx', 'wb') as f:
        f.write(output.getvalue())

    print("[OK] test_output.xlsx に出力されました")
    print("[OK] Excelファイルを開いて、3シートが正しく作成されているか確認してください")
    print("   - シート1: 前回データ（5行）")
    print("   - シート2: 今回データ（5行）")
    print("   - シート3: 比較データ（3行）")

if __name__ == '__main__':
    try:
        df, comment = test_read_excel()
        test_write_excel(df, comment)
        print("\n" + "=" * 50)
        print("[OK] すべてのテストが成功しました！")
        print("=" * 50)
    except Exception as e:
        print(f"\n[NG] エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
