"""
matcher.py の動作確認テスト
"""

import sys
sys.path.append('.')

from modules.matcher import create_comparison_dataframe
import pandas as pd

def test_matching():
    """
    マッチング処理のテスト
    """
    print("=" * 50)
    print("[テスト] マッチング処理")
    print("=" * 50)

    # 前回データ
    previous_df = pd.DataFrame({
        'stationid': [1, 2],
        'name': ['東京', '新宿'],
        'railroad2': ['JR', 'JR'],
        'railroad': ['JR山手線', 'JR山手線'],
        'cityid': [13101, 13104],
        '新築換算平均価格': [9000000, 8500000]
    })

    # 今回データ
    current_df = pd.DataFrame({
        'stationid': [1, 3],
        'name': ['東京', '渋谷'],
        'railroad2': ['JR', 'JR'],
        'railroad': ['JR山手線', 'JR山手線'],
        'cityid': [13101, 13113],
        '新築換算平均価格': [9500000, 9200000]
    })

    print("\n【前回データ】")
    print(previous_df)

    print("\n【今回データ】")
    print(current_df)

    # マッチング実行
    comparison_df = create_comparison_dataframe(previous_df, current_df)

    print("\n【比較データ（マッチング結果）】")
    print(comparison_df)

    # 検証
    print("\n【検証】")

    # レコード数チェック
    expected_rows = 3  # 両方存在(1) + 前回のみ(2) + 今回のみ(3) = 3
    actual_rows = len(comparison_df)
    print(f"レコード数: {actual_rows} (期待値: {expected_rows})")
    assert actual_rows == expected_rows, f"[NG] レコード数エラー: {actual_rows} != {expected_rows}"
    print("[OK] レコード数チェック成功")

    # stationid=1（両方存在）
    row1 = comparison_df[comparison_df['stationid'] == 1].iloc[0]
    print(f"\nstationid=1（両方存在）:")
    print(f"  前回価格: {row1['前回新築換算平均価格']} (期待値: 9000000)")
    print(f"  今回価格: {row1['今回新築換算平均価格']} (期待値: 9500000)")
    assert row1['前回新築換算平均価格'] == 9000000, "[NG] 前回価格エラー"
    assert row1['今回新築換算平均価格'] == 9500000, "[NG] 今回価格エラー"
    print("[OK] 両方存在ケース成功")

    # stationid=2（前回のみ）
    row2 = comparison_df[comparison_df['stationid'] == 2].iloc[0]
    print(f"\nstationid=2（前回のみ）:")
    print(f"  前回価格: {row2['前回新築換算平均価格']} (期待値: 8500000)")
    print(f"  今回価格: {row2['今回新築換算平均価格']} (期待値: データなし)")
    assert row2['前回新築換算平均価格'] == 8500000, "[NG] 前回価格エラー"
    assert row2['今回新築換算平均価格'] == "データなし", "[NG] 今回価格エラー（データなしのはず）"
    print("[OK] 前回のみケース成功")

    # stationid=3（今回のみ）
    row3 = comparison_df[comparison_df['stationid'] == 3].iloc[0]
    print(f"\nstationid=3（今回のみ）:")
    print(f"  前回価格: {row3['前回新築換算平均価格']} (期待値: データなし)")
    print(f"  今回価格: {row3['今回新築換算平均価格']} (期待値: 9200000)")
    assert row3['前回新築換算平均価格'] == "データなし", "[NG] 前回価格エラー（データなしのはず）"
    assert row3['今回新築換算平均価格'] == 9200000, "[NG] 今回価格エラー"
    print("[OK] 今回のみケース成功")

    # 基本情報の引き継ぎ確認
    print(f"\nstationid=2 の名前: {row2['name']} (期待値: 新宿)")
    assert row2['name'] == '新宿', "[NG] 前回データからの基本情報引き継ぎエラー"
    print("[OK] 前回データからの基本情報引き継ぎ成功")

    print(f"stationid=3 の名前: {row3['name']} (期待値: 渋谷)")
    assert row3['name'] == '渋谷', "[NG] 今回データからの基本情報引き継ぎエラー"
    print("[OK] 今回データからの基本情報引き継ぎ成功")

    print("\n[OK] マッチング処理のテスト成功")

def test_matching_with_complex_keys():
    """
    複雑なマッチングキーのテスト
    """
    print("\n" + "=" * 50)
    print("[テスト2] 複雑なマッチングキー")
    print("=" * 50)

    # 前回データ
    previous_df = pd.DataFrame({
        'stationid': [1, 1, 2],
        'name': ['東京A', '東京B', '新宿'],
        'railroad2': ['JR', 'メトロ', 'JR'],
        'railroad': ['JR山手線', '東京メトロ丸ノ内線', 'JR山手線'],
        'cityid': [13101, 13101, 13104],
        '新築換算平均価格': [9000000, 8000000, 8500000]
    })

    # 今回データ
    current_df = pd.DataFrame({
        'stationid': [1, 1],
        'name': ['東京A', '東京B'],
        'railroad2': ['JR', 'メトロ'],
        'railroad': ['JR山手線', '東京メトロ丸ノ内線'],
        'cityid': [13101, 13101],
        '新築換算平均価格': [9500000, 8500000]
    })

    print("\n【前回データ】")
    print(previous_df)

    print("\n【今回データ】")
    print(current_df)

    # マッチング実行
    comparison_df = create_comparison_dataframe(previous_df, current_df)

    print("\n【比較データ（マッチング結果）】")
    print(comparison_df[['stationid', 'name', 'railroad', '前回新築換算平均価格', '今回新築換算平均価格']])

    # 検証
    print("\n【検証】")

    # レコード数チェック（両方2つ + 前回のみ1つ = 3）
    expected_rows = 3
    actual_rows = len(comparison_df)
    print(f"レコード数: {actual_rows} (期待値: {expected_rows})")
    assert actual_rows == expected_rows, f"[NG] レコード数エラー: {actual_rows} != {expected_rows}"
    print("[OK] レコード数チェック成功")

    # stationid=1, railroad=JR山手線
    row_jr = comparison_df[
        (comparison_df['stationid'] == 1) &
        (comparison_df['railroad'] == 'JR山手線')
    ].iloc[0]
    print(f"\nstationid=1, railroad=JR山手線:")
    print(f"  前回価格: {row_jr['前回新築換算平均価格']}")
    print(f"  今回価格: {row_jr['今回新築換算平均価格']}")
    assert row_jr['前回新築換算平均価格'] == 9000000, "[NG] JR山手線の前回価格エラー"
    assert row_jr['今回新築換算平均価格'] == 9500000, "[NG] JR山手線の今回価格エラー"
    print("[OK] JR山手線のマッチング成功")

    # stationid=1, railroad=東京メトロ丸ノ内線
    row_metro = comparison_df[
        (comparison_df['stationid'] == 1) &
        (comparison_df['railroad'] == '東京メトロ丸ノ内線')
    ].iloc[0]
    print(f"\nstationid=1, railroad=東京メトロ丸ノ内線:")
    print(f"  前回価格: {row_metro['前回新築換算平均価格']}")
    print(f"  今回価格: {row_metro['今回新築換算平均価格']}")
    assert row_metro['前回新築換算平均価格'] == 8000000, "[NG] 東京メトロの前回価格エラー"
    assert row_metro['今回新築換算平均価格'] == 8500000, "[NG] 東京メトロの今回価格エラー"
    print("[OK] 東京メトロのマッチング成功")

    print("\n[OK] 複雑なマッチングキーのテスト成功")

if __name__ == '__main__':
    try:
        test_matching()
        test_matching_with_complex_keys()
        print("\n" + "=" * 50)
        print("[OK] すべてのテストが成功しました！")
        print("=" * 50)
    except Exception as e:
        print(f"\n[NG] エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
