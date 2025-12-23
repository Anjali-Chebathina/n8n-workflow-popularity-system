import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def fetch_youtube_workflows(query="n8n workflow"):
    """
    Fetches top n8n videos and their statistics from YouTube.
    Satisfies Requirement 4.1.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    # Search for relevant videos
    search_request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=25,
        type="video",
        order="viewCount"
    )
    search_response = search_request.execute()

    results = []
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]

        # Get detailed metrics (views, likes, comments)
        video_request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        video_stats = video_request.execute()["items"][0]["statistics"]

        results.append({
            "name": title,
            "platform": "YouTube",
            "metrics": {
                "views": int(video_stats.get("viewCount", 0)),
                "likes": int(video_stats.get("likeCount", 0)),
                "comments": int(video_stats.get("commentCount", 0))
            }
        })
    return results