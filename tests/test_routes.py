import json
import os

from app import app, calculate_probabilities
import pytest


@pytest.fixture
def client():
    return app.test_client()


def test_probabilities_no_k(client):
    ret = client.get('/probabilities')
    assert ret.status_code == 200

    env_start_value = int(os.environ.get('START_VALUE'))
    env_end_value = int(os.environ.get('END_VALUE'))
    assert json.loads(ret.data) == {'probabilities': calculate_probabilities(env_start_value, env_end_value)}


@pytest.mark.parametrize("k", range(int(os.environ.get('START_VALUE')), int(os.environ.get('END_VALUE'))+1))
def test_probabilities_with_k_value(client, k):
    ret = client.get(f'/probabilities', headers={'k': k})
    assert ret.status_code == 200
    assert json.loads(ret.data) == {'probability': k/ (2*k - 1)}


@pytest.mark.parametrize("k", [int(os.environ.get('START_VALUE')) - 1, int(os.environ.get('END_VALUE'))+1])
def test_probabilities_k_out_of_range(client, k):
    ret = client.get(f'/probabilities', headers={'k': k})
    assert ret.status_code == 400
    assert ret.data == b'Value out of range'


def test_probabilities_k_invalid(client):
    ret = client.get('/probabilities', headers={'k': 'tt'})
    assert ret.status_code == 400
    assert ret.data == b'Invalid value for "k"'
