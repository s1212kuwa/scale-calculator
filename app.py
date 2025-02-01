import streamlit as st

# カスタムCSSを更新
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 24px;
        font-weight: bold;
        margin: 2px;
        padding: 0px;
    }
    
    /* 計算ボタンのスタイル */
    .calc-button .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.2rem;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* テンキーのグリッドレイアウト */
    .numpad-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 5px;
        max-width: 300px;
        margin: 0 auto;
        padding: 10px;
    }

    .numpad-button {
        width: 100%;
    }

    /* モバイル対応のための追加スタイル */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 20px;
            height: 45px;
            min-width: unset !important;
        }
        
        .input-area input {
            font-size: 1.2rem;
            height: 45px;
        }
    }
</style>
""", unsafe_allow_html=True)

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
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['0', 'C', '⌫']
    ]
    
    # テンキーの表示
    container = st.container()
    with container:
        html_buttons = ""
        for row in buttons:
            for button in row:
                html_buttons += f'<div class="numpad-button element-container css-1hynsf2 e1f1d6gn2">'
                html_buttons += f'<div class="row-widget stButton css-1yqw6j3 e1f1d6gn1">'
                html_buttons += f'<button kind="secondary" class="css-1cpxqw2 edgvbvh9" id="{key_prefix}_{button}">{button}</button>'
                html_buttons += '</div></div>'

        st.markdown(f'<div class="numpad-grid">{html_buttons}</div>', unsafe_allow_html=True)

        # JavaScriptでボタンのクリックイベントを処理
        js = f"""
        <script>
        const buttons = document.querySelectorAll('.numpad-grid button');
        buttons.forEach(button => {{
            button.addEventListener('click', function() {{
                const value = this.textContent;
                // Streamlitのボタンクリックをシミュレート
                document.querySelector(`button[key="{key_prefix}_${{value}}"]`).click();
            }});
        }});
        </script>
        """
        st.markdown(js, unsafe_allow_html=True)

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
