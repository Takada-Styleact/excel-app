"""
マッチング処理モジュール

このモジュールは、前回データと今回データのマッチング処理を担当します。
- stationid + railroad でマッチングキーを生成
- 外部結合により両方のデータを保持
- 比較用DataFrameの作成
"""

import pandas as pd


def create_comparison_dataframe(previous_df, current_df):
    """
    前回データと今回データをマッチングして比較用DataFrameを作成

    Args:
        previous_df: 前回データ（J列を含む）
        current_df: 今回データ（J列を含む）

    Returns:
        比較用DataFrame（A〜G列を含む）
    """
    # 1. マッチングキーを作成
    previous_df = previous_df.copy()
    current_df = current_df.copy()

    previous_df['match_key'] = (
        previous_df['stationid'].astype(str) + '_' +
        previous_df['railroad'].astype(str)
    )
    current_df['match_key'] = (
        current_df['stationid'].astype(str) + '_' +
        current_df['railroad'].astype(str)
    )

    # 2. 必要なカラムのみ抽出
    prev_cols = ['match_key', 'stationid', 'name', 'railroad2', 'railroad', 'cityid', '新築換算平均価格']
    curr_cols = ['match_key', 'stationid', 'name', 'railroad2', 'railroad', 'cityid', '新築換算平均価格']

    prev_subset = previous_df[prev_cols].copy()
    curr_subset = current_df[curr_cols].copy()

    # 3. 外部結合（両方のデータを保持）
    merged_df = pd.merge(
        prev_subset,
        curr_subset,
        on='match_key',
        how='outer',
        suffixes=('_prev', '_curr')
    )

    # 4. カラムを整理
    # 基本情報は今回データ優先、なければ前回データ
    comparison_df = pd.DataFrame()
    comparison_df['stationid'] = merged_df['stationid_curr'].fillna(merged_df['stationid_prev'])
    comparison_df['name'] = merged_df['name_curr'].fillna(merged_df['name_prev'])
    comparison_df['railroad2'] = merged_df['railroad2_curr'].fillna(merged_df['railroad2_prev'])
    comparison_df['railroad'] = merged_df['railroad_curr'].fillna(merged_df['railroad_prev'])
    comparison_df['cityid'] = merged_df['cityid_curr'].fillna(merged_df['cityid_prev'])

    # 価格データ
    comparison_df['前回新築換算平均価格'] = merged_df['新築換算平均価格_prev']
    comparison_df['今回新築換算平均価格'] = merged_df['新築換算平均価格_curr']

    # 5. NaNを「データなし」に変換（価格列のみ）
    comparison_df['前回新築換算平均価格'] = comparison_df['前回新築換算平均価格'].fillna("データなし")
    comparison_df['今回新築換算平均価格'] = comparison_df['今回新築換算平均価格'].fillna("データなし")

    return comparison_df
