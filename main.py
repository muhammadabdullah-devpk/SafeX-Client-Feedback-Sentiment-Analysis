"""
SafeX Client Feedback Sentiment Analysis Pipeline
Student: Muhammad Abdullah
Email: meharabdullah4337@gmail.com
Internship Track: AI/ML (Group 3)
Task: Week 1 - Sentiment Analysis on Sample Client Feedback
"""

import os
import sys
import json
import pandas as pd

# Set utf-8 encoding for stdout on Windows if possible
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src.sentiment_analyzer import process_feedback_dataframe, extract_top_negative_alerts
from src.visualizer import plot_sentiment_distribution, plot_service_breakdown, plot_polarity_vs_subjectivity


def main():
    print("=" * 70)
    print("      SAFEX CYBERSECURITY & AI LABS - WEEK 1 TASK PIPELINE")
    print("      Student: Muhammad Abdullah | Track: AI/ML Group 3")
    print("      Task: Sentiment Analysis on Sample Client Feedback")
    print("=" * 70)

    # 1. Load Dataset
    data_path = os.path.join(os.path.dirname(__file__), "dataset", "client_feedback.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    print(f"\n[1/5] Loading client feedback dataset from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"      Successfully loaded {len(df)} client feedback records.")

    # 2. Run Sentiment Analysis
    print("\n[2/5] Performing hybrid sentiment analysis (VADER + TextBlob)...")
    analyzed_df = process_feedback_dataframe(df)
    
    # Summary stats
    cat_counts = analyzed_df['category'].value_counts()
    pos_cnt = cat_counts.get('Positive', 0)
    neu_cnt = cat_counts.get('Neutral', 0)
    neg_cnt = cat_counts.get('Negative', 0)
    total = len(analyzed_df)

    print("\n" + "-" * 50)
    print("  SENTIMENT DISTRIBUTION SUMMARY")
    print("-" * 50)
    print(f"  * Total Feedback Evaluated : {total}")
    print(f"  * Positive Feedback (Satisfied) : {pos_cnt} ({pos_cnt/total*100:.1f}%)")
    print(f"  * Neutral Feedback (Standard)   : {neu_cnt} ({neu_cnt/total*100:.1f}%)")
    print(f"  * Negative Feedback (Critical)  : {neg_cnt} ({neg_cnt/total*100:.1f}%)")
    print(f"  * Average Compound Score        : {analyzed_df['compound_score'].mean():.4f}")
    print("-" * 50)

    # 3. Extract Top 3 Most Negative Comments
    print("\n[3/5] Identifying Top 3 Most Critical Negative Comments for Follow-up...")
    top_alerts = extract_top_negative_alerts(analyzed_df, top_n=3)

    print("\n" + "=" * 70)
    print("  [!] CRITICAL CLIENT ESCALATION ALERTS (TOP 3 NEGATIVE REVIEWS)")
    print("=" * 70)
    for alert in top_alerts:
        print(f"\n[ALERT #{alert['rank']}] - Severity: {alert['severity']}")
        print(f"  Client Name  : {alert['client_name']} ({alert['service_type']})")
        print(f"  Rating / VADER Score : {alert['rating']}/5 | Compound: {alert['compound_score']}")
        print(f"  Feedback     : \"{alert['feedback_text']}\"")
        print(f"  Action Plan  : -> {alert['recommended_action']}")

    # 4. Save Outputs
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    csv_out = os.path.join(output_dir, "analyzed_client_feedback.csv")
    json_out = os.path.join(output_dir, "top_3_negative_alerts.json")
    
    analyzed_df.to_csv(csv_out, index=False)
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(top_alerts, f, indent=4)
        
    print(f"\n[4/5] Saved structured results to:")
    print(f"      - CSV : {csv_out}")
    print(f"      - JSON: {json_out}")

    # 5. Generate Visualizations
    print("\n[5/5] Generating publication-grade visualizations...")
    chart_dist = os.path.join(output_dir, "sentiment_distribution.png")
    chart_service = os.path.join(output_dir, "sentiment_by_service.png")
    chart_scatter = os.path.join(output_dir, "polarity_vs_subjectivity.png")
    
    plot_sentiment_distribution(analyzed_df, chart_dist)
    plot_service_breakdown(analyzed_df, chart_service)
    plot_polarity_vs_subjectivity(analyzed_df, chart_scatter)

    print("\n" + "=" * 70)
    print("  [+] PIPELINE EXECUTION COMPLETE SUCCESSFULLY!")
    print("  All deliverables generated in 'output/' directory.")
    print("=" * 70)


if __name__ == "__main__":
    main()
