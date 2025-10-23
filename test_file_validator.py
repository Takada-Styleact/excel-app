"""
file_validator.py の動作確認テスト
"""

import sys
sys.path.append('.')

from utils.file_validator import validate_file
import pandas as pd
from io import BytesIO

def test_valid_file():
    """
    正常なファイルのバリデーション
    """
    print("=" * 50)
    print("[テスト1] 正常なファイルのバリデーション")
    print("=" * 50)

    file_path = 'tests/sample_data/sample_前回データ.xlsx'

    # ファイルオブジェクトを直接使用
    with open(file_path, 'rb') as f:
        try:
            validate_file(f, "前回データ")
            print("[OK] バリデーション成功")
        except ValueError as e:
            print(f"[NG] バリデーションエラー: {e}")
            raise

def test_invalid_extension():
    """
    不正な拡張子のテスト
    """
    print("\n" + "=" * 50)
    print("[テスト2] 不正な拡張子")
    print("=" * 50)

    class MockInvalidFile:
        def __init__(self):
            self.name = 'test.xls'  # .xlsは非対応

    file = MockInvalidFile()

    try:
        validate_file(file, "テストデータ")
        print("[NG] エラーが発生すべきでした")
        raise AssertionError("拡張子チェックが機能していません")
    except ValueError as e:
        print(f"[OK] 期待通りエラー: {e}")

def test_missing_columns():
    """
    必須カラムがないファイルのテスト
    """
    print("\n" + "=" * 50)
    print("[テスト3] 必須カラムがないファイル")
    print("=" * 50)

    # stationidカラムがないデータを作成
    df = pd.DataFrame({
        'name': ['東京', '新宿'],
        'railroad': ['JR山手線', 'JR山手線']
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 備考行を追加
        pd.DataFrame([['備考行']]).to_excel(writer, sheet_name='Sheet1', index=False, header=False)
        df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1)

    output.seek(0)

    class MockBytesIOFile:
        def __init__(self, data, filename):
            self.name = filename
            self._data = data

        def read(self):
            return self._data.read()

        def seek(self, position):
            self._data.seek(position)

    file = MockBytesIOFile(output, 'test.xlsx')

    try:
        validate_file(file, "テストデータ")
        print("[NG] エラーが発生すべきでした")
        raise AssertionError("必須カラムチェックが機能していません")
    except ValueError as e:
        print(f"[OK] 期待通りエラー: {e}")
        assert 'stationid' in str(e), "エラーメッセージにstationidが含まれていません"

def test_empty_file():
    """
    データ行がないファイルのテスト
    """
    print("\n" + "=" * 50)
    print("[テスト4] データ行がないファイル")
    print("=" * 50)

    # ヘッダーのみでデータがないファイルを作成
    df = pd.DataFrame(columns=['stationid', 'name', 'railroad'])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 備考行を追加
        pd.DataFrame([['備考行']]).to_excel(writer, sheet_name='Sheet1', index=False, header=False)
        df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1)

    output.seek(0)

    class MockBytesIOFile:
        def __init__(self, data, filename):
            self.name = filename
            self._data = data

        def read(self):
            return self._data.read()

        def seek(self, position):
            self._data.seek(position)

    file = MockBytesIOFile(output, 'test.xlsx')

    try:
        validate_file(file, "テストデータ")
        print("[NG] エラーが発生すべきでした")
        raise AssertionError("データ行チェックが機能していません")
    except ValueError as e:
        print(f"[OK] 期待通りエラー: {e}")
        assert 'データ行が見つかりませんでした' in str(e), "エラーメッセージが正しくありません"

if __name__ == '__main__':
    try:
        test_valid_file()
        test_invalid_extension()
        test_missing_columns()
        test_empty_file()
        print("\n" + "=" * 50)
        print("[OK] すべてのテストが成功しました！")
        print("=" * 50)
    except Exception as e:
        print(f"\n[NG] エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
