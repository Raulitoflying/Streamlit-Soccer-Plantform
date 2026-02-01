import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from models.data import FootballDataAPI
from models.produce import DataExporter
import matplotlib.pyplot as plt
import datetime as dt

# Page configuration
st.set_page_config(
    page_title="Football Statistics",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for modern design with dark mode support
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #1E88E5;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 3px solid #1E88E5;
        padding-bottom: 0.5rem;
    }
    .team-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #4CAF50;
    }
    /* Dark mode support for team names in standings */
    @media (prefers-color-scheme: dark) {
        .team-name-light {
            color: #e0e0e0 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)


# Country code helper for flags
def get_country_code(nationality):
    """Map nationality names to ISO 3166-1 alpha-2 country codes"""
    country_codes = {
        'England': 'GB-ENG', 'Spain': 'ES', 'France': 'FR', 'Germany': 'DE',
        'Italy': 'IT', 'Portugal': 'PT', 'Brazil': 'BR', 'Argentina': 'AR',
        'Netherlands': 'NL', 'Belgium': 'BE', 'Uruguay': 'UY', 'Colombia': 'CO',
        'Croatia': 'HR', 'Poland': 'PL', 'Egypt': 'EG', 'Senegal': 'SN',
        'Morocco': 'MA', 'Serbia': 'RS', 'Denmark': 'DK', 'Switzerland': 'CH',
        'Austria': 'AT', 'Sweden': 'SE', 'Norway': 'NO', 'Ukraine': 'UA',
        'Czech Republic': 'CZ', 'Turkey': 'TR', 'Greece': 'GR', 'Chile': 'CL',
        'Mexico': 'MX', 'Japan': 'JP', 'South Korea': 'KR', 'Nigeria': 'NG',
        'Ivory Coast': 'CI', 'Ghana': 'GH', 'Cameroon': 'CM', 'Algeria': 'DZ',
        'USA': 'US', 'Canada': 'CA', 'Australia': 'AU', 'Scotland': 'GB-SCT',
        'Wales': 'GB-WLS', 'Ireland': 'IE', 'Northern Ireland': 'GB-NIR',
        'Ecuador': 'EC', 'Peru': 'PE', 'Paraguay': 'PY', 'Venezuela': 'VE',
        'Iceland': 'IS', 'Finland': 'FI', 'Romania': 'RO', 'Hungary': 'HU',
        'Slovakia': 'SK', 'Slovenia': 'SI', 'Bosnia-Herzegovina': 'BA',
        'Bosnia and Herzegovina': 'BA', 'Albania': 'AL', 'North Macedonia': 'MK', 'Montenegro': 'ME',
        'Kosovo': 'XK', 'Russia': 'RU', 'Tunisia': 'TN', 'Iran': 'IR',
        'Georgia': 'GE', 'Guinea': 'GN', 'South Africa': 'ZA', 'Costa Rica': 'CR', 'Jamaica': 'JM',
        'Mali': 'ML', 'Burkina Faso': 'BF', 'Saudi Arabia': 'SA', 'Qatar': 'QA',
        'UAE': 'AE', 'United Arab Emirates': 'AE', 'Bolivia': 'BO', 'Honduras': 'HN', 'Panama': 'PA',
        'El Salvador': 'SV', 'Guatemala': 'GT', 'Trinidad and Tobago': 'TT',
        'Curacao': 'CW', 'Curaçao': 'CW', 'New Zealand': 'NZ', 'China PR': 'CN', 'India': 'IN',
        'Thailand': 'TH', 'Vietnam': 'VN', 'Indonesia': 'ID', 'Philippines': 'PH',
        'Malaysia': 'MY'
    }
    if not nationality:
        return ''
    return country_codes.get(nationality, '')


def leagues_display(choice, data):
    """Display league names based on the specified area choice."""
    leagues = []
    for comp in data["competitions"]:
        if comp['area']['name'] == choice:
            leagues.append(comp['name'])

    if leagues:
        for league in leagues:
            st.markdown(f"⚽ **{league}**")
    else:
        st.info("No leagues found for this region.")


# Header
st.markdown('<h1 style="color: #1E88E5;">📊 World Football Statistics Platform</h1>', unsafe_allow_html=True)
st.markdown("### Explore comprehensive football data from leagues worldwide")

# Sidebar
st.sidebar.title('📋 Navigation & Filters')

with st.sidebar.expander('ℹ️ About This Page'):
    st.write('**Features:**')
    st.write('• 🌍 View competitions by continent/country')
    st.write('• 👥 Team information and details')
    st.write('• 🎯 Top 10 scorers rankings')
    st.write('• 📈 League standings and tables')
    st.write('• 📁 Export data to CSV/Excel')

if st.sidebar.button('🏠 Back to Main Page', width="stretch"):
    st.switch_page("app.py")

# Load data with spinner
with st.spinner('🔄 Loading football data...'):
    data = FootballDataAPI()
    data1 = data.fetch_data_general()

# Process data
area_dict = {}
comp_dict = {}
for comp in data1['competitions']:
    area_name = comp['area']['name']
    comp_name = comp['name']
    area_dict[area_name] = area_dict.get(area_name, 0) + 1
    comp_dict[comp_name] = comp_dict.get(comp_name, 0) + 1

area_df = pd.DataFrame(area_dict.items(), columns=['Country Name', 'Count'])
comp_df = pd.DataFrame(comp_dict.items(), columns=['League Name', 'Count'])

st.markdown("---")

# Word Cloud Section
st.markdown('<p class="section-header">☁️ League Word Cloud</p>', unsafe_allow_html=True)

if st.button("🎨 Generate Word Cloud", width="stretch"):
    with st.spinner('Creating word cloud...'):
        words = ' '.join(comp_df['League Name'])
        wordcloud = WordCloud(
            stopwords=STOPWORDS,
            background_color='white',
            width=1600,
            height=700,
            colormap='viridis'
        ).generate(words)

        fig, ax = plt.subplots(figsize=(16, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        plt.close()

st.markdown("---")

# General Stats Section
st.sidebar.markdown("---")
st.sidebar.header('📊 General Statistics')

show_comp_stats = st.sidebar.checkbox('🌍 Country Distribution', key='country_dist')

if show_comp_stats:
    st.markdown('<p class="section-header">🌍 Competitions Per Country</p>', unsafe_allow_html=True)

    chosen_nations = st.multiselect(
        'Select countries to compare:',
        area_df['Country Name'].tolist(),
        key='nation_select'
    )

    if len(chosen_nations) == 0:
        st.info("👆 Please select at least one country to view statistics")
    else:
        sub_area_df = area_df[area_df['Country Name'].isin(chosen_nations)].reset_index(drop=True)
        sub_area_df.index = range(1, len(sub_area_df) + 1)

        col1, col2 = st.columns([2, 3])

        with col1:
            st.dataframe(sub_area_df, width="stretch")

        with col2:
            if sub_area_df.shape[0] > 0:
                fig = px.bar(
                    sub_area_df,
                    x='Country Name',
                    y='Count',
                    title='Competition Count by Country',
                    color='Count',
                    color_continuous_scale='blues',
                    labels={'Count': 'Number of Competitions'}
                )
                fig.update_layout(
                    height=400,
                    xaxis_tickangle=-45 if len(sub_area_df) > 5 else 0
                )
                st.plotly_chart(fig, width="stretch")

st.markdown("---")

# Leagues by Continent
show_leagues_continent = st.sidebar.checkbox('🌏 Leagues by Continent')
continents = ['Europe', 'Asia', 'Africa', 'North America', 'South America', 'Australia']

if show_leagues_continent:
    st.markdown('<p class="section-header">🌏 Football Leagues by Continent</p>', unsafe_allow_html=True)
    choice = st.selectbox('Select Continent:', continents, key='continent_select')
    st.markdown(f"### {choice}'s Football Leagues")
    leagues_display(choice, data1)

st.markdown("---")

# Leagues by Country
show_leagues_country = st.sidebar.checkbox('🏳️ Leagues by Country')

if show_leagues_country:
    st.markdown('<p class="section-header">🏳️ Football Leagues by Country</p>', unsafe_allow_html=True)
    helper = list(area_df[~area_df['Country Name'].isin(continents)]['Country Name'])
    choice = st.selectbox('Select Country:', helper, key='country_select')
    st.markdown(f"### {choice}'s Football Leagues")
    leagues_display(choice, data1)

st.markdown("---")

# Competition Details Section
st.sidebar.markdown("---")
st.sidebar.header('🏆 Competition Details')

with st.sidebar.expander('ℹ️ About Competition Stats'):
    st.write('View detailed information for major leagues including:')
    st.write('• Team information')
    st.write('• Top scorers')
    st.write('• League standings')

# Build competition dictionary
comp_dict = {}
free_tier_list = [
    'Serie A',                  # Italy
    'UEFA Champions League',    # UEFA
    'European Championship',    # UEFA
    'Ligue 1',                  # France
    'Bundesliga',              # Germany
    'Eredivisie',              # Netherlands
    'Primeira Liga',           # Portugal
    'Primera Division',        # Spain
    'FIFA World Cup',          # FIFA
    'Championship',            # England 2nd tier
    'Premier League',          # England
    'Copa Libertadores',       # South America
    'Campeonato Brasileiro Série A'  # Brazil
]

for comp in data1['competitions']:
    if comp['name'] in free_tier_list:
        comp_dict[comp['name']] = comp['id']

# Select competition
default = 'Select a Competition'
options = [default] + list(comp_dict.keys())
svalue = st.sidebar.selectbox('Choose Competition:', options, key='comp_select')

if svalue != default:
    st.markdown(f'<p class="section-header">🏆 {svalue}</p>', unsafe_allow_html=True)
    scorers_data = None

    # Team Info
    if st.sidebar.checkbox('👥 Team Information'):
        with st.spinner('Loading team information...'):
            data2 = data.fetch_data_from_endpoint("teams", comp_dict, svalue)

            if data2 and 'teams' in data2:
                st.markdown(f"**Total Teams:** {data2.get('count', len(data2['teams']))}")

                col1, col2 = st.columns(2)
                for i, team in enumerate(data2['teams']):
                    target_col = col1 if i % 2 == 0 else col2

                    with target_col:
                        with st.expander(f"⚽ {team.get('name', 'Unknown')}"):
                            # Display team logo if available
                            if team.get('crest'):
                                logo_col1, logo_col2 = st.columns([1, 3])
                                with logo_col1:
                                    st.image(team['crest'], width=80)
                                with logo_col2:
                                    st.markdown(f"### {team.get('name', 'Unknown')}")
                                st.markdown("---")

                            st.write(f"**Address:** {team.get('address', 'N/A')}")
                            st.write(f"**Phone:** {team.get('phone', 'N/A')}")
                            if team.get('website'):
                                st.markdown(f"[🌐 Website]({team['website']})")
                            st.write(f"**Founded:** {team.get('founded', 'N/A')}")
                            st.write(f"**Venue:** {team.get('venue', 'N/A')}")

    # Scorers
    top_scorers_enabled = st.sidebar.checkbox('🎯 Top Scorers')

    if top_scorers_enabled:
        if scorers_data is None:
            with st.spinner('Loading top scorers...'):
                scorers_data = data.fetch_data_from_endpoint('scorers', comp_dict, svalue)

        data2 = scorers_data

        if data2 and 'scorers' in data2 and len(data2['scorers']) > 0:
            st.markdown("### 🎯 Top 10 Scorers")

            # Create enhanced scorer list with team crest
            scorer_list = [{
                'Rank': idx + 1,
                'Name': scorer['player']['name'],
                'Position': scorer['player'].get('position', 'N/A'),
                'Nationality': scorer['player'].get('nationality', 'N/A'),
                'Team': scorer['team']['name'],
                'Team_Crest': scorer['team'].get('crest', ''),
                'Goals': scorer.get('goals', scorer.get('numberOfGoals', 0))
            } for idx, scorer in enumerate(data2['scorers'])]

            df = pd.DataFrame(scorer_list)

            # Display scorers with team crests
            st.markdown("#### 🏅 Top Scorers Table")

            # Table header
            header_cols = st.columns([0.5, 3, 0.4, 1.4, 0.5, 2.5, 1])
            headers = ['#', 'Player', '', 'Nationality', '', 'Team', 'Goals']
            for col, header in zip(header_cols, headers):
                with col:
                    st.markdown(f"**{header}**")

            st.markdown("---")

            # Table rows
            for idx, row in df.head(10).iterrows():
                col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 3, 0.4, 1.4, 0.5, 2.5, 1])

                # Rank coloring
                rank = row['Rank']
                if rank == 1:
                    rank_color = "#FFD700"  # Gold
                elif rank == 2:
                    rank_color = "#C0C0C0"  # Silver
                elif rank == 3:
                    rank_color = "#CD7F32"  # Bronze
                else:
                    rank_color = "#6c757d"  # Gray

                with col1:
                    st.markdown(f'<div style="color: {rank_color}; font-size: 1.2em; font-weight: bold; text-align: center;">{row["Rank"]}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{row['Name']}**")
                with col3:
                    # Display country flag using flagcdn.com
                    country_code = get_country_code(row['Nationality'])
                    if country_code:
                        flag_url = f"https://flagcdn.com/w40/{country_code.lower()}.png"
                        st.markdown(f'<img src="{flag_url}" width="30" style="border-radius: 3px;">', unsafe_allow_html=True)
                with col4:
                    st.write(row['Nationality'])
                with col5:
                    if row['Team_Crest']:
                        st.image(row['Team_Crest'], width=30)
                with col6:
                    st.write(row['Team'])
                with col7:
                    st.markdown(f'<div style="background-color: #28a745; color: white; padding: 5px; border-radius: 5px; text-align: center; font-weight: bold;">{row["Goals"]}</div>', unsafe_allow_html=True)

            st.markdown("---")

            # Also show the dataframe for export purposes (hidden in expander)
            with st.expander("📋 View as Table"):
                df_display = df.drop(['Team_Crest', 'Position'], axis=1)
                st.dataframe(df_display, width="stretch")

            # Visualization (only if we have data)
            if not df.empty:
                st.markdown("#### 📊 Goals Distribution")
                fig = px.bar(
                    df.head(10),
                    x='Name',
                    y='Goals',
                    color='Goals',
                    title='Top 10 Goal Scorers - Goals Comparison',
                    color_continuous_scale='reds',
                    labels={'Goals': 'Goals Scored', 'Name': 'Player'},
                    text='Goals'
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(xaxis_tickangle=-45, height=400, showlegend=False)
                st.plotly_chart(fig, width="stretch")

            # Export options
            export_list = [{k: v for k, v in scorer.items() if k != 'Team_Crest'} for scorer in scorer_list]
            exporter = DataExporter(export_list)
            col1, col2 = st.columns(2)
            with col1:
                csv_result = exporter.export_to_csv()
                if csv_result["success"]:
                    st.download_button(
                        "📥 Download CSV",
                        data=csv_result["data"],
                        file_name="scorer_data.csv",
                        mime="text/csv",
                        width="stretch",
                        key='scorers_csv'
                    )
                else:
                    st.warning(csv_result["message"])

            with col2:
                excel_result = exporter.export_to_excel()
                if excel_result["success"]:
                    st.download_button(
                        "📥 Download Excel",
                        data=excel_result["data"],
                        file_name="scorer_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        width="stretch",
                        key='scorers_excel'
                    )
                else:
                    st.warning(excel_result["message"])
        else:
            st.warning("⚠️ Scorer data not available for this competition")

# Standings
if st.sidebar.checkbox('📈 League Standings'):
    if svalue == default:
        st.info("Please select a competition to view standings.")
    else:
        with st.spinner('Loading league standings...'):
            data3 = data.fetch_data_from_new_urlversion('standings', comp_dict, svalue)

            if data3 and 'standings' in data3:
                st.markdown("### 📈 League Standings")

                # Check if grouped (like World Cup)
                if data3['standings'][0].get('group'):
                    for standings_table in data3['standings']:
                        st.markdown(f"#### {standings_table.get('group', 'Group')}")

                        standing_list = [{
                            'Position': entry['position'],
                            'Team': entry['team']['name'],
                            'Crest': entry['team'].get('crest', ''),
                            'Played': entry['playedGames'],
                            'Won': entry['won'],
                            'Draw': entry['draw'],
                            'Lost': entry['lost'],
                            'GF': entry['goalsFor'],
                            'GA': entry['goalsAgainst'],
                            'GD': entry['goalDifference'],
                            'Points': entry['points']
                        } for entry in standings_table['table']]

                        df = pd.DataFrame(standing_list)

                        # Table header
                        header_cols = st.columns([0.5, 0.5, 2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1])
                        headers = ['#', '', 'Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
                        for col, header in zip(header_cols, headers):
                            with col:
                                st.markdown(f"**{header}**")

                        st.markdown("---")

                        # Table rows with color coding
                        for idx, row in df.iterrows():
                            # Color coding for group stage (top 2 advance)
                            position = row['Position']
                            if position <= 2:  # Qualification spots
                                bg_color = "#d4edda"  # Green
                                text_color = "#155724"
                                use_custom_color = True
                            else:
                                bg_color = "#ffffff"
                                text_color = "#333333"
                                use_custom_color = False

                            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns([0.5, 0.5, 2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1])

                            with col1:
                                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 5px; border-radius: 5px; text-align: center;"><b>{row["Position"]}</b></div>', unsafe_allow_html=True)
                            with col2:
                                if row['Crest']:
                                    st.image(row['Crest'], width=30)
                            with col3:
                                if use_custom_color:
                                    st.markdown(f'<div style="color: {text_color};"><b>{row["Team"]}</b></div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f"**{row['Team']}**")
                            with col4:
                                st.write(row['Played'])
                            with col5:
                                st.markdown(f'<div style="color: #28a745;"><b>{row["Won"]}</b></div>', unsafe_allow_html=True)
                            with col6:
                                st.markdown(f'<div style="color: #ffc107;">{row["Draw"]}</div>', unsafe_allow_html=True)
                            with col7:
                                st.markdown(f'<div style="color: #dc3545;">{row["Lost"]}</div>', unsafe_allow_html=True)
                            with col8:
                                st.write(row['GF'])
                            with col9:
                                st.write(row['GA'])
                            with col10:
                                gd = row['GD']
                                gd_color = "#28a745" if gd > 0 else ("#dc3545" if gd < 0 else "#6c757d")
                                st.markdown(f'<div style="color: {gd_color};"><b>{gd:+d}</b></div>', unsafe_allow_html=True)
                            with col11:
                                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 5px; border-radius: 5px; text-align: center;"><b>{row["Points"]}</b></div>', unsafe_allow_html=True)

                        st.markdown("---")
                else:
                    standing_list = [{
                        'Position': entry['position'],
                        'Team': entry['team']['name'],
                        'Crest': entry['team'].get('crest', ''),
                        'Played': entry['playedGames'],
                        'Won': entry['won'],
                        'Draw': entry['draw'],
                        'Lost': entry['lost'],
                        'GF': entry['goalsFor'],
                        'GA': entry['goalsAgainst'],
                        'GD': entry['goalDifference'],
                        'Points': entry['points']
                    } for entry in data3['standings'][0]['table']]

                    df = pd.DataFrame(standing_list)

                    # Display standings with team logos
                    st.markdown("#### 📊 League Table")

                    # Table header
                    header_cols = st.columns([0.5, 0.5, 2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1])
                    headers = ['#', '', 'Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
                    for col, header in zip(header_cols, headers):
                        with col:
                            st.markdown(f"**{header}**")

                    st.markdown("---")

                    # Table rows with color coding
                    for idx, row in df.iterrows():
                        # Color coding based on position
                        position = row['Position']
                        if position <= 4:  # Champions League spots
                            bg_color = "#d4edda"  # Green
                            text_color = "#155724"
                            use_custom_color = True
                        elif position <= 6:  # Europa League spots
                            bg_color = "#d1ecf1"  # Blue
                            text_color = "#0c5460"
                            use_custom_color = True
                        elif position >= len(df) - 2:  # Relegation zone
                            bg_color = "#f8d7da"  # Red
                            text_color = "#721c24"
                            use_custom_color = True
                        else:
                            bg_color = "#ffffff"
                            text_color = "#333333"
                            use_custom_color = False

                        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns([0.5, 0.5, 2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1])

                        with col1:
                            st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 5px; border-radius: 5px; text-align: center;"><b>{row["Position"]}</b></div>', unsafe_allow_html=True)
                        with col2:
                            if row['Crest']:
                                st.image(row['Crest'], width=30)
                        with col3:
                            if use_custom_color:
                                st.markdown(f'<div style="color: {text_color};"><b>{row["Team"]}</b></div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f"**{row['Team']}**")
                        with col4:
                            st.write(row['Played'])
                        with col5:
                            st.markdown(f'<div style="color: #28a745;"><b>{row["Won"]}</b></div>', unsafe_allow_html=True)
                        with col6:
                            st.markdown(f'<div style="color: #ffc107;">{row["Draw"]}</div>', unsafe_allow_html=True)
                        with col7:
                            st.markdown(f'<div style="color: #dc3545;">{row["Lost"]}</div>', unsafe_allow_html=True)
                        with col8:
                            st.write(row['GF'])
                        with col9:
                            st.write(row['GA'])
                        with col10:
                            gd = row['GD']
                            gd_color = "#28a745" if gd > 0 else ("#dc3545" if gd < 0 else "#6c757d")
                            st.markdown(f'<div style="color: {gd_color};"><b>{gd:+d}</b></div>', unsafe_allow_html=True)
                        with col11:
                            st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 5px; border-radius: 5px; text-align: center;"><b>{row["Points"]}</b></div>', unsafe_allow_html=True)

                    # Also show the dataframe for export purposes (hidden in expander)
                    with st.expander("📋 View as Table"):
                        df_display = df.drop('Crest', axis=1)
                        st.dataframe(df_display, width="stretch")

                    # Visualization (only if we have data)
                    if not df.empty:
                        # Create a more informative chart with custom colors
                        df_chart = df.head(20).copy()

                        # Add color categories
                        colors = []
                        for pos in df_chart['Position']:
                            if pos <= 4:
                                colors.append('#28a745')  # Green for Champions League
                            elif pos <= 6:
                                colors.append('#17a2b8')  # Blue for Europa League
                            elif pos >= len(df_chart) - 2:
                                colors.append('#dc3545')  # Red for relegation
                            else:
                                colors.append('#6c757d')  # Gray for mid-table

                        fig = px.bar(
                            df_chart,
                            x='Team',
                            y='Points',
                            title='League Standings - Points Distribution',
                            labels={'Points': 'Points', 'Team': ''},
                            text='Points'
                        )

                        # Update bar colors
                        fig.update_traces(
                            marker_color=colors,
                            textposition='outside',
                            textfont_size=12
                        )

                        fig.update_layout(
                            xaxis_tickangle=-45,
                            height=500,
                            showlegend=False,
                            xaxis_title="",
                            yaxis_title="Points"
                        )

                        st.plotly_chart(fig, width="stretch")

                        # Legend explanation
                        st.markdown("""
                        <div style="display: flex; gap: 20px; justify-content: center; margin-top: 10px;">
                            <span style="color: #28a745;">● Champions League (1-4)</span>
                            <span style="color: #17a2b8;">● Europa League (5-6)</span>
                            <span style="color: #dc3545;">● Relegation Zone</span>
                        </div>
                        """, unsafe_allow_html=True)

                        # Team crests display below chart
                        st.markdown("#### 🏆 Team Crests")
                        crest_cols = st.columns(min(len(df_chart), 10))
                        for idx, (_, row) in enumerate(df_chart.iterrows()):
                            if idx < 10:  # Show top 10 teams
                                with crest_cols[idx]:
                                    if row['Crest']:
                                        st.image(row['Crest'], width=50)
                                        st.caption(f"{row['Position']}. {row['Team'][:15]}{'...' if len(row['Team']) > 15 else ''}")
                                    else:
                                        st.caption(f"{row['Position']}. {row['Team'][:15]}{'...' if len(row['Team']) > 15 else ''}")

                        # Show remaining teams if more than 10
                        if len(df_chart) > 10:
                            st.markdown("---")
                            remaining_cols = st.columns(min(len(df_chart) - 10, 10))
                            for idx in range(10, min(len(df_chart), 20)):
                                row = df_chart.iloc[idx]
                                with remaining_cols[idx - 10]:
                                    if row['Crest']:
                                        st.image(row['Crest'], width=50)
                                        st.caption(f"{row['Position']}. {row['Team'][:15]}{'...' if len(row['Team']) > 15 else ''}")
                                    else:
                                        st.caption(f"{row['Position']}. {row['Team'][:15]}{'...' if len(row['Team']) > 15 else ''}")

                # Export options
                exporter = DataExporter(standing_list)
                col1, col2 = st.columns(2)
                with col1:
                    csv_result = exporter.export_to_csv()
                    if csv_result["success"]:
                        st.download_button(
                            "📥 Download CSV",
                            data=csv_result["data"],
                            file_name="standings_data.csv",
                            mime="text/csv",
                            width="stretch"
                        )
                    else:
                        st.warning(csv_result["message"])

                with col2:
                    excel_result = exporter.export_to_excel()
                    if excel_result["success"]:
                        st.download_button(
                            "📥 Download Excel",
                            data=excel_result["data"],
                            file_name="standings_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            width="stretch"
                        )
                    else:
                        st.warning(excel_result["message"])
            else:
                st.warning("⚠️ Standings data not available for this competition")
# Matches search
st.sidebar.markdown("---")
show_matches = st.sidebar.checkbox('📅 Matches')

if show_matches:
    st.markdown('<p class="section-header">📅 Matches</p>', unsafe_allow_html=True)

    # Date range
    today = dt.date.today()
    default_from = today - dt.timedelta(days=7)
    default_to = today + dt.timedelta(days=7)
    date_range = st.date_input("Date range", (default_from, default_to))

    # Competition filter
    comp_ids = list(comp_dict.values())
    comp_names = list(comp_dict.keys())
    selected_comps = st.multiselect("Competitions (optional)", comp_names)
    comp_id_filter = [comp_dict[name] for name in selected_comps] if selected_comps else None

    status_filter = st.selectbox("Status", ["", "SCHEDULED", "LIVE", "IN_PLAY", "PAUSED", "FINISHED", "POSTPONED", "CANCELED"])

    date_from, date_to = (None, None)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date = date_range[0]
        end_date = date_range[1]
        if start_date and end_date:
            max_end = start_date + dt.timedelta(days=10)
            if end_date > max_end:
                st.warning("Date range exceeds 10 days. End date has been adjusted to match the API limit.")
                end_date = max_end
        date_from = start_date.isoformat() if start_date else None
        date_to = end_date.isoformat() if end_date else None

    with st.spinner("Loading matches..."):
        matches_resp = data.fetch_matches(
            date_from=date_from,
            date_to=date_to,
            competitions=comp_id_filter,
            status=status_filter or None,
            limit=50,
            offset=0
        )

    matches = matches_resp.get("matches", [])
    if matches:
        # Custom table so Home/Away can include crest + name in a single column
        header_cols = st.columns([2.2, 1.6, 2.2, 2.2, 1.2, 1.0])
        headers = ["Date", "Competition", "Home", "Away", "Status", "Score"]
        for col, header in zip(header_cols, headers):
            with col:
                st.markdown(f"**{header}**")

        st.markdown("---")

        for m in matches:
            home_team = m.get("homeTeam", {}) or {}
            away_team = m.get("awayTeam", {}) or {}
            home_crest = home_team.get("crest", "")
            away_crest = away_team.get("crest", "")
            home_name = home_team.get("name", "")
            away_name = away_team.get("name", "")

            row_cols = st.columns([2.2, 1.6, 2.2, 2.2, 1.2, 1.0])
            with row_cols[0]:
                st.write(m.get("utcDate", ""))
            with row_cols[1]:
                st.write(m.get("competition", {}).get("name", ""))
            with row_cols[2]:
                if home_crest:
                    st.markdown(
                        f'<div style="display:flex; align-items:center; gap:8px;">'
                        f'<span style="display:inline-flex; align-items:center; justify-content:center; '
                        f'background:#ffffff; border-radius:50%; width:26px; height:26px; '
                        f'box-shadow:0 0 0 1px rgba(0,0,0,0.2);">'
                        f'<img src="{home_crest}" width="20" height="20" /></span>'
                        f'<span>{home_name}</span></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.write(home_name)
            with row_cols[3]:
                if away_crest:
                    st.markdown(
                        f'<div style="display:flex; align-items:center; gap:8px;">'
                        f'<span style="display:inline-flex; align-items:center; justify-content:center; '
                        f'background:#ffffff; border-radius:50%; width:26px; height:26px; '
                        f'box-shadow:0 0 0 1px rgba(0,0,0,0.2);">'
                        f'<img src="{away_crest}" width="20" height="20" /></span>'
                        f'<span>{away_name}</span></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.write(away_name)
            with row_cols[4]:
                st.write(m.get("status", ""))
            with row_cols[5]:
                score = m.get("score", {}).get("fullTime", {})
                st.write(f"{score.get('home', '')} - {score.get('away', '')}")
    else:
        st.info("No matches found for the selected filters.")

# Future features
st.sidebar.markdown("---")
st.sidebar.header('🔮 Coming Soon')
st.sidebar.info('• Player detailed statistics\n• Match predictions\n• Historical data analysis')
