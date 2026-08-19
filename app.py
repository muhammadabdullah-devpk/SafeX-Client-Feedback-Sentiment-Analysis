"""
SafeX Sentiment Intelligence Web Application
Author: Muhammad Abdullah (AI/ML Group 3)
Interactive Dashboard for Client Sentiment Analysis Demo
"""

import os
import pandas as pd
from flask import Flask, render_template, request, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "client_feedback.csv")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=OUTPUT_DIR,
    static_url_path="/static"
)

from src.sentiment_analyzer import process_feedback_dataframe, extract_top_negative_alerts, analyze_sentiment
from src.visualizer import plot_sentiment_distribution, plot_service_breakdown, plot_polarity_vs_subjectivity


def ensure_data_analyzed():
    """Ensure data is loaded, processed, and charts are generated."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(DATASET_PATH)
    analyzed_df = process_feedback_dataframe(df)
    
    # Save CSV
    analyzed_df.to_csv(os.path.join(OUTPUT_DIR, "analyzed_client_feedback.csv"), index=False)
    
    # Always regenerate charts to keep them fresh
    dist_img = os.path.join(OUTPUT_DIR, "sentiment_distribution.png")
    serv_img = os.path.join(OUTPUT_DIR, "sentiment_by_service.png")
    scat_img = os.path.join(OUTPUT_DIR, "polarity_vs_subjectivity.png")
    
    plot_sentiment_distribution(analyzed_df, dist_img)
    plot_service_breakdown(analyzed_df, serv_img)
    plot_polarity_vs_subjectivity(analyzed_df, scat_img)
        
    return analyzed_df


@app.route("/")
def index():
    analyzed_df = ensure_data_analyzed()
    total_count = len(analyzed_df)
    counts = analyzed_df['category'].value_counts()
    
    pos_count = int(counts.get('Positive', 0))
    neu_count = int(counts.get('Neutral', 0))
    neg_count = int(counts.get('Negative', 0))
    
    top_alerts = extract_top_negative_alerts(analyzed_df, top_n=3)
    feedback_list = analyzed_df.to_dict(orient="records")
    
    return render_template(
        "index.html",
        total_count=total_count,
        pos_count=pos_count,
        neu_count=neu_count,
        neg_count=neg_count,
        top_alerts=top_alerts,
        feedback_list=feedback_list
    )


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    result = analyze_sentiment(text)
    return jsonify(result)


if __name__ == "__main__":
    ensure_data_analyzed()
    print("\n[+] SafeX Sentiment Dashboard running at: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
