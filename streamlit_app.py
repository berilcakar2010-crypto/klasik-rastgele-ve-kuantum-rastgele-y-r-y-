import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Klasik ve kuantum rastgele yürüyüş", layout="wide")

# Sadece Terminal Estetiği (Matrix Green & Deep Black)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    div[data-testid="stMarkdownContainer"] { color: #00FF41; font-family: 'Courier New', monospace; }
    .stSlider label { color: #00FF41 !important; }
    .stHeader { color: #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# Yan Panel Kontrolleri
st.sidebar.markdown("KONTROL PANELİ")
steps = st.sidebar.slider("ADIM SAYISI", 10, 150, 60)
opacity = st.sidebar.slider("İZ YOĞUNLUĞU", 0.1, 1.0, 0.6)

def run_classical(n):
    probs = np.zeros(2 * n + 1)
    probs[n] = 1.0
    for _ in range(n):
        new_p = np.zeros(2 * n + 1)
        new_p[1:-1] = 0.5 * probs[:-2] + 0.5 * probs[2:]
        probs = new_p
    return probs

def run_quantum(n):
    size = 2 * n + 1
    state = np.zeros((size, 2), dtype=complex)
    state[n, 0] = 1/np.sqrt(2)
    state[n, 1] = 1j/np.sqrt(2)
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    for _ in range(n):
        state = np.dot(state, H.T)
        new_s = np.zeros_like(state)
        new_s[:-1, 0] = state[1:, 0]
        new_s[1:, 1] = state[:-1, 1]
        state = new_s
    return np.sum(np.abs(state)**2, axis=1)

# Veriyi işle
c_data = run_classical(steps)
q_data = run_quantum(steps)
x = np.arange(-steps, steps + 1)

# Görselleştirme (Radar Ekranı)
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('black')
ax.set_facecolor('#050505')

# Izgara çizgileri (Radar efekti)
ax.grid(color='#00FF41', linestyle='--', linewidth=0.3, alpha=0.2)

# Klasik Yürüyüş (Kırmızı Sis)
ax.fill_between(x, c_data, color='#FF0000', alpha=opacity * 0.4, label='[KLASİK RASTGELE YÜRÜYÜŞ]')
ax.plot(x, c_data, color='#FF0000', linewidth=1, alpha=opacity)

# Kuantum Yürüyüş (Neon Yeşil Dalga)
ax.fill_between(x, q_data, color='#00FF41', alpha=opacity * 0.3, label='[KUANTUM RASTGELE YÜRÜYÜŞ]')
ax.plot(x, q_data, color='#00FF41', linewidth=2, alpha=opacity)

ax.tick_params(colors='#00FF41', labelsize=8)
ax.legend(facecolor='black', labelcolor='#00FF41', edgecolor='#00FF41')

st.pyplot(fig)

# Basit ve Net Açıklamalar
col1, col2 = st.columns(2)

with col1:
    st.markdown(" Klasik Yürüyüş (Zar Atışı)")
    st.write("""
    Parçacık her seferinde eş olasılıkla sağa veya sola gider. 
    Yazı tura atar gibi ilerlediği için sürekli merkeze geri döner. 
    Çok yavaştır; yerinde sayar.
    """)

with col2:
    st.markdown(" Kuantum Yürüyüş (Süperpozisyon)")
    st.write("""
     Parçacık süperpozisyona geçer, aynı anda hem sağa hem sola gider. 
    Yollar birbiriyle girişim deseni oluşturur.
    Merkezden uzaklaşmaya meyillidir. Bir kuantum bilgisayarın saniyeler içinde 
    milyarlarca veriyi taramasını sağlayan yöntem budur.
    """)
