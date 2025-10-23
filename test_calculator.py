"""
calculator.py の動作確認テスト
"""

import sys
sys.path.append('.')

from modules.calculator import calculate_j_k_l_m_columns, calculate_comparison_columns
import pandas as pd

def test_j_k_l_m():
    """
    J〜M列の計算テスト
    """
    print("=" * 50)
    print("[テスト1] J～M列の計算")
    print("=" * 50)

    # テストデータ
    df = pd.DataFrame({
        'stationid': [1, 2, 3, 4],
        'priceunitconvnewly': [450000, 0, None, 500000],
        'priceunitnewly': [500000, 550000, None, 520000],
        'priceunitusedsigned': [380000, 420000, None, 400000]
    })

    print("\n【入力データ】")
    print(df)

    result_df = calculate_j_k_l_m_columns(df)

    print("\n【出力データ】")
    print(result_df[['stationid', '新築換算平均価格', '新築時平均価格', '中古平均価格', '新築換算ー中古']])

    # 検証
    print("\n【検証】")

    # stationid=1（正常計算）
    j_value = result_df.loc[0, '新築換算平均価格']
    expected = int(round(450000 * 0.3025 * 70, 0))
    print(f"stationid=1 のJ列: {j_value} (期待値: {expected})")
    assert j_value == expected, f"[NG] J列計算エラー: {j_value} != {expected}"
    print("[OK] J列計算成功")

    # stationid=2（0のエラー処理）
    j_value_2 = result_df.loc[1, '新築換算平均価格']
    print(f"stationid=2 のJ列: {j_value_2} (期待値: データなし)")
    assert j_value_2 == "データなし", "[NG] 0のエラー処理エラー"
    print("[OK] 0のエラー処理成功")

    # stationid=3（NaNのエラー処理）
    j_value_3 = result_df.loc[2, '新築換算平均価格']
    print(f"stationid=3 のJ列: {j_value_3} (期待値: データなし)")
    assert j_value_3 == "データなし", "[NG] NaNのエラー処理エラー"
    print("[OK] NaNのエラー処理成功")

    # M列の計算チェック（stationid=1）
    m_value = result_df.loc[0, '新築換算ー中古']
    j_val = result_df.loc[0, '新築換算平均価格']
    l_val = result_df.loc[0, '中古平均価格']
    expected_m = int(j_val - l_val)
    print(f"stationid=1 のM列: {m_value} (期待値: {expected_m})")
    assert m_value == expected_m, f"[NG] M列計算エラー: {m_value} != {expected_m}"
    print("[OK] M列計算成功")

    print("\n[OK] J～M列のテスト成功")
    return result_df

def test_comparison():
    """
    比較データの計算テスト
    """
    print("\n" + "=" * 50)
    print("[テスト2] 比較データの計算（差異・値上げ率）")
    print("=" * 50)

    # テストデータ
    df = pd.DataFrame({
        'stationid': [1, 2, 3, 4, 5],
        '前回新築換算平均価格': [9000000, 9000000, "データなし", 9000000, 0],
        '今回新築換算平均価格': [9500000, 9000000, 9500000, 9001000, 9500000]
    })

    print("\n【入力データ】")
    print(df)

    result_df = calculate_comparison_columns(df)

    print("\n【出力データ】")
    print(result_df[['stationid', '前回新築換算平均価格', '今回新築換算平均価格', '差異', '値上げ率']])

    # 検証
    print("\n【検証】")

    # stationid=1（差異計算）
    diff = result_df.loc[0, '差異']
    expected_diff = 500000
    print(f"stationid=1 の差異: {diff} (期待値: {expected_diff})")
    assert diff == expected_diff, f"[NG] 差異計算エラー: {diff} != {expected_diff}"
    print("[OK] 差異計算成功")

    # stationid=1（値上げ率計算：切り上げ）
    rate = result_df.loc[0, '値上げ率']
    # 9500000 / 9000000 - 1 = 0.0555... → 5.555...% → 切り上げで6%
    expected_rate = 6
    print(f"stationid=1 の値上げ率: {rate}% (期待値: {expected_rate}%)")
    assert rate == expected_rate, f"[NG] 値上げ率（切り上げ）エラー: {rate} != {expected_rate}"
    print("[OK] 値上げ率（切り上げ）成功")

    # stationid=2（変化なし）
    rate_2 = result_df.loc[1, '値上げ率']
    expected_rate_2 = 0
    print(f"stationid=2 の値上げ率: {rate_2}% (期待値: {expected_rate_2}%)")
    assert rate_2 == expected_rate_2, f"[NG] 値上げ率エラー: {rate_2} != {expected_rate_2}"
    print("[OK] 変化なしケース成功")

    # stationid=3（データなし処理）
    diff_3 = result_df.loc[2, '差異']
    print(f"stationid=3 の差異: {diff_3} (期待値: データなし)")
    assert diff_3 == "データなし", "[NG] エラー処理エラー"
    print("[OK] データなし処理成功")

    # stationid=4（小数点切り上げ）
    rate_4 = result_df.loc[3, '値上げ率']
    # 9001000 / 9000000 - 1 = 0.0001111... → 0.01111...% → 切り上げで1%
    expected_rate_4 = 1
    print(f"stationid=4 の値上げ率: {rate_4}% (期待値: {expected_rate_4}%)")
    assert rate_4 == expected_rate_4, f"[NG] 小数点切り上げエラー: {rate_4} != {expected_rate_4}"
    print("[OK] 小数点切り上げ成功")

    # stationid=5（0除算のエラー処理）
    rate_5 = result_df.loc[4, '値上げ率']
    print(f"stationid=5 の値上げ率: {rate_5} (期待値: データなし)")
    assert rate_5 == "データなし", "[NG] 0除算のエラー処理エラー"
    print("[OK] 0除算のエラー処理成功")

    print("\n[OK] 比較データのテスト成功")

if __name__ == '__main__':
    try:
        test_j_k_l_m()
        test_comparison()
        print("\n" + "=" * 50)
        print("[OK] すべてのテストが成功しました！")
        print("=" * 50)
    except Exception as e:
        print(f"\n[NG] エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
