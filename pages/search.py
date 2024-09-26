"""
pages_search.py from Yixiang Zhou

5001 final project for final submission
"""
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from models.data import FootballDataAPI
from models.produce import DataExporter
import os
from streamlit_extras.switch_page_button import switch_page
# streamlit run search.py


def leagues_display(choice, data):
    """
    Display league names based on the specified area choice.

    Parameters:
    - choice (str): The selected area for filtering leagues.
    - data (dict): The dictionary containing competition data.

    Returns:
    None

    This function iterates through the provided competition data and filters out
    the leagues that belong to the specified area (choice). It then displays
    the names of these leagues using Streamlit's 'subheader' function.

    Example:
    leagues_display("Europe", competition_data)
    """
    leagues = []
    for i in range(len(data["competitions"])):
        if data['competitions'][i]['area']['name'] == choice:
            leagues.append(data['competitions'][i]['name'])
    for i in range(len(leagues)):
        st.subheader((leagues[i]))


st.title('World Football Platform')
st.sidebar.title('Widget Section :bar_chart:')


with st.sidebar.expander('About the page'):
    st.write('This page not only provides a keyword word cloud, but also allows you to view and roughly compare the national leagues for each major region and country.')
    st.write('In addition, this page also allows you to view team information, top ten scorers, and standings for several competitions within your jurisdiction, and the top scorers list can be exported, mainly in CSV and XLSX formats.')
    st.write('Player data functionality is still under development')


data = FootballDataAPI()
data1 = data.fetch_data_general()

area_dict = {}
comp_dict = {}
for i in range(len(data1['competitions'])):
    area_dict[data1['competitions'][i]['area']['name']] = 0
    comp_dict[data1['competitions'][i]['name']] = 0


for i in range(len(data1['competitions'])):
    area_dict[data1['competitions'][i]['area']['name']] += 1
    comp_dict[data1['competitions'][i]['name']] += 1


area_df = pd.DataFrame(area_dict.items(), columns=['Country Name', 'Count'])
comp_df = pd.DataFrame(comp_dict.items(), columns=['League Name', 'Count'])


# word cloud part
newwc = st.sidebar.button('New Wordcloud!', key=1,)
newwc = True

if st.sidebar.button('Go back to main page'):
    switch_page("app")

if newwc:
    words = ' '.join(comp_df['League Name'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=820, height=410).generate(words)
    plt.imshow(wordcloud)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.xticks([])
    plt.yticks([])
    sns.despine(left=True, bottom=True)
    st.pyplot()

newwc = False

# Overall preview data
st.sidebar.header('General Stats: :chart_with_upwards_trend:\n')

with st.sidebar.expander('About this part'):
    st.write('Country Wise Distribution can be possible to make an approximate comparison of the number of competitions in each region or country.')
    st.write('Other sections categorise the competition information by continent or country.')


show_comp_stats = st.sidebar.checkbox('Country Wise Distribution', key=2)

# Show Country Wise Distribution
if show_comp_stats:
    st.header('Number Of Competitions Per Country:\n')
    chosen_nations = st.sidebar.multiselect('Choose Country', area_df['Country Name'], key=3)
    if len(chosen_nations) == 0:
        st.write('Choose a country..')
    else:
        sub_area_df = area_df[area_df['Country Name'].isin(chosen_nations)].reset_index().drop(['index'], axis=1)
        sub_area_df.index = range(1, len(sub_area_df) + 1)
        st.table(sub_area_df)
        st.write('\n')
        if sub_area_df.shape[0] != 0:
            sns.set_style('whitegrid')
            params = {'legend.fontsize': 18,
                'figure.figsize': (20, 8),
                'axes.labelsize': 22,
                'axes.titlesize': 22,
                'xtick.labelsize': 22,
                'ytick.labelsize': 22,
                'figure.titlesize': 22}
            plt.rcParams.update(params)
            fig, ax = plt.subplots()
            ax = sns.barplot(data=sub_area_df, x='Country Name', y='Count')
            if len(sub_area_df) > 5:
                plt.xticks(rotation=60)
            if len(sub_area_df) > 10:
                plt.xticks(rotation=90)
            sns.despine(left=True)
            st.pyplot(fig)


# show leagues per continent
show_leagues_per_continent = st.sidebar.checkbox('Football Leagues By Continent')

continents = ['Europe', 'Asia', 'Africa', 'North America', 'South America', 'Australia']

if show_leagues_per_continent:
    choice = st.sidebar.selectbox('Choose Continent', continents, key=4)
    write = choice + '\'s football leagues: '
    st.header(write + '\n')
    leagues_display(choice, data1)

# show leagues per country
show_leagues_per_country = st.sidebar.checkbox('Football Leagues By Country', key=5)

if show_leagues_per_country:
    helper = list(area_df[~area_df['Country Name'].isin(continents)]['Country Name'])
    choice = st.sidebar.selectbox('Choose Country', helper, key=6,)
    write = choice + '\'s football leagues: '
    st.header(write + '\n')
    leagues_display(choice, data1)


# Overall Competitions Stats data
st.sidebar.header('Competitions Stats: :dart:')

with st.sidebar.expander('About this part'):
    st.write('This section shows details of a number of competitions, mainly some of the current major leagues.')
    st.write('In addition to team-specific information, you can also view a list of the top 10 goal-scoring players in the league, a table of points, while they can each be exported.')

comp_dict = {}
free_tier_list = ['Serie A', 'UEFA Champions', 'European Champions', 'Ligue 1', 'Bundesliga', 'Eridivisie', 'Primeira Liga', 'Primera Division', 'FIFA World Cup']

for i in range(len(data1['competitions'])):
    if data1['competitions'][i]['name'] not in free_tier_list:
        continue
    comp_dict[data1['competitions'][i]['name']] = data1['competitions'][i]['id']

# Select a match
default = 'Select a Competition'
options = [default]

options = options + list(comp_dict.keys())
svalue = st.sidebar.selectbox('', options, key=7)


if svalue != default:
    st.title(svalue)
    if st.sidebar.checkbox('Team Info'):
        data = FootballDataAPI()
        data2 = data.fetch_data_from_endpoint("teams", comp_dict, svalue)
        st.header('Number of teams: ' + str(data2['count']))
        col1, col2 = st.columns(2)
        if len(data2['teams']):
            for i in range(len(data2['teams'])):
                if i % 2:
                    col1.subheader(data2['teams'][i]['name'])
                    if 'address' in data2['teams'][i].keys():
                        col1.write('Address: ' + data2['teams'][i]['address'])
                    else:
                        col1.write('Address: ' + 'Not Available (maybe in the future)')
                    if 'phone' in data2['teams'][i].keys():
                        if data2['teams'][i]['phone'] is not None:
                            col1.write('Phone: ' + (data2['teams'][i]['phone']))
                        else:
                            col1.write('Phone: ' + 'Not Available (maybe in the future)')
                    if 'website' in data2['teams'][i].keys():
                        if data2['teams'][i]['website'] is not None:
                            col1.write('Website: ' + data2['teams'][i]['website'])
                        else:
                            col1.write('Website: ' + 'Not Available (maybe in the future)')
                    if 'email' in data2['teams'][i].keys():
                        if data2['teams'][i]['email'] is not None:
                            col1.write('Email: ' + data2['teams'][i]['email'])
                        else:
                            col1.write('Email: ' + 'Not Available (maybe in the future)')
                    if 'founded' in data2['teams'][i].keys():
                        col1.write('Founded in ' + str(data2['teams'][i]['founded']))
                    else:
                        col1.write('Founded in: ' + 'Not Available (maybe in the future)')
                    if 'venue' in data2['teams'][i].keys():
                        if data2['teams'][i]['venue'] is not None:
                            col1.write('Venue: ' + data2['teams'][i]['venue'])
                        else:
                            col1.write('Venue: ' + 'Not Available (maybe in the future)')
                else:
                    col2.subheader(data2['teams'][i]['name'])
                    if 'address' in data2['teams'][i].keys():
                        col2.write('Address: ' + data2['teams'][i]['address'])
                    else:
                        col2.write('Address: ' + 'Not Available (maybe in the future)')
                    if 'phone' in data2['teams'][i].keys():
                        if data2['teams'][i]['phone'] is not None:
                            col2.write('Phone: ' + (data2['teams'][i]['phone']))
                    else:
                        col2.write('Phone' + 'Not Available (maybe in the future)')
                    if 'website' in data2['teams'][i].keys():
                        col2.write('Website: ' + data2['teams'][i]['website'])
                    else:
                        col2.write('Website' + 'Not Available (maybe in the future)')
                    if 'email' in data2['teams'][i].keys():
                        if data2['teams'][i]['email'] is not None:
                            col2.write('Email: ' + data2['teams'][i]['email'])
                        else:
                            col2.write('Website' + 'Not Available (maybe in the future)')
                    if 'founded' in data2['teams'][i].keys():
                        col2.write('Founded in ' + str(data2['teams'][i]['founded']))
                    else:
                        col2.write('Founded in: ' + 'Not Available (maybe in the future)')
                    if 'venue' in data2['teams'][i].keys():
                        if data2['teams'][i]['venue'] is not None:
                            col2.write('Venue: ' + data2['teams'][i]['venue'])
                        else:
                            col2.write('Venue: ' + 'Not Available (maybe in the future)')

    # Select Current Top 10 Shooters
    if st.sidebar.checkbox('Scorers'):
        data2 = FootballDataAPI.fetch_data_from_endpoint(data, 'scorers', comp_dict, svalue)
        if data2 is not None:
            st.subheader('Top 10 Scorers:')
            scorer_list = [{
                'Name': scorer['player']['name'],
                'Nationality': scorer['player']['nationality'],
                'Position': scorer['player']['position'],
                'Team': scorer['team']['name'],
                'Number of Goals': scorer['numberOfGoals']
                }for scorer in data2['scorers']]
            df = pd.DataFrame(scorer_list)
            df.index = range(1, len(df) + 1)
            df.columns = ['Name', 'Nationality', 'Position', 'Team', 'Number of Goals']
            st.table(df)

            if st.button("Exporting Scorers data to a CSV file"):
                scorer_data1 = DataExporter(scorer_list)
                scorer_list = scorer_data1.export_to_csv("scorer_data.csv")

                current_directory = os.getcwd()

                # Show download link on streamlit page
                st.markdown(f"Data exported to {current_directory} successfully.")

            if st.button("Exporting Scorers data to a Excel file"):
                scorer_data2 = DataExporter(scorer_list)
                scorer_list = scorer_data2.export_to_excel("scorer_data.xlsx")

                current_directory = os.getcwd()

                # Show download link on streamlit page
                st.markdown(f"Data exported to {current_directory} successfully.")
        else:
            st.write('Something wrong due to API unstable conditions')

    if st.sidebar.checkbox('Standings'):
        data3 = FootballDataAPI.fetch_data_from_new_urlversion(data, 'standings', comp_dict, svalue)
        st.subheader('Competition Ranking')

        if 'standings' in data3 and data3['standings'][0]['group'] is not None:
            # Iterate each ranking table
            for standings_table in data3['standings']:
                if len(standings_table['table']):
                    standing_list = []  # Initialising the list inside a loop

                    for i in range(len(standings_table['table'])):
                        standings_data = standings_table['table'][i]
                        standing = {
                            'Group': standings_table['group'],  # Use the group name of the current ranking table
                            'Team': standings_data['team']['name'],
                            'Position': standings_data['position'],
                            'Played Games': standings_data['playedGames'],
                            'Won': standings_data['won'],
                            'Draw': standings_data['draw'],
                            'Lost': standings_data['lost'],
                            'Points': standings_data['points'],
                            'Goals For': standings_data['goalsFor'],
                            'Goals Against': standings_data['goalsAgainst'],
                            'Goal Difference': standings_data['goalDifference']
                        }
                        standing_list.append(standing)

                    df = pd.DataFrame(standing_list)
                    df.index = range(1, len(df) + 1)
                    df.columns = ['Group', 'Team', 'Position', 'Played Games', 'Won', 'Draw', 'Lost', 'Points', 'Goals For', 'Goals Against', 'Goal Difference']
                    st.table(df)

        else:
            standing_list = []  # Initialise the list outside the loop
            for i in range(len(data3['standings'][0]['table'])):
                standings_data = data3['standings'][0]['table'][i]
                standing = {
                    'Team': standings_data['team']['name'],
                    'Position': standings_data['position'],
                    'Played Games': standings_data['playedGames'],
                    'Won': standings_data['won'],
                    'Draw': standings_data['draw'],
                    'Lost': standings_data['lost'],
                    'Points': standings_data['points'],
                    'Goals For': standings_data['goalsFor'],
                    'Goals Against': standings_data['goalsAgainst'],
                    'Goal Difference': standings_data['goalDifference']
                }
                standing_list.append(standing)

            df = pd.DataFrame(standing_list)
            df.index = range(1, len(df) + 1)
            df.columns = ['Team', 'Position', 'Played Games', 'Won', 'Draw', 'lost', 'Points', 'Goals For', 'Goals Against', 'Goals Difference']
            st.table(df)

        if st.button("Exporting Standing data to a CSV file"):
            standing_data1 = DataExporter(standing_list)
            standing_list = standing_data1.export_to_csv("standing_data.csv")

            current_directory = os.getcwd()

            # Show download link on streamlit page
            st.markdown(f"Data exported to {current_directory} successfully.")

        if st.button("Exporting Standing data to a Excel file"):
            standing_data2 = DataExporter(standing_list)
            standing_list = standing_data2.export_to_excel("standing_data.xlsx")

            current_directory = os.getcwd()

            # Show download link on streamlit page
            st.markdown(f"Data exported to {current_directory} successfully.")

st.sidebar.header('Player Stats: :necktie:')
st.sidebar.write('For the future project!!')
