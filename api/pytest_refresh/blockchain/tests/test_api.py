import json
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse
from blockchain.models import Blockchain


@pytest.mark.django_db  # it's creating replica of django db for tests
class BasicBlockchainAPiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.blockchain_url = reverse("blockchain-list")

    def tearDown(self) -> None:
        pass


class TestGetBlockchain(BasicBlockchainAPiTestCase):
    def test_zero_blockchain_empty_list(self) -> None:
        response = self.client.get(self.blockchain_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_blockchain_list(self) -> None:
        test_blockchain = Blockchain.objects.create(
            name="Cardano",
            ticker="ADA",
        )

        response = self.client.get(self.blockchain_url)
        response_content = json.loads(response.content)[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content["name"], test_blockchain.name)
        self.assertEqual(response_content["ticker"], test_blockchain.ticker)
        self.assertEqual(response_content["type"], "Not Selected")
        self.assertIsNotNone(
            response_content["last_update"], test_blockchain.last_update
        )
        self.assertEqual(response_content["project_url"], "")
        self.assertEqual(response_content["market_cap"], 0)
        self.assertEqual(response_content["last_price"], 0)
        self.assertEqual(response_content["notes"], "")


class TestPostBlockchain(BasicBlockchainAPiTestCase):
    def test_blockchain_no_arguments(self) -> None:
        response = self.client.post(path=self.blockchain_url)
        self.assertEqual(response.status_code, 400)
        expected = {
            "name": ["This field is required."],
            "ticker": ["This field is required."],
        }
        self.assertDictEqual(json.loads(response.content), expected)

    def test_blockchain_no_argument_name(self) -> None:
        response = self.client.post(path=self.blockchain_url, data={"name": "Cardano"})
        self.assertEqual(response.status_code, 400)
        expected = {
            "ticker": ["This field is required."],
        }
        self.assertDictEqual(json.loads(response.content), expected)

    def test_blockchain_no_argument_ticker(self) -> None:
        response = self.client.post(path=self.blockchain_url, data={"ticker": "ADA"})
        self.assertEqual(response.status_code, 400)
        expected = {
            "name": ["This field is required."],
        }
        self.assertDictEqual(json.loads(response.content), expected)

    def test_blockchain_no_argument_duplicate_name_and_ticker(self) -> None:
        test_blockchain = Blockchain.objects.create(name="Cardano", ticker="ADA")
        response = self.client.post(
            path=self.blockchain_url, data={"name": "Cardano", "ticker": "ADA"}
        )
        self.assertEqual(response.status_code, 400)
        expected = {
            "name": ["blockchain with this name already exists."],
            "ticker": ["blockchain with this ticker already exists."],
        }
        self.assertDictEqual(json.loads(response.content), expected)

    def test_blockchain_no_argument_duplicate_name(self) -> None:
        test_blockchain = Blockchain.objects.create(name="Cardano", ticker="ADA")
        response = self.client.post(
            path=self.blockchain_url, data={"name": "Cardano", "ticker": "ADX"}
        )
        self.assertEqual(response.status_code, 400)
        expected = {
            "name": ["blockchain with this name already exists."],
        }
        self.assertDictEqual(json.loads(response.content), expected)

    def test_blockchain_no_argument_duplicate_ticker(self) -> None:
        test_blockchain = Blockchain.objects.create(name="Cardano", ticker="ADA")
        response = self.client.post(
            path=self.blockchain_url, data={"name": "Binance", "ticker": "ADA"}
        )
        self.assertEqual(response.status_code, 400)
        expected = {
            "ticker": ["blockchain with this ticker already exists."],
        }
        self.assertDictEqual(json.loads(response.content), expected)

    def test_blockchain_default_fields(self) -> None:
        response = self.client.post(
            path=self.blockchain_url, data={"name": "Binance", "ticker": "BNB"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['name'], 'Binance')
        self.assertEqual(response_content['ticker'], 'BNB')
        self.assertEqual(response_content['type'], 'Not Selected')
        self.assertEqual(response_content['project_url'], '')
        self.assertEqual(response_content['market_cap'], 0)
        self.assertEqual(response_content['last_price'], 0)
        self.assertEqual(response_content['notes'], '')

    def test_blockchain_default_type_wrong(self) -> None:
        response = self.client.post(
            path=self.blockchain_url, data={"name": "Binance", "ticker": "BNB", 'type': 'Babla'}
        )
        self.assertEqual(response.status_code, 400)
        response_content = json.loads(response.content)
        self.assertIn("is not a valid choice.", str(response_content))

    def test_blockchain_default_type_layer1(self) -> None:
        response = self.client.post(
            path=self.blockchain_url, data={"name": "Binance", "ticker": "BNB", 'type': 'Layer 1'}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['type'], 'Layer 1')

    def test_blockchain_str_validate_mark_cap(self) -> None:
        response = self.client.post(
            path=self.blockchain_url, data={"name": "Binance", "ticker": "BNB", 'type': 'Layer 1', 'market_cap': 'daf'}
        )
        self.assertEqual(response.status_code, 400)
        response_content = json.loads(response.content)
        print(response_content)

