from pytrends.request import TrendReq
import time

def fetch_google_trends(keywords, country_code):
    """
    Fetches relative search interest for specific regions.
    Satisfies Requirement 4.3 & 5.3.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # Google Trends has strict rate limits; we fetch in small batches
    pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo=country_code)
    data = pytrends.interest_over_time()

    results = []
    if not data.empty:
        averages = data.mean()
        for kw in keywords:
            results.append({
                "name": kw,
                "platform": "Google Search",
                "country": country_code,
                "metrics": {
                    "search_interest_score": round(averages[kw], 2)
                }
            })
    return results