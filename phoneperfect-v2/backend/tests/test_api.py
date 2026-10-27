import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True
    assert data["total_catalog_devices"] > 0

def test_get_brands():
    response = client.get("/api/v1/brands")
    assert response.status_code == 200
    brands = response.json()
    assert len(brands) >= 10
    brand_names = [b["name"].lower() for b in brands]
    assert any("samsung" in b for b in brand_names)
    assert any("apple" in b for b in brand_names)

def test_catalog_pagination_and_search():
    response = client.get("/api/v1/catalog?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] > 500

    # Test Search Query
    search_res = client.get("/api/v1/catalog?search=Galaxy")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert len(search_data["items"]) > 0
    assert all("galaxy" in item["model_name"].lower() or "samsung" in item["brand_name"].lower() for item in search_data["items"])

def test_phone_detail():
    response = client.get("/api/v1/catalog/galaxys24")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "galaxys24"
    assert data["brand"]["name"].lower() == "samsung"
    assert data["specification"] is not None
    assert len(data["prices"]) > 0

def test_recommendation_engine_hard_budget_constraint():
    # Budget strictly 30,000 INR
    budget = 30000.0
    payload = {
        "budget_max": budget,
        "primary_use": "GAMING",
        "priorities": {
            "performance": 5,
            "camera": 3,
            "battery": 4,
            "display": 4,
            "longevity": 3
        },
        "min_ram_gb": 8,
        "require_5g": True
    }
    response = client.post("/api/v1/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["budget_max"] == budget
    assert len(data["recommendations"]) > 0
    
    # HARD CONSTRAINT VERIFICATION: No recommended phone can exceed budget
    for rec in data["recommendations"]:
        assert rec["current_price"] <= budget, f"Phone {rec['phone']['model_name']} exceeds budget {rec['current_price']} > {budget}"
        assert rec["match_score"] >= 0 and rec["match_score"] <= 100
        assert len(rec["why_recommended"]) > 0
        assert "performance" in rec["score_breakdown"]

def test_phone_comparison():
    payload = {
        "phone_ids": ["galaxys24", "oneplus12"]
    }
    response = client.post("/api/v1/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["phones"]) == 2
    assert "chipset" in data["spec_comparison"]
    assert "battery" in data["spec_comparison"]
    assert len(data["advantages"]) == 2

def test_purchase_risk_assessment():
    response = client.get("/api/v1/risk/galaxys24")
    assert response.status_code == 200
    data = response.json()
    assert data["phone_id"] == "galaxys24"
    assert data["overall_risk_level"] in ["LOW", "MODERATE", "HIGH"]
    assert data["overall_risk_score"] >= 0 and data["overall_risk_score"] <= 100
    assert len(data["buyer_checklist"]) >= 2
