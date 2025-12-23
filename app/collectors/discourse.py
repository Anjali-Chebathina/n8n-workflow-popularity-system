import requests

def fetch_discourse_workflows():
    """
    Fetches latest technical discussions from n8n forum.
    Satisfies Requirement 4.2.
    """
    url = "https://community.n8n.io/latest.json"
    response = requests.get(url)
    data = response.json()

    results = []
    for topic in data.get("topic_list", {}).get("topics", []):
        # We focus on topics with higher post counts or views
        results.append({
            "name": topic["title"],
            "platform": "Discourse",
            "metrics": {
                "replies": topic["posts_count"],
                "views": topic["views"],
                "likes": topic["like_count"]
            }
        })
    return results