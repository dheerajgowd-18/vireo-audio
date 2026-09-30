"""Automated tests for text classification, evaluation sampling, and defect signal detection."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.text_classifier import (
    TAXONOMY_CATEGORIES,
    TAXONOMY_OUTCOMES,
    detect_hardware_defect_signal,
    create_stratified_evaluation_sample,
    generate_ground_truth,
    LocalTicketClassifier,
    evaluate_predictions,
)


def test_taxonomy_labels_are_valid():
    """Verify taxonomy categories and outcomes adhere to the defined specification."""
    expected_categories = {
        "delivery_shipping", "returns_refunds", "billing_payment",
        "charging_battery", "connectivity_pairing", "hardware_audio_defect",
        "cancellation", "product_enquiry_setup", "other_unclear"
    }
    expected_outcomes = {
        "replacement_approved", "refund_processed", "troubleshooting_resolved",
        "courier_escalated", "store_credit_issued", "unresolved_ambiguous"
    }
    assert set(TAXONOMY_CATEGORIES) == expected_categories
    assert set(TAXONOMY_OUTCOMES) == expected_outcomes


def test_classifier_output_schema_and_bounds():
    """Verify classifier output dictionary contains required keys and confidence in [0, 1]."""
    classifier = LocalTicketClassifier()
    # Fit with minimal toy data
    train_texts = [
        "cancel order please",
        "where is my package tracking",
        "left earbud is not charging",
        "refund not received yet",
    ]
    train_labels = ["cancellation", "delivery_shipping", "charging_battery", "returns_refunds"]
    classifier.fit(train_texts, train_labels)
    
    test_texts = ["please cancel my order VR123", "left earbud dead"]
    test_notes = ["cancelled before dispatch", "rplc raised"]
    preds = classifier.predict(test_texts, test_notes)
    
    required_keys = {"issue_category", "resolution_outcome", "hardware_defect_signal", "confidence", "is_rule_override"}
    for p in preds:
        assert set(p.keys()) == required_keys
        assert p["issue_category"] in TAXONOMY_CATEGORIES
        assert p["resolution_outcome"] in TAXONOMY_OUTCOMES
        assert isinstance(p["hardware_defect_signal"], bool)
        assert 0.0 <= p["confidence"] <= 1.0


def test_ai_output_cannot_introduce_unsupported_categories():
    """Ensure that classifier never outputs a category outside the official taxonomy."""
    classifier = LocalTicketClassifier()
    train_texts = ["cancel order", "delivered late"]
    train_labels = ["cancellation", "delivery_shipping"]
    classifier.fit(train_texts, train_labels)
    
    preds = classifier.predict(["some random ambiguous text"])
    assert preds[0]["issue_category"] in TAXONOMY_CATEGORIES


def test_hardware_defect_signal_accuracy():
    """Verify that hardware defect signals detect physical failures and ignore unrelated issues."""
    assert detect_hardware_defect_signal("the left earbud is not charging at all") is True
    assert detect_hardware_defect_signal("one of them never gets the green light in the case") is True
    assert detect_hardware_defect_signal("charging pins damaged on the pulse 2") is True
    assert detect_hardware_defect_signal("no sound from the right earbud") is True
    
    # Negative cases
    assert detect_hardware_defect_signal("tracking is not updating for my order") is False
    assert detect_hardware_defect_signal("card charged two times please refund") is False
    assert detect_hardware_defect_signal("coupon code invalid") is False


def test_junk_text_handled_separately():
    """Verify that telephony junk text is excluded from evaluation sampling."""
    tickets = pd.DataFrame([
        {"ticket_id": "T1", "category": "Delivery", "channel": "chat", "replacement_issued": "N", "csat_score": 4.0, "customer_message": "my order is delayed"},
        {"ticket_id": "T2", "category": "Delivery", "channel": "voice", "replacement_issued": "N", "csat_score": np.nan, "customer_message": "[IVR transcript] [line dropped]"},
        {"ticket_id": "T3", "category": "Delivery", "channel": "chat", "replacement_issued": "N", "csat_score": 5.0, "customer_message": "[inaudible] ... charging"},
        {"ticket_id": "T4", "category": "Delivery", "channel": "chat", "replacement_issued": "N", "csat_score": 5.0, "customer_message": "test"},
    ])
    
    sample, junk_count = create_stratified_evaluation_sample(tickets, sample_size=1, random_seed=42)
    assert junk_count == 3
    assert len(sample) == 1
    assert sample.iloc[0]["ticket_id"] == "T1"


def test_deterministic_seed_reproducibility():
    """Verify that evaluation sampling with the same seed produces identical results."""
    # Create 20 synthetic tickets
    data = []
    for i in range(20):
        data.append({
            "ticket_id": f"T{i:03d}",
            "category": "Charging" if i % 2 == 0 else "Delivery",
            "channel": "chat" if i % 3 == 0 else "email",
            "replacement_issued": "Y" if i % 4 == 0 else "N",
            "csat_score": 4.0 if i % 5 == 0 else np.nan,
            "customer_message": f"Customer issue message number {i} with sufficient text length",
        })
    tickets = pd.DataFrame(data)
    
    sample_a, _ = create_stratified_evaluation_sample(tickets, sample_size=6, random_seed=42)
    sample_b, _ = create_stratified_evaluation_sample(tickets, sample_size=6, random_seed=42)
    
    pd.testing.assert_frame_equal(sample_a, sample_b)


def test_full_data_inference_preserves_row_count():
    """Verify that predicting across a dataset preserves the exact row count."""
    classifier = LocalTicketClassifier()
    classifier.fit(["cancel order", "delivered late"], ["cancellation", "delivery_shipping"])
    
    df = pd.DataFrame([
        {"ticket_id": "T1", "customer_message": "cancel my order", "agent_notes": "cancelled"},
        {"ticket_id": "T2", "customer_message": "package not here", "agent_notes": "awb checked"},
        {"ticket_id": "T3", "customer_message": "cancel order please", "agent_notes": "done"},
    ])
    
    preds = classifier.predict(df["customer_message"].tolist(), df["agent_notes"].tolist())
    assert len(preds) == len(df)


def test_source_category_never_overwritten():
    """Verify that original ticket category is not overwritten when derived category is added."""
    df = pd.DataFrame([
        {"ticket_id": "T1", "category": "Other", "customer_message": "cancel order please", "agent_notes": "done"},
    ])
    classifier = LocalTicketClassifier()
    classifier.fit(["cancel order", "delayed"], ["cancellation", "delivery_shipping"])
    
    preds = classifier.predict(df["customer_message"].tolist(), df["agent_notes"].tolist())
    df["ai_issue_category"] = [p["issue_category"] for p in preds]
    
    # Original remains "Other", AI is "cancellation"
    assert df.iloc[0]["category"] == "Other"
    assert df.iloc[0]["ai_issue_category"] == "cancellation"


def test_model_artifact_serialization(tmp_path):
    """Verify model artifacts can be saved, loaded, and produce identical predictions."""
    classifier = LocalTicketClassifier()
    classifier.fit(["cancel order", "delayed package"], ["cancellation", "delivery_shipping"])
    
    test_text = ["cancel order immediately"]
    orig_pred = classifier.predict(test_text)
    
    save_file = tmp_path / "model.pkl"
    classifier.save(save_file)
    
    loaded_classifier = LocalTicketClassifier()
    loaded_classifier.load(save_file)
    loaded_pred = loaded_classifier.predict(test_text)
    
    assert orig_pred == loaded_pred


def test_evaluation_metric_calculations():
    """Verify evaluation metric computation on known toy labels."""
    y_true = ["cancellation", "cancellation", "delivery_shipping"]
    y_pred = ["cancellation", "delivery_shipping", "delivery_shipping"]
    
    res = evaluate_predictions(y_true, y_pred)
    assert pytest.approx(res["accuracy"], 0.01) == 2 / 3
    assert res["error_count"] == 1
    assert "cancellation" in res["labels"]
    assert "delivery_shipping" in res["labels"]
