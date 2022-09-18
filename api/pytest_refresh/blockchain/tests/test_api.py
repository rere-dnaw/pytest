import json
from unittest import TestCase

import pytest
from django.urls import reverse
from blockchain.models import Blockchain


blockchain_url = reverse("blockchain-list")
pytestmark = (
    pytest.mark.django_db
)  # will add @pytest.mark.django_db decorator to each test


# |------TEST GET------|
# @pytest.mark.django_db  # it's creating replica of django db for tests
# decorator commented out because "pytestmark" parameter added into file
def test_zero_blockchain_empty_list(client) -> None:
    response = client.get(blockchain_url)

    assert response.status_code == 200
    assert json.loads(response.content)["results"] == []


def test_one_blockchain_list(client) -> None:
    test_blockchain = Blockchain.objects.create(
        name="Cardano",
        ticker="ADA",
    )

    response = client.get(blockchain_url)
    response_content = json.loads(response.content)["results"][0]

    assert response.status_code == 200
    assert response_content["ticker"] == test_blockchain.ticker
    assert response_content["type"] == "Not Selected"
    assert response_content["name"] == test_blockchain.name
    assert response_content["last_update"] != test_blockchain.last_update
    assert response_content["project_url"] == ""
    assert response_content["market_cap"] == 0
    assert response_content["last_price"] == 0
    assert response_content["notes"] == ""


# |------TEST POST------|
def test_blockchain_no_arguments(client) -> None:
    response = client.post(path=blockchain_url)
    assert response.status_code == 400
    expected = {
        "name": ["This field is required."],
        "ticker": ["This field is required."],
    }
    assert json.loads(response.content) == expected


def test_blockchain_no_argument_name(client) -> None:
    response = client.post(path=blockchain_url, data={"name": "Cardano"})
    assert response.status_code, 400
    expected = {
        "ticker": ["This field is required."],
    }
    assert json.loads(response.content) == expected


def test_blockchain_no_argument_ticker(client) -> None:
    response = client.post(path=blockchain_url, data={"ticker": "ADA"})
    assert response.status_code == 400
    expected = {
        "name": ["This field is required."],
    }
    assert json.loads(response.content) == expected


def test_blockchain_no_argument_duplicate_name_and_ticker(client) -> None:
    test_blockchain = Blockchain.objects.create(name="Cardano", ticker="ADA")
    response = client.post(
        path=blockchain_url, data={"name": "Cardano", "ticker": "ADA"}
    )
    assert response.status_code == 400
    expected = {
        "name": ["blockchain with this name already exists."],
        "ticker": ["blockchain with this ticker already exists."],
    }
    assert json.loads(response.content) == expected


def test_blockchain_no_argument_duplicate_name(client) -> None:
    test_blockchain = Blockchain.objects.create(name="Cardano", ticker="ADA")
    response = client.post(
        path=blockchain_url, data={"name": "Cardano", "ticker": "ADX"}
    )
    assert response.status_code == 400
    expected = {
        "name": ["blockchain with this name already exists."],
    }
    assert json.loads(response.content) == expected


def test_blockchain_no_argument_duplicate_ticker(client) -> None:
    test_blockchain = Blockchain.objects.create(name="Cardano", ticker="ADA")
    response = client.post(
        path=blockchain_url, data={"name": "Binance", "ticker": "ADA"}
    )
    assert response.status_code == 400
    expected = {
        "ticker": ["blockchain with this ticker already exists."],
    }
    assert json.loads(response.content) == expected


def test_blockchain_default_fields(client) -> None:
    response = client.post(
        path=blockchain_url, data={"name": "Binance", "ticker": "BNB"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content["name"] == "Binance"
    assert response_content["ticker"] == "BNB"
    assert response_content["type"] == "Not Selected"
    assert response_content["project_url"] == ""
    assert response_content["market_cap"] == 0
    assert response_content["last_price"] == 0
    assert response_content["notes"] == ""


def test_blockchain_default_type_wrong(client) -> None:
    response = client.post(
        path=blockchain_url,
        data={"name": "Binance", "ticker": "BNB", "type": "Babla"},
    )
    assert response.status_code == 400
    response_content = json.loads(response.content)
    assert "is not a valid choice." in str(response_content)


def test_blockchain_default_type_layer1(client) -> None:
    response = client.post(
        path=blockchain_url,
        data={"name": "Binance", "ticker": "BNB", "type": "Layer 1"},
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content["type"] == "Layer 1"


def test_blockchain_str_validate_mark_cap(client) -> None:
    response = client.post(
        path=blockchain_url,
        data={
            "name": "Binance",
            "ticker": "BNB",
            "type": "Layer 1",
            "market_cap": "daf",
        },
    )
    assert response.status_code == 400
    response_content = json.loads(response.content)
