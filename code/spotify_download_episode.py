import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# document:
# https://spotipy.readthedocs.io/en/2.24.0/index.html#spotipy.client.Spotify.show_episodes
# https://developer.spotify.com/documentation/web-api/reference/get-a-shows-episodes

# 初始化 Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="",
    client_secret=""
))


def search_episodes(podcast_id, limit=10):
    results = sp.show_episodes(show_id=podcast_id, limit=limit)
    # print(results)
    episodes = []
    for episode in results.get('items', []):
        # 获取图片映射
        if episode is None:
            continue
        image_map = {image.get('height'): image.get('url') for image in (episode.get('images') or [])}
        # print(episode)
        episodes.append({
            "Podcast_ID": podcast_id,
            "Audio_Preview_URL": episode.get('audio_preview_url', None),
            "Description": episode.get('description', None),
            # "HTML_Description": episode.get('html_description', None),
            "Duration_MS": episode.get('duration_ms', None),
            # "Explicit": episode.get('explicit', None),
            "External_URL": episode.get('external_urls', {}).get('spotify', None),
            "Href": episode.get('href', None),
            "Episode_ID": episode.get('id', None),
            "Image_640": image_map.get(640, None),
            "Image_300": image_map.get(300, None),
            "Image_64": image_map.get(64, None),
            # "Is_Externally_Hosted": episode.get('is_externally_hosted', None),
            # "Is_Playable": episode.get('is_playable', None),
            # "Language": episode.get('language', None),
            "Languages": episode.get('languages', None),
            "Name": episode.get('name', None),
            "Release_Date": episode.get('release_date', None),
            # "Release_Date_Precision": episode.get('release_date_precision', None),
            # "Resume_Point": episode.get('resume_point', None),
            # "Type": episode.get('type', None),
            # "URI": episode.get('uri', None)
        })
    return episodes


all_episodes = []
podcast_df = pd.read_csv("podcasts_list.csv", encoding="utf-8")
for index, podcast_id in podcast_df['Podcast_ID'].items():
    if index % 100 == 0:
        print(index)
    episodes = search_episodes(podcast_id)
    all_episodes.extend(episodes)
    time.sleep(0.15)

df = pd.DataFrame(all_episodes)
# df.drop_duplicates(subset="Episode_ID", inplace=True)  # 去重
filename = "episodes_list.csv"
df.to_csv(filename, index=False, encoding="utf-8")
print(f"Saved {len(df)} episodes to {filename}")
