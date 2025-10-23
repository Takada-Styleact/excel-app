"""
エクセルデータ加工システム（Streamlit版）

このアプリケーションは、2つのExcelファイルを比較・加工し、
3シートを含む1つのExcelファイルを出力します。
"""

import streamlit as st
from datetime import datetime
from modules.data_processor import process_excel_files
from utils.file_validator import validate_file

# ページ設定
st.set_page_config(
    page_title="エクセルデータ加工システム",
    page_icon="📊",
    layout="centered"
)

# セッション状態初期化
if 'processed' not in st.session_state:
    st.session_state['processed'] = False
if 'output' not in st.session_state:
    st.session_state['output'] = None
if 'stats' not in st.session_state:
    st.session_state['stats'] = None

# タイトル
st.title("📊 エクセルデータ加工システム")
st.markdown("---")

# セクション1: ファイルアップロード
st.header("📁 ファイルアップロード")

col1, col2 = st.columns(2)

with col1:
    st.subheader("前回データ")
    previous_file = st.file_uploader(
        "前回データをアップロード",
        type=['xlsx', 'csv'],
        key="previous"
    )
    if previous_file:
        st.success(f"✅ {previous_file.name}")

with col2:
    st.subheader("今回データ")
    current_file = st.file_uploader(
        "今回データをアップロード",
        type=['xlsx', 'csv'],
        key="current"
    )
    if current_file:
        st.success(f"✅ {current_file.name}")

st.markdown("---")

# セクション2: 異常値シート設定
st.header("⚙️ 異常値シート設定")
threshold = st.number_input(
    "異常値の基準（±%）",
    min_value=1,
    max_value=99,
    value=20,
    step=1,
    help="値上げ率がこの値以上（またはマイナスこの値以下）の場合、異常値シートに表示されます"
)
st.info(f"💡 現在の設定: ±{threshold}%以上のデータを異常値として抽出します")

st.markdown("---")

# セクション3: 処理実行
st.header("⚡ データ処理")

# ボタンの有効化条件
if previous_file and current_file:
    if st.button("🚀 データ処理を実行", type="primary", use_container_width=True):
        try:
            with st.spinner("処理中です...しばらくお待ちください"):
                # バリデーション
                validate_file(previous_file, "前回データ")
                validate_file(current_file, "今回データ")

                # メイン処理（基準値を渡す）
                output_buffer, stats = process_excel_files(
                    previous_file,
                    current_file,
                    threshold=threshold
                )

                # セッション状態に保存
                st.session_state['output'] = output_buffer
                st.session_state['stats'] = stats
                st.session_state['processed'] = True

            # 成功メッセージ
            st.success("✅ 処理が完了しました！")
            st.info(f"""
            📊 **処理結果**
            - 前回データ: {stats['previous_rows']}行
            - 今回データ: {stats['current_rows']}行
            - 比較データ: {stats['comparison_rows']}行
            """)

        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
            st.session_state['processed'] = False
else:
    st.warning("⚠️ 両方のファイルをアップロードしてください")

st.markdown("---")

# セクション3: ダウンロード
st.header("📥 結果ダウンロード")

if st.session_state.get('processed', False):
    output_buffer = st.session_state['output']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"output_{timestamp}.xlsx"

    st.download_button(
        label="📥 結果をダウンロード",
        data=output_buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True
    )
else:
    st.info("💡 処理を実行すると、ダウンロードボタンが表示されます")
