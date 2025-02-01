import streamlit as st

st.title("80分の1スケール 計算ツール")

# CSSでスタイルを設定
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 24px;
        font-weight: bold;
        margin: 0px;
        padding: 0px;
    }
    
    [data-testid="stHorizontalBlock"] {
        min-width: 200px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'input_value' not in st.session_state:
    st.session_state.input_value = '0'

def create_tenkey(key_prefix):
    buttons = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['0', 'C', '⌫']
    ]
    
    # テンキーの表示
    container = st.container()
    with container:
        for row in buttons:
            cols = st.columns(3)
            for i, button in enumerate(row):
                with cols[i]:
                    if st.button(button, key=f'{key_prefix}_{button}', use_container_width=True):
                        if button == 'C':
                            st.session_state.input_value = '0'
                        elif button == '⌫':
                            st.session_state.input_value = st.session_state.input_value[:-1] or '0'
                        else:
                            if st.session_state.input_value == '0':
                                st.session_state.input_value = button
                            else:
                                st.session_state.input_value += button

# タブの作成
tab1, tab2 = st.tabs(["図面から", "実寸から"])

with tab1:
    st.markdown("図面上の寸法（mm）")
    
    # 数値入力フィールド
    drawing_input = st.text_input("図面寸法", value=st.session_state.input_value, key="drawing_input")
    
    # テンキー表示
    create_tenkey("drawing")
    
    if st.button("計算する", key="calc_drawing"):
        try:
            drawing_size = float(st.session_state.input_value)
            real_size = drawing_size * 80
            
            st.markdown(f"""
            計算結果:
            
            図面上の寸法:
            - {drawing_size:.1f} mm
            - {drawing_size/1000:.3f} m
            
            実際の寸法:
            - {real_size:.1f} mm
            - {real_size/1000:.3f} m
            
            縮尺: 1:80
            """)
        except ValueError:
            st.error("有効な数値を入力してください")

with tab2:
    st.markdown("実際の寸法（mm）")
    
    # 数値入力フィールド
    real_input = st.text_input("実寸法", value=st.session_state.input_value, key="real_input")
    
    # テンキー表示
    create_tenkey("real")
    
    if st.button("計算する", key="calc_real"):
        try:
            real_size = float(st.session_state.input_value)
            drawing_size = real_size / 80
            
            st.markdown(f"""
            計算結果:
            
            実際の寸法:
            - {real_size:.1f} mm
            - {real_size/1000:.3f} m
            
            図面上の寸法:
            - {drawing_size:.1f} mm
            - {drawing_size/1000:.3f} m
            
            縮尺: 1:80
            """)
        except ValueError:
            st.error("有効な数値を入力してください")

st.markdown("""
使い方:
1. 計算したい寸法のタブを選択
2. テンキーで数値を入力(または直接入力)
3. "計算する"ボタンをクリック
* テンキーの'C'は入力クリア
""")
