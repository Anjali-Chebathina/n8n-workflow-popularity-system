# n8n Workflow Popularity System 🚀

A production-grade system designed to identify, rank, and serve the most popular **n8n workflows** across multiple platforms. This project aggregates data from **YouTube**, **n8n Community Forums**, and **Google Trends** to provide a verifiable popularity index.



## 📋 Table of Contents
* [Overview](#overview)
* [System Architecture](#system-architecture)
* [Popularity Scoring Logic](#popularity-scoring-logic)
* [Tech Stack](#tech-stack)
* [Setup & Installation](#setup--installation)
* [API Documentation](#api-documentation)

---

## 🔍 Overview
This system solves the problem of finding "what's trending" in the n8n ecosystem. By combining social proof (YouTube), community engagement (Forums), and search intent (Google), it generates a `composite_score` for workflows, segmented by country (US & India).

**Key Features:**
* **Multi-Platform Ingestion:** Tracks views, likes, comments, and thread activity.
* **Weighted Scoring:** Ranks workflows based on engagement ratios, not just raw counts.
* **High Performance:** FastAPI + In-Memory Caching for response times **< 500ms**.
* **Automated Pipeline:** Cron-ready scripts for daily data refreshes.

---

## ⚙️ System Architecture
1.  **Collectors:** Python scripts fetch data via YouTube Data API v3, Discourse API, and PyTrends.
2.  **Database:** PostgreSQL stores normalized workflow data and raw metrics.
3.  **Scoring Engine:** A logic layer that calculates the weighted popularity index.
4.  **API Layer:** A RESTful interface built with FastAPI to serve JSON data.

---

## 📊 Popularity Scoring Logic
The system uses a weighted formula to ensure high-quality community engagement is valued alongside mass-market views:

* **YouTube (40%):** Focuses on reach and visual proof (Views, Likes, Comments).
* **Forum (35%):** Focuses on technical utility and contributor depth (Replies, Views, Contributors).
* **Google Trends (25%):** Focuses on regional search interest and growth.

---

## 🛠 Tech Stack
* **Backend:** Python 3.11, FastAPI
* **Database:** PostgreSQL, SQLAlchemy
* **Caching:** FastAPI-Cache2 (In-Memory)
* **APIs:** YouTube Data API v3, Discourse API
* **Deployment:** Uvicorn (ASGI Server)

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/n8n-popularity-system.git](https://github.com/yourusername/n8n-popularity-system.git)
cd n8n-popularity-system
```
### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
```bash
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/n8n_popularity
YOUTUBE_API_KEY=your_key_here
```
### 5. Run the API
```bash
python run_pipeline.py
python main.py
```
---

## 📖 API Documentation

Once the server is running, you can access the interactive documentation at:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **Redoc:** `http://127.0.0.1:8000/redoc`

### Sample Request
`GET /api/v1/workflows?platform=YouTube&country=US&limit=5`

### Sample Response
```json
{
  "status": "success",
  "timestamp": "2025-12-23T19:20:00",
  "count": 1,
  "data": [
    {
      "workflow_name": "Google Sheets to Slack Automation",
      "platform": "YouTube",
      "composite_score": 88.5,
      "country_code": "US",
      "popularity_metrics": {
        "views": 15000,
        "likes": 450,
        "comments": 32
      }
    }
  ]
}
