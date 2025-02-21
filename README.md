# Concrete Strength Predictor

A web application that predicts concrete compressive strength using an Artificial Neural Network (ANN) model. The application provides a user-friendly interface for inputting concrete mixture parameters and obtaining strength predictions.

## Features

- Real-time prediction of concrete compressive strength based on "Cement", "BlastFurnaceSlag", "FlyAsh", "Water", "Superplasticizer", "CoarseAggregate", "FineAggregate" and "Age"
- User-friendly web interface
- RESTful API endpoint for predictions
- Dockerized application
- Automated CI/CD pipeline

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (jQuery)
- **ML Model**: TensorFlow/Keras
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Prerequisites

- Python 3.12
- Docker
- Git

## Local Development Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t concrete-strength-predictor .
```

2. Run the container:
```bash
docker run -d -p 5000:5000 concrete-strength-predictor
```

## API Usage

The application exposes a RESTful API endpoint for making predictions:

```bash
POST /predict
Content-Type: application/x-www-form-urlencoded

Parameters:
- Cement: float (kg/m³)
- BlastFurnaceSlag: float (kg/m³)
- FlyAsh: float (kg/m³)
- Water: float (kg/m³)
- Superplasticizer: float (kg/m³)
- CoarseAggregate: float (kg/m³)
- FineAggregate: float (kg/m³)
- Age: integer (days)

Response:
{
    "prediction": float,
    "status": "success"
}
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:

1. Runs tests and linting on every push and pull request
2. Builds and pushes Docker image on main branch commits
3. Automatically deploys to production server

### Required Secrets

The following secrets need to be set in GitHub repository settings:

- `DOCKER_HUB_USERNAME`
- `DOCKER_HUB_ACCESS_TOKEN`
- `DEPLOY_HOST`
- `DEPLOY_USERNAME`
- `DEPLOY_SSH_KEY`

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.