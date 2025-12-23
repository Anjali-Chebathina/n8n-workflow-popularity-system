import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def save_to_db(name, platform, metrics, country="Global", score=0.0):
    # SQL logic with 'ON CONFLICT' to satisfy PRD Requirement 5.1 & 5.2
    query = text("""
        INSERT INTO workflows (workflow_name, platform, popularity_metrics, country_code, composite_score)
        VALUES (:name, :platform, :metrics, :country, :score)
        ON CONFLICT (workflow_name, platform, country_code) 
        DO UPDATE SET 
            popularity_metrics = EXCLUDED.popularity_metrics,
            composite_score = EXCLUDED.composite_score,
            last_updated = CURRENT_TIMESTAMP;
    """)
    
    # Convert dict to JSON string for PostgreSQL JSONB compliance
    json_metrics = json.dumps(metrics)

    with engine.connect() as conn:
        try:
            conn.execute(query, {
                "name": str(name), 
                "platform": str(platform), 
                "metrics": json_metrics, 
                "country": str(country), 
                "score": float(score)
            })
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"⚠️ Skipping entry due to error: {e}")