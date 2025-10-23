"""
ファイルバリデーションモジュール

このモジュールは、アップロードされたExcelファイルまたはCSVファイルの妥当性を検証します。
- ファイル形式のチェック（.xlsx, .csv）
- ファイル読み込みテスト
- 必須カラムの存在確認
- データ行の存在確認
"""

import pandas as pd
from utils.excel_handler import detect_csv_encoding


def validate_file(file, file_name):
    """
    ファイルの妥当性を検証

    Args:
        file: Streamlitのアップロードファイル
        file_name: ファイル名（エラーメッセージ用）

    Raises:
        ValueError: バリデーションエラー
    """
    # 1. 拡張子チェック
    is_xlsx = file.name.endswith('.xlsx')
    is_csv = file.name.endswith('.csv')

    if not (is_xlsx or is_csv):
        raise ValueError(f"{file_name}: .xlsxまたは.csv形式のファイルをアップロードしてください")

    try:
        # 2. ファイル読み込みテスト（まず2行目をヘッダーとして試す）
        if is_csv:
            # エンコーディングを自動検出
            encoding = detect_csv_encoding(file)
            if hasattr(file, 'seek'):
                file.seek(0)
            df = pd.read_csv(file, header=1, encoding=encoding)
        else:
            df = pd.read_excel(file, header=1)

        # 3. ヘッダー行の存在チェック
        if df.empty:
            raise ValueError(f"{file_name}: データ行が見つかりませんでした")

        # 4. 必須カラムチェック（大文字小文字を無視）
        required_columns = ['stationid', 'railroad']

        # カラム名を小文字に変換してチェック
        df_columns_lower = [col.lower() if isinstance(col, str) else col for col in df.columns]
        has_required_columns = all(
            req_col.lower() in df_columns_lower for req_col in required_columns
        )

        # 必須カラムが見つからない場合、1行目をヘッダーとして再試行
        if not has_required_columns:
            # ファイルポインタをリセット
            if hasattr(file, 'seek'):
                file.seek(0)

            # 1行目をヘッダーとして読み込み
            if is_csv:
                df_alt = pd.read_csv(file, header=0, encoding=encoding)
            else:
                df_alt = pd.read_excel(file, header=0)

            if not df_alt.empty:
                df_alt_columns_lower = [col.lower() if isinstance(col, str) else col for col in df_alt.columns]
                has_required_columns_alt = all(
                    req_col.lower() in df_alt_columns_lower for req_col in required_columns
                )

                # 1行目で見つかった場合は、それを採用
                if has_required_columns_alt:
                    df = df_alt
                    has_required_columns = True

        # まだ必須カラムが見つからない場合はエラー
        if not has_required_columns:
            missing_columns = [col for col in required_columns
                             if col.lower() not in df_columns_lower]
            raise ValueError(
                f"{file_name}: 必須カラムが見つかりません - {', '.join(missing_columns)}"
            )

        # 5. データ行の存在チェック
        if len(df) < 1:
            raise ValueError(f"{file_name}: データ行が見つかりませんでした")

        # ファイルポインタをリセット（ファイルオブジェクトの場合のみ）
        if hasattr(file, 'seek'):
            file.seek(0)

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        else:
            raise ValueError(f"{file_name}: ファイル読み込みエラー - {str(e)}")
