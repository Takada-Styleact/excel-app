"""
data_processor.py の動作確認テスト（統合テスト）
"""

import sys
sys.path.append('.')

from modules.data_processor import process_excel_files
import pandas as pd

def test_full_process():
    """
    全処理のテスト（実際のサンプルデータを使用）
    """
    print("=" * 60)
    print("[統合テスト] 全処理フローのテスト")
    print("=" * 60)

    previous_file = 'tests/sample_data/sample_前回データ.xlsx'
    current_file = 'tests/sample_data/sample_今回データ.xlsx'

    print("\n【ステップ1】ファイル読み込み中...")
    print(f"  前回データ: {previous_file}")
    print(f"  今回データ: {current_file}")

    # 処理実行
    print("\n【ステップ2】処理実行中...")
    print("  - 今回データのJ～M列を計算")
    print("  - 前回データと今回データをマッチング")
    print("  - 比較データのH, I列を計算")
    print("  - 3シートのExcelファイルを生成")

    output, stats = process_excel_files(previous_file, current_file)

    print("\n【ステップ3】処理完了！")
    print("\n【処理統計】")
    print(f"  前回データ: {stats['previous_rows']}行")
    print(f"  今回データ: {stats['current_rows']}行")
    print(f"  比較データ: {stats['comparison_rows']}行")
    print(f"  処理日時: {stats['processed_at']}")

    # 統計情報の検証
    print("\n【検証】")
    assert stats['previous_rows'] > 0, "[NG] 前回データが読み込めていません"
    print(f"[OK] 前回データ読み込み成功: {stats['previous_rows']}行")

    assert stats['current_rows'] > 0, "[NG] 今回データが読み込めていません"
    print(f"[OK] 今回データ読み込み成功: {stats['current_rows']}行")

    assert stats['comparison_rows'] > 0, "[NG] 比較データが作成されていません"
    print(f"[OK] 比較データ作成成功: {stats['comparison_rows']}行")

    # 出力ファイルの検証
    print("\n【ステップ4】出力ファイルの検証")
    assert output is not None, "[NG] 出力ファイルが生成されていません"
    assert len(output.getvalue()) > 0, "[NG] 出力ファイルが空です"
    print(f"[OK] 出力ファイル生成成功: {len(output.getvalue())}バイト")

    # ファイル出力（確認用）
    output_filename = 'test_full_output.xlsx'
    with open(output_filename, 'wb') as f:
        f.write(output.getvalue())

    print(f"\n【ステップ5】ファイル保存完了")
    print(f"  ファイル名: {output_filename}")
    print(f"  サイズ: {len(output.getvalue())}バイト")

    # 出力ファイルの内容確認
    print("\n【ステップ6】出力ファイルの内容確認")
    try:
        # シート1: 前回データ
        df_sheet1 = pd.read_excel(output_filename, sheet_name='前回データ', header=1)
        print(f"  シート1（前回データ）: {len(df_sheet1)}行 × {len(df_sheet1.columns)}列")
        print(f"    カラム: {list(df_sheet1.columns[:5])}...")

        # シート2: 今回データ
        df_sheet2 = pd.read_excel(output_filename, sheet_name='今回データ', header=1)
        print(f"  シート2（今回データ）: {len(df_sheet2)}行 × {len(df_sheet2.columns)}列")
        print(f"    カラム: {list(df_sheet2.columns[:5])}...")

        # J～M列の存在確認
        required_cols = ['新築換算平均価格', '新築時平均価格', '中古平均価格', '新築換算ー中古']
        for col in required_cols:
            assert col in df_sheet2.columns, f"[NG] {col}列がありません"
        print(f"    [OK] J～M列の計算結果が含まれています")

        # シート3: 比較データ
        df_sheet3 = pd.read_excel(output_filename, sheet_name='比較データ', header=1)
        print(f"  シート3（比較データ）: {len(df_sheet3)}行 × {len(df_sheet3.columns)}列")
        print(f"    カラム: {list(df_sheet3.columns)}")

        # H, I列の存在確認
        assert '差異' in df_sheet3.columns, "[NG] 差異列がありません"
        assert '値上げ率' in df_sheet3.columns, "[NG] 値上げ率列がありません"
        print(f"    [OK] 差異・値上げ率列が含まれています")

        print("\n[OK] 出力ファイルの内容確認成功")

    except Exception as e:
        print(f"[NG] 出力ファイルの読み込みエラー: {str(e)}")
        raise

    print("\n" + "=" * 60)
    print("[OK] 統合テスト成功！")
    print("=" * 60)
    print(f"\n確認: {output_filename} をExcelで開いて、")
    print("       3シートが正しく作成されているか確認してください。")

if __name__ == '__main__':
    try:
        test_full_process()
    except Exception as e:
        print(f"\n[NG] エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
