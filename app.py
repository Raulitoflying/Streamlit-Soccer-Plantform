import streamlit as st

# Page configuration
st.set_page_config(
    page_title="World Football Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .stat-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    /* Light theme - 浅色主题用浅色卡片 */
    [data-testid="stAppViewContainer"][data-theme="light"] .stat-box,
    .stat-box {
        background: #f8f9fa !important;
        border-left: 4px solid #1E88E5;
        color: #333 !important;
    }
    [data-testid="stAppViewContainer"][data-theme="light"] .stat-box h4,
    .stat-box h4 {
        color: #1E88E5 !important;
    }
    [data-testid="stAppViewContainer"][data-theme="light"] .stat-box p,
    .stat-box p {
        color: #666 !important;
    }

    /* Dark theme - 深色主题用深色卡片 */
    [data-testid="stAppViewContainer"][data-theme="dark"] .stat-box {
        background: #1a1a1a !important;
        border-left: 4px solid #64b5f6;
        color: #e0e0e0 !important;
    }
    [data-testid="stAppViewContainer"][data-theme="dark"] .stat-box h4 {
        color: #64b5f6 !important;
    }
    [data-testid="stAppViewContainer"][data-theme="dark"] .stat-box p {
        color: #b0b0b0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">⚽ World Football Platform</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Gateway to Football Data & Highlights</p>', unsafe_allow_html=True)

# Hero image
image_url = 'https://cdn.pixabay.com/photo/2016/09/18/20/47/football-1678992_1280.jpg'
st.image(image_url, width="stretch")

# Feature cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h2>📊 Statistical Data</h2>
            <p>Explore comprehensive football statistics, team info, standings, and top scorers from leagues worldwide.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Explore Stats", width="stretch", type="primary"):
        st.switch_page("pages/search.py")

with col2:
    st.markdown("""
        <div class="feature-card">
            <h2>🎥 Video Highlights</h2>
            <p>Watch the latest match highlights and goals from top football competitions around the world.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Watch Videos", width="stretch", type="primary"):
        st.switch_page("pages/watch.py")

# About section
st.markdown("---")
st.markdown("### 📖 About This Platform")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### 🌍 Global Coverage")
    st.write("Data from major football leagues and competitions worldwide")

with col_b:
    st.markdown("#### 📈 Real-time Data")
    st.write("Up-to-date statistics powered by Football Data API")

with col_c:
    st.markdown("#### 🎬 Video Highlights")
    st.write("Latest match videos from ScoreBat API")

# Sidebar
st.sidebar.title('🧭 Navigation')

apilink = '[Football Data](https://www.football-data.org/)'
with st.sidebar.expander('ℹ️ About the Project'):
    st.write('This platform was built out of love for football and curiosity for stats.')
    st.write(f'Data powered by {apilink}')
    st.write("**Features:**")
    st.write("• 📊 View global football competitions and statistics")
    st.write("• 👥 Team information and standings")
    st.write("• ⚽ Top scorers and league tables")
    st.write("• 🎥 Watch exciting match highlights")

with st.sidebar.expander('👤 Credits'):
    st.write('**Created by:** Yixiang Zhou')
    st.markdown('[LinkedIn Profile](https://www.linkedin.com/in/yixiang-zhou-1b5040250/)')
    st.markdown('[Football Data API](https://www.football-data.org)')

st.sidebar.markdown("---")
st.sidebar.info("💡 Select a feature above to get started!")
