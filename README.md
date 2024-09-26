# Project Report: Soccer time plantform

## 1. Project Summary

Since childhood, the world of football has fascinated me not only on the field but also in the intricate patterns of data it weaves. Discovering Streamlit felt like finding a hidden treasure, offering the power to transform football team data into vibrant visual stories. Hence, this stranlit football lightware web is made for my dream which comes true! This Sports Insights Application is designed to offer users comprehensive statistics and insights into sports teams, encompassing details such as wins, losses, scores, and dynamic performance graphs. Users have the ability to search for sports teams, access in-depth statistics, delve into dynamic performance word clouds, and export specific team statistics or performance videos from various games.

## 2. Description of the REST API(s)

### Football Data API

- **URL:** [https://www.football-data.org/index](https://www.football-data.org/index)
- **Documentation:** [Football Data API Documentation](https://www.football-data.org/documentation)
- **Description:** Fetch real-time and historical data about various sports teams, including wins, losses, and scores. This data will be associated with the Team Search and Display feature.

### ScoreBat Video API

- **URL:** [https://www.scorebat.com/video-api/](https://www.scorebat.com/video-api/)
- **Documentation:** [ScoreBat Video API Documentation](https://www.scorebat.com/video-api/documentation/)
- **Description:** Fetch game highlight data to be associated with the Dynamic Performance Graphs feature, providing users with visual insights into team performance over time.

## 3. List of Features

### Feature: Team Search and Display

- **Description:** Users can search for sports teams and view comprehensive statistics.
- **Data Class:** `Team`, `league`, `Cup`, `Countries`
- **REST API Endpoint:** `v4/competitions/`
- **Pages:** `search_page`, `search_page`

### Feature: Dynamic Performance Word Cloud

- **Description:** Display dynamic word clouds representing the team’s or league’s keywords over time for trend analysis.
- **Data Class:** `PerformanceWordCloud`
- **REST API Endpoint:** `amueller.github.io/word_cloud/index.html`
- **Pages:** `search_page`

### Feature: Wonderful football Games

- **Description:** Allow users to export or watch the specific team statistics or performance videos from different games.
- **Data Class:** `VideoData`
- **REST API Endpoint:** `/video-api/v3/feed`
- **Pages:** `watch_page`

## 4. References

- [Football Data API Documentation](https://www.football-data.org/documentation)
- [ScoreBat Video API Documentation](https://www.scorebat.com/video-api/documentation/)
- [Premier-League-2022-2023-Streamlit-App](https://github.com/TheOX027/Premier-League-2022-2023-Streamlit-App)
- [streamlit-datastrike](https://github.com/Bakero08/streamlit-datastrike)

## 5. Code Highlights

In the implementation of our football data application, several key aspects stood out: Firstly, I enhance the page by incorporating hyperlinks and widgets to showcase the various functions. Secondly, we distribute the functions across different pages using widgets, ensuring a comprehensive presentation. Additionally, we employ word cloud visualization to depict keywords within the JSON file, fostering a more user-friendly interaction with the data. The presentation of each league’s quantity, format, league table, team details, and top scorers follows a structured hierarchy, providing an organized display. Furthermore, a data export function is integrated, aiding users in comprehending and managing the data effectively. Lastly, the distinctive feature of watching matches and video highlights through the streamlined platform enhances user interaction, offering a unique and engaging experience.

## 6. Next Steps

Considering the current state of our application, several potential improvements and enhancements could be made:

(1)User Interface Refinement: Enhance the user interface for a more user-friendly experience, possibly incorporating modern design principles.
(2)Data Visualization: Implement data visualization features, such as graphs and charts, to provide users with a more comprehensive view of football-related statistics.
(3)User Authentication: Introduce user authentication to enable personalized features and preferences.

## 7. Reflection

Engaging in this project has truly been a priceless learning journey. The aspect that posed the greatest challenge revolved around establishing robust testing procedures, particularly in the realm of external APIs. Yet, surmounting these hurdles and accomplishing successful mocking for testing brought about a deeply gratifying sense of achievement. Reflecting on this experience, if granted the opportunity to tackle the project anew, I would prioritize early testing even more and explore additional features to enhance the overall user experience.
