from models.video import ScoreBatVideoAPI
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Football Videos",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .video-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #E91E63;
    }
    .match-title {
        color: #E91E63;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .competition-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .date-info {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🎥 Football Match Highlights")
st.markdown("### Watch the latest goals and match highlights from top competitions")

# Hero image
image_url = 'https://cdn.pixabay.com/photo/2013/12/12/21/48/football-stadium-227561_1280.jpg'
st.image(image_url, width="stretch")

# Sidebar
st.sidebar.title('🎬 Video Section')

with st.sidebar.expander('ℹ️ About This Page'):
    st.write('Click the button below to fetch the latest football match highlights and videos!')
    st.write('**Features:**')
    st.write('• 🎯 Latest match highlights')
    st.write('• ⚽ Goals and key moments')
    st.write('• 🏆 Coverage from major competitions')

if st.sidebar.button('🏠 Back to Main Page', width="stretch"):
    st.switch_page("app.py")

st.markdown("---")

# Main content
if st.button("🎬 Fetch Latest Highlights", width="stretch", type="primary"):
    with st.spinner('🔄 Loading latest match highlights...'):
        try:
            my_video = ScoreBatVideoAPI()
            video_data = my_video.get_recent_video()

            if not video_data:
                st.warning("⚠️ No videos available at the moment. Please try again later.")
            else:
                st.success(f"✅ Found {len(video_data)} match highlights!")
                st.markdown("---")

                # Display videos in a grid
                for idx, video_info in enumerate(video_data):
                    title = video_info.get('title', 'Unknown Match')
                    competition = video_info.get('competition', 'Competition')
                    matchview_url = video_info.get('matchviewUrl', '#')
                    thumbnail = video_info.get('thumbnail', '')
                    date = video_info.get('date', 'Date unknown')
                    videos = video_info.get('videos', [])

                    # Create expandable card for each match
                    with st.expander(f"⚽ {title}", expanded=(idx < 3)):
                        col1, col2 = st.columns([2, 3])

                        with col1:
                            if thumbnail:
                                st.image(thumbnail, width="stretch")
                            st.markdown(f'<span class="competition-badge">{competition}</span>', unsafe_allow_html=True)
                            st.markdown(f'<p class="date-info">📅 {date}</p>', unsafe_allow_html=True)
                            if matchview_url and matchview_url != '#':
                                st.link_button("🔗 Full Match Details", matchview_url, width="stretch")

                        with col2:
                            if videos:
                                # Only show the first available embed per match
                                target_video = next((v for v in videos if v.get('embed')), videos[0])
                                video_title = target_video.get('title', 'Highlight')
                                embed_code = target_video.get('embed', '')

                                st.markdown(f"**{video_title}**")
                                if embed_code:
                                    st.markdown(embed_code, unsafe_allow_html=True)
                                else:
                                    st.info("No video embed available for this match")
                            else:
                                st.info("No video embed available for this match")

                        st.markdown("---")

        except Exception as e:
            st.error(f"❌ Error loading videos: {str(e)}")
            st.info("💡 Please check your API configuration and try again.")
else:
    st.info("👆 Click the button above to load the latest football highlights!")
