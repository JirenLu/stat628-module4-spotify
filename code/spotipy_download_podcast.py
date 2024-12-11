import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# ducument: https://developer.spotify.com/documentation/web-api/reference/search

# 初始化 Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="",
    client_secret=""
))


# 定义一个函数，搜索播客
def search_podcasts(query, limit, offset=0):
    results = sp.search(q=query, type="show", limit=limit, offset=offset)
    podcasts = []
    for show in results.get('shows', {}).get('items', []):
        # 获取图片映射
        image_map = {image.get('height'): image.get('url') for image in show.get('images', [])}

        # 添加每个播客信息，使用 get 方法确保字段不存在时返回 None
        podcasts.append({
            "Search_Keyword": query,
            "Available_Markets": show.get('available_markets', None),
            # "Copyrights": show.get('copyrights', None),
            "Description": show.get('description', None),
            # "HTML_Description": show.get('html_description', None),
            "Explicit": show.get('explicit', None),
            "External_URL": show.get('external_urls', {}).get('spotify', None),
            "Href": show.get('href', None),
            "Podcast_ID": show.get('id', None),
            "Image_640": image_map.get(640, None),
            "Image_300": image_map.get(300, None),
            "Image_64": image_map.get(64, None),
            "Is_Externally_Hosted": show.get('is_externally_hosted', None),
            "Languages": show.get('languages', None),
            "Media_Type": show.get('media_type', None),
            "Name": show.get('name', None),
            "Publisher": show.get('publisher', None),
            "Type": show.get('type', None),
            # "URI": show.get('uri', None),
            "Total_Episodes": show.get('total_episodes', None)
        })
    return podcasts


# 批量搜索多个关键词
def batch_search_podcasts(categories, limit=50, delay=2):
    all_podcasts = []
    for queries in categories.values():
        for query in queries:
            print(f"Searching podcasts with keyword: {query}")
            for i in range(20):  # limit+offset不能超过1000，此处offset最大为950
                podcasts = search_podcasts(query, limit=limit, offset=i * limit)
                all_podcasts.extend(podcasts)
                # 添加延迟，防止超出请求限制
                time.sleep(delay)  # 设置延迟
    return all_podcasts


# 保存为 CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.drop_duplicates(subset="Podcast_ID", inplace=True)  # 去重
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Saved {len(df)} podcasts to {filename}")


'''
# 定义关键词列表
keywords = [
    "art", "business", "comedy", "crime", "culture", "economics", "education", "entertainment", "finance", "food",
    "gaming", "health", "history", "horror", "language", "music", "news", "parenting", "politics", "psychology",
    "science", "science fiction", "society", "sports", "spirituality", "sustainability", "technology", "travel"
]
# 混合策略
categories_list = {
    # 新闻类
    "news": ["news", "daily news", "current events", "breaking news", "world news", "political news"],
    # 喜剧类
    "comedy": ["comedy", "funny", "jokes", "stand-up comedy", "improv", "satire", "humor"],
    # 教育类
    "education": ["education", "learning", "self-improvement", "language learning", "teaching", "how to", "skills development", "online courses"],
    # 科技类
    "technology": ["technology", "gadgets", "AI", "programming", "coding", "software development", "innovation", "space tech", "cybersecurity"],
    # 犯罪类
    "true crime": ["true crime", "criminal justice", "mystery", "unsolved cases", "forensic science", "crime investigations", "legal analysis"],
    # 健康类
    "health": ["health", "fitness", "mental health", "nutrition", "wellness", "exercise", "medical breakthroughs", "therapy"],
    # 音乐类
    "music": ["music", "pop music", "classical music", "jazz", "rock", "hip hop", "electronic", "country music", "indie music"],
    # 历史类
    "history": ["history", "world history", "ancient history", "historical events", "archaeology", "war history", "cultural history"],
    # 娱乐类
    "entertainment": ["entertainment", "movies", "TV shows", "Hollywood", "celebrities", "pop culture", "fan theories", "fiction"],
    # 商业类
    "business": ["business", "startups", "entrepreneurship", "corporate culture", "marketing", "e-commerce", "productivity", "innovation"],
    # 金融类
    "finance": ["finance", "investing", "personal finance", "stock market", "cryptocurrency", "real estate", "financial planning", "economy"],
    # 文化类
    "culture": ["culture", "traditions", "anthropology", "art history", "literature", "philosophy", "global culture"],
    # 犯罪类扩展
    "crime": ["crime", "true crime", "mystery", "forensic investigations", "unsolved mysteries", "legal drama", "prisons"],
    # 艺术类
    "art": ["art", "visual art", "modern art", "painting", "design", "creative expression"],
    # 语言类
    "language": ["language", "linguistics", "language learning", "translation", "grammar", "multilingual communication"],
    # 食物类
    "food": ["food", "cooking", "recipes", "culinary arts", "baking", "nutrition"],
    # 旅行类
    "travel": ["travel", "adventure", "destinations", "road trips", "vacations", "backpacking"],
    # 心理类
    "psychology": ["psychology", "mental health", "emotions", "therapy", "self-help", "cognitive science"],
    # 社会类
    "society": ["society", "social issues", "human rights", "diversity", "inequality", "activism", "community"],
    # 经济类
    "economics": ["economics", "macroeconomics", "microeconomics", "global economy", "development", "trade", "policy analysis"],
    # 科幻类
    "science fiction": ["sci-fi", "science fiction", "futurism", "alien stories", "space adventures", "dystopia"],
    # 恐怖类
    "horror": ["horror", "ghost stories", "paranormal", "thriller", "psychological horror"],
    # 家庭与育儿类
    "parenting": ["parenting", "family life", "relationships", "child development", "motherhood", "fatherhood"],
    # 游戏类
    "gaming": ["gaming", "video games", "esports", "board games", "RPGs", "game development"],
    # 环境与可持续发展类
    "sustainability": ["sustainability", "environment", "climate change", "wildlife", "green living", "eco-friendly"],
    # 哲学与精神类
    "spirituality": ["spirituality", "meditation", "mindfulness", "religion", "philosophy", "personal growth"]
}
'''

categories_list = {
    # 艺术与娱乐：11
    "arts_entertainment": ["arts & entertainment", "books", "celebrities", "comedy", "design", "fiction", "film",
                           "literature", "pop culture", "stories", "tv"],
    # 商业与科技：7
    "business_technology": ["business", "business & technology", "careers", "economics", "finance", "marketing",
                            "technology"],
    # 教育类：6
    "educational": ["educational", "government", "history", "language", "philosophy", "science"],
    # 游戏：2
    "games": ["games", "video games"],
    # 生活方式与健康：12
    "lifestyle_health": ["beauty", "fashion", "fitness & nutrition", "food", "health", "hobbies", "lifestyle",
                         "meditation podcasts", "parenting", "relationships", "self-care", "sex"],
    # 新闻与政治：2
    "news_politics": ["news & politics", "politics"],
    # 体育与休闲：13
    "sports_recreation": ["baseball", "basketball", "boxing", "football", "hockey", "mma", "outdoor", "rugby",
                          "running", "soccer", "sports & recreation", "tennis", "wrestling"],
    # 真相犯罪：1
    "true_crime": ["true crime"]
}

# 搜索播客
podcasts = batch_search_podcasts(categories_list)
# 保存结果到 CSV
save_to_csv(podcasts, "podcasts_list.csv")
