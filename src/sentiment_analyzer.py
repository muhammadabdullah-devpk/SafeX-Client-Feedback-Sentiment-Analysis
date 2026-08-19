"""
SafeX Sentiment Analysis Engine
Author: Muhammad Abdullah (AI/ML Group 3)
Internship Field: AI/ML
Task: Sentiment Analysis on Sample Client Feedback
"""

import os
import re
import pandas as pd
import numpy as np

# NLP Libraries
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader_analyzer = SentimentIntensityAnalyzer()
except ImportError:
    vader_analyzer = None

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None


def clean_text(text: str) -> str:
    """Preprocess and clean text for NLP analysis."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def analyze_sentiment(text: str) -> dict:
    """
    Perform hybrid sentiment analysis using VADER and TextBlob.
    Combines rule-based lexicon evaluation with NLP polarity.
    """
    cleaned = clean_text(text)
    
    # 1. VADER Scoring
    if vader_analyzer:
        vader_scores = vader_analyzer.polarity_scores(cleaned)
        v_compound = vader_scores['compound']
        pos = vader_scores['pos']
        neu = vader_scores['neu']
        neg = vader_scores['neg']
    else:
        v_compound, pos, neu, neg = 0.0, 0.0, 1.0, 0.0

    # 2. TextBlob Scoring
    if TextBlob:
        blob = TextBlob(cleaned)
        tb_polarity = blob.sentiment.polarity
        tb_subjectivity = blob.sentiment.subjectivity
    else:
        tb_polarity = v_compound
        tb_subjectivity = 0.5

    # 3. Hybrid Combined Scoring
    if abs(v_compound) > 0.05 and abs(tb_polarity) > 0.05:
        final_score = (v_compound * 0.6) + (tb_polarity * 0.4)
    elif abs(v_compound) > 0.05:
        final_score = v_compound
    elif abs(tb_polarity) > 0.05:
        final_score = tb_polarity
    else:
        final_score = v_compound

    final_score = round(final_score, 4)

    # 4. Categorization logic
    if final_score >= 0.05:
        category = "Positive"
        sentiment_label = "Positive (Satisfied)"
    elif final_score <= -0.05:
        category = "Negative"
        sentiment_label = "Negative (Needs Attention)"
    else:
        category = "Neutral"
        sentiment_label = "Neutral (Standard)"

    return {
        "cleaned_text": cleaned,
        "compound_score": final_score,
        "vader_pos": round(pos, 4),
        "vader_neu": round(neu, 4),
        "vader_neg": round(neg, 4),
        "textblob_polarity": round(tb_polarity, 4),
        "textblob_subjectivity": round(tb_subjectivity, 4),
        "category": category,
        "sentiment_label": sentiment_label
    }


def process_feedback_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze all feedback records in a DataFrame."""
    results = []
    for _, row in df.iterrows():
        res = analyze_sentiment(row['feedback_text'])
        merged = {**row.to_dict(), **res}
        results.append(merged)
    
    analyzed_df = pd.DataFrame(results)
    return analyzed_df


def extract_top_negative_alerts(analyzed_df: pd.DataFrame, top_n: int = 3) -> list:
    """
    Extract and prioritize top N most negative client comments for immediate action.
    """
    neg_df = analyzed_df[analyzed_df['category'] == 'Negative'].sort_values(
        by=['compound_score', 'rating'], ascending=[True, True]
    )
    
    top_alerts = []
    for rank, (_, row) in enumerate(neg_df.head(top_n).iterrows(), start=1):
        issue_text = row['feedback_text'].lower()
        if "communication" in issue_text or "rude" in issue_text or "unresponsive" in issue_text:
            action = "Escalate to Client Relationship Lead for immediate apology and direct manager follow-up."
            severity = "CRITICAL"
        elif "delay" in issue_text or "late" in issue_text or "lost" in issue_text:
            action = "Conduct internal post-mortem on SLA delivery and issue expedited resolution report."
            severity = "HIGH"
        elif "false positive" in issue_text or "failed" in issue_text or "quality" in issue_text:
            action = "Assign Senior Security Architect to re-evaluate technical deliverables and offer complimentary re-test."
            severity = "CRITICAL"
        else:
            action = "Schedule client retention sync within 24 hours to address grievances."
            severity = "HIGH"

        alert = {
            "rank": rank,
            "feedback_id": row.get('feedback_id', f"FB-NEG-{rank}"),
            "client_name": row.get('client_name', 'Unknown Client'),
            "service_type": row.get('service_type', 'N/A'),
            "rating": int(row.get('rating', 1)),
            "compound_score": float(row.get('compound_score', -0.5)),
            "feedback_text": row.get('feedback_text', ''),
            "severity": severity,
            "recommended_action": action
        }
        top_alerts.append(alert)
        
    return top_alerts
