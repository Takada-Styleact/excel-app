"""
メイン処理モジュール

このモジュールは、全モジュールを統合してメイン処理フローを制御します。
- ファイル読み込み → 計算 → マッチング → 出力の一連の流れ
- 処理統計情報の返却
- 異常値の抽出（±20%以上）
"""

from io import BytesIO
from datetime import datetime
import pandas as pd
from utils.excel_handler import read_excel_with_comment, write_excel_with_sheets
from modules.calculator import calculate_j_k_l_m_columns, calculate_comparison_columns
from modules.matcher import create_comparison_dataframe


def extract_abnormal_values(comparison_df, threshold=20):
    """
    比較データから異常値（±threshold%以上）を抽出

    Args:
        comparison_df: 比較データのDataFrame
        threshold: 閾値（デフォルト: 20%）

    Returns:
        DataFrame: 異常値のデータ
    """
    def parse_rate(rate_str):
        """
        値上げ率の文字列から数値を抽出
        例: "5%" -> 5, "-3%" -> -3, "データなし" -> None
        """
        if pd.isna(rate_str) or rate_str == "データなし":
            return None
        try:
            # %記号を除去して数値に変換
            return float(str(rate_str).replace('%', ''))
        except (ValueError, AttributeError):
            return None

    # 値上げ率を数値に変換
    comparison_df['_rate_numeric'] = comparison_df['値上げ率'].apply(parse_rate)

    # ±threshold%以上のデータを抽出
    abnormal_df = comparison_df[
        (comparison_df['_rate_numeric'].notna()) &
        ((comparison_df['_rate_numeric'] >= threshold) |
         (comparison_df['_rate_numeric'] <= -threshold))
    ].copy()

    # 値上げ率の数値で降順ソート
    if not abnormal_df.empty:
        abnormal_df = abnormal_df.sort_values(by='_rate_numeric', ascending=False)

    # 一時カラムを削除
    if '_rate_numeric' in abnormal_df.columns:
        abnormal_df = abnormal_df.drop(columns=['_rate_numeric'])

    return abnormal_df


def process_excel_files(previous_file, current_file, threshold=20):
    """
    Excelファイルを処理して4シート出力を生成

    Args:
        previous_file: 前回データのファイル
        current_file: 今回データのファイル
        threshold: 異常値の基準（デフォルト: 20%）

    Returns:
        tuple: (出力ExcelのBytesIO, 処理統計dict)

    Raises:
        ValueError: 処理エラー
    """
    try:
        # 1. ファイル読み込み
        previous_df, previous_comment = read_excel_with_comment(previous_file)
        current_df, current_comment = read_excel_with_comment(current_file)

        # 2. 今回データの計算（J〜M列）
        current_df = calculate_j_k_l_m_columns(current_df)

        # 3. 比較データの作成
        comparison_df = create_comparison_dataframe(previous_df, current_df)

        # 4. 比較データの計算（H, I列）
        comparison_df = calculate_comparison_columns(comparison_df)

        # 5. 異常値シートの作成（ユーザー指定の閾値を使用）
        abnormal_df = extract_abnormal_values(comparison_df, threshold=threshold)

        # 6. 前回データの備考行を作成（各列に個別のテキストを設定）
        previous_comment_dict = {
            'A1': previous_comment,  # 元の備考行
            'F1': '新築換算坪単価',
            'G1': '新築坪単価',
            'H1': '成約中古坪単価',
            'I1': 'サンプル数',
            'J1': '→坪単価*0.3025*70'
        }

        # 6. 今回データの備考行を作成（各列に個別のテキストを設定）
        current_comment_dict = {
            'A1': current_comment,  # 元の備考行
            'F1': '新築換算坪単価',
            'G1': '新築坪単価',
            'H1': '成約中古坪単価',
            'I1': 'サンプル数',
            'J1': '→坪単価*0.3025*70'
        }

        # 7. 比較データの備考行を作成
        today = datetime.now().strftime('%Y年%m月%d日')
        comparison_comment = f"前回データと今回データの比較（{today}処理）"

        # 8. 異常値シートの備考行を作成
        abnormal_comment = f"値上げ率±{threshold}%以上の異常値データ（{today}処理）"

        # 9. Excelファイル生成（4シート）
        output = write_excel_with_sheets(
            previous_df, previous_comment_dict,
            current_df, current_comment_dict,
            comparison_df, comparison_comment,
            abnormal_df, abnormal_comment
        )

        # 10. 統計情報
        stats = {
            'previous_rows': len(previous_df),
            'current_rows': len(current_df),
            'comparison_rows': len(comparison_df),
            'abnormal_rows': len(abnormal_df),
            'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return output, stats

    except Exception as e:
        raise ValueError(f"データ処理中にエラーが発生しました: {str(e)}")
