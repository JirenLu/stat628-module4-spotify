Code:
Shinyapps:
Link: https://jirenlu.shinyapps.io/epicodes-recommendation/
The whole interface of shinyapp mimics the design of spotify, with search, display, recommendation and play functions. 
First of all, users can search for Podcasts or Episodes they are interested in, and the webpage will call spotify's api to search and show users the 6 closest options. 
When the user selects the target Podcasts or Episodes, the webpage will display detailed information on the top left, including name, album cover, release date, duration, detailed description, etc. 
The webpage also calculates the Topic Entry of the target Podcasts or Episodes. At the same time, the webpage calculates the Topic Entropy and Emotional Disposition of the target, searches from the database, and recommends the specified number of Episodes to the user, which are displayed in detail on the right side of the page for the user to view. 
The webpage also visualizes the recommendation basis at the bottom left for the user's reference. The webpage is also designed with a player to audition Episode clips, but the song-cutting function is not yet complete.

Data:
Raw data: The data download from api.
Cleaned data: data for modeling.
Labeled data: data with two tags.

Model:
Code for modeling.
