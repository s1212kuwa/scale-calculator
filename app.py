import streamlit as st

# カスタムCSSを更新
st.markdown("""

def calculate_real_size(drawing_size):
    return drawing_size * 80

def calculate_drawing_size(real_size):
    return real_size / 80

def add_numpad(key_prefix, current_value):
    # 現在の値を文字列として管理
    if 'input_value' not in st.session_state:
        st.session_state.input_value = str(int(current_value))
    
    # テンキーのボタン配置
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
    
    try:
        return int(st.session_state.input_value)
    except ValueError:
        return 0

st.title('80分の1スケール変換計算機')

# タブを作成
tab1, tab2 = st.tabs(['図面から', '実寸から'])

# 図面から実寸への変換
with tab1:
    st.header('図面から')
    
    # テンキー
    st.write('テンキー：')
    current_value1 = add_numpad('drawing', 0.0)
    
    # 入力エリア
    st.markdown('##### 入力値')
    input_col1 = st.container()
    with input_col1:
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        drawing_size = st.number_input(
            '図面上で測定した長さ（mm）：',
            min_value=0,
            step=1,
            format='%d',
            value=int(current_value1)
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 計算ボタン
    calc_col1 = st.container()
    with calc_col1:
        st.markdown('<div class="calc-button">', unsafe_allow_html=True)
        if st.button('計算する', key='calc1'):
            real_size = calculate_real_size(drawing_size)
            st.success(f"""
            実際のサイズ：
            - {real_size:.1f} mm
            - {real_size/1000:.3f} m
            """)
        st.markdown('</div>', unsafe_allow_html=True)

# 実寸から図面サイズへの変換
with tab2:
    st.header('実寸から')
    
    # テンキー
    st.write('テンキー：')
    current_value2 = add_numpad('real', 0.0)
    
    # 入力エリア
    st.markdown('##### 入力値')
    input_col2 = st.container()
    with input_col2:
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        real_size = st.number_input(
            '実際の長さ（mm）：',
            min_value=0,
            step=1,
            format='%d',
            value=int(current_value2)
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 計算ボタン
    calc_col2 = st.container()
    with calc_col2:
        st.markdown('<div class="calc-button">', unsafe_allow_html=True)
        if st.button('計算する', key='calc2'):
            drawing_size = calculate_drawing_size(real_size)
            st.success(f"""
            図面上のサイズ：
            - {drawing_size:.1f} mm
            """)
        st.markdown('</div>', unsafe_allow_html=True)

# サイドバーに説明を追加
with st.sidebar:
    st.header('使い方')
    st.write("""
    1. 変換したい方のタブを選択
    2. テンキーで数値を入力（または直接入力）
    3. 「計算する」ボタンをクリック
    
    ※ テンキーの'C'は入力クリア
    """)


