import os
import sys
import html

# Path fix for 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.collectors.youtube import fetch_youtube_workflows
from app.collectors.discourse import fetch_discourse_workflows
from app.database import save_to_db
from app.scoring import calculate_composite_score

def run_sync():
    print("🚀 SYNC START: YouTube")
    try:
        yt_data = fetch_youtube_workflows()
        for item in yt_data:
            # Clean HTML entities like &amp; from titles
            clean_name = html.unescape(item['name'])
            score = calculate_composite_score(item['metrics']['views'], item['metrics']['likes'])
            save_to_db(clean_name, 'YouTube', item['metrics'], 'Global', score)
    except Exception as e:
        print(f"YouTube Error: {e}")

    print("🚀 SYNC START: Discourse")
    try:
        forum_data = fetch_discourse_workflows()
        for item in forum_data:
            clean_name = html.unescape(item['name'])
            # Score based on views and replies
            score = calculate_composite_score(item['metrics']['views'], item['metrics']['replies'])
            save_to_db(clean_name, 'Discourse', item['metrics'], 'Global', score)
    except Exception as e:
        print(f"Forum Error: {e}")

    print("✅ PIPELINE COMPLETE: Database updated.")

if __name__ == "__main__":
    run_sync()