import pytest
import json
import numpy as np
from app import app as flask_app
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    """Test that home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Concrete Strength Predictor' in response.data

def test_predict_missing_data(client):
    """Test prediction endpoint with missing data"""
    data = {
        'Cement': '350',
        # Missing other required fields
    }
    response = client.post('/predict', data=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'

def test_predict_invalid_values(client):
    """Test prediction endpoint with invalid values"""
    data = {
        'Cement': '-100',  # Invalid negative value
        'BlastFurnaceSlag': '100',
        'FlyAsh': '50',
        'Water': '175',
        'Superplasticizer': '5',
        'CoarseAggregate': '1000',
        'FineAggregate': '800',
        'Age': '28'
    }
    response = client.post('/predict', data=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'
    assert 'Negative value not allowed' in response_data['error']

@patch('tensorflow.keras.models.load_model')
def test_predict_valid_input(mock_load_model, client):
    """Test prediction endpoint with valid input"""
    # Mock the model prediction
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([[42.5]])
    mock_load_model.return_value = mock_model

    data = {
        'Cement': '350',
        'BlastFurnaceSlag': '100',
        'FlyAsh': '50',
        'Water': '175',
        'Superplasticizer': '5',
        'CoarseAggregate': '1000',
        'FineAggregate': '800',
        'Age': '28'
    }
    
    response = client.post('/predict', data=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'success'
    assert 'prediction' in response_data
    assert isinstance(response_data['prediction'], float)

def test_predict_non_numeric_input(client):
    """Test prediction endpoint with non-numeric input"""
    data = {
        'Cement': 'abc',  # Non-numeric input
        'BlastFurnaceSlag': '100',
        'FlyAsh': '50',
        'Water': '175',
        'Superplasticizer': '5',
        'CoarseAggregate': '1000',
        'FineAggregate': '800',
        'Age': '28'
    }
    response = client.post('/predict', data=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'

def test_404_error(client):
    """Test 404 error handler"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data['status'] == 'error'
    assert 'Not found' in response_data['error']

def test_model_load_failure(client):
    """Test behavior when model fails to load"""
    with patch('tensorflow.keras.models.load_model', side_effect=Exception('Model load failed')):
        response = client.post('/predict', data={})
        assert response.status_code == 503
        response_data = json.loads(response.data)
        assert response_data['status'] == 'error'
        assert 'Model not loaded' in response_data['error']