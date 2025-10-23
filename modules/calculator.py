"""
計算モジュール

このモジュールは、各種価格計算を担当します。
- 今回データのJ〜M列（新築換算平均価格、新築時平均価格、中古平均価格、新築換算ー中古）
- 比較データのH, I列（差異、値上げ率）
"""

import pandas as pd
import math


def calculate_j_k_l_m_columns(df):
    """
    J〜M列を計算してDataFrameに追加

    Args:
        df: 今回データのDataFrame（F, G, H列を含む）

    Returns:
        J〜M列が追加されたDataFrame
    """
    def calc_price(value):
        """
        坪単価換算

        計算式: value × 0.3025 × 70
        """
        if pd.isna(value) or value == 0:
            return "データなし"
        result = round(value * 0.3025 * 70, 0)
        return int(result)

    # J列: 新築換算平均価格
    df['新築換算平均価格'] = df['priceunitconvnewly'].apply(calc_price)

    # K列: 新築時平均価格
    df['新築時平均価格'] = df['priceunitnewly'].apply(calc_price)

    # L列: 中古平均価格
    df['中古平均価格'] = df['priceunitusedsigned'].apply(calc_price)

    # M列: 新築換算ー中古
    def calc_diff(row):
        """
        新築換算平均価格 - 中古平均価格
        """
        j = row['新築換算平均価格']
        l = row['中古平均価格']
        if j == "データなし" or l == "データなし":
            return "データなし"
        return int(j - l)

    df['新築換算ー中古'] = df.apply(calc_diff, axis=1)

    return df


def calculate_comparison_columns(df):
    """
    比較データのH列（差異）とI列（値上げ率）を計算

    Args:
        df: 比較データのDataFrame
            （前回新築換算平均価格, 今回新築換算平均価格を含む）

    Returns:
        H, I列が追加されたDataFrame
    """
    def calc_diff(row):
        """
        差異計算: 今回 - 前回
        """
        prev = row['前回新築換算平均価格']
        curr = row['今回新築換算平均価格']

        if (prev == "データなし" or curr == "データなし" or
            pd.isna(prev) or pd.isna(curr)):
            return "データなし"

        return int(curr - prev)

    def calc_rate(row):
        """
        値上げ率計算（切り上げ）

        計算式: (今回 / 前回 - 1) × 100
        ※ math.ceil() で切り上げ
        ※ ％記号付きで返す
        """
        prev = row['前回新築換算平均価格']
        curr = row['今回新築換算平均価格']

        if (prev == "データなし" or curr == "データなし" or
            pd.isna(prev) or pd.isna(curr) or prev == 0):
            return "データなし"

        rate = (curr / prev - 1) * 100
        return f"{math.ceil(rate)}%"  # 切り上げ + ％記号

    # H列: 差異
    df['差異'] = df.apply(calc_diff, axis=1)

    # I列: 値上げ率
    df['値上げ率'] = df.apply(calc_rate, axis=1)

    return df
