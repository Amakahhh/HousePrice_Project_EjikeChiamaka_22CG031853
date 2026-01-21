# House Price Prediction System

A machine learning-powered web application that predicts house prices based on key property features using Random Forest Regression.

## Project Overview

This project implements a complete end-to-end machine learning solution:
- **Model**: Random Forest Regressor trained on house price data
- **Features**: 6 carefully selected features from the House Prices dataset
- **Web Framework**: Flask
- **Deployment**: Production-ready with environment variable support

## Features Used

The model predicts house prices based on:
1. **OverallQual** - Overall material and finish quality (1-10)
2. **GrLivArea** - Gross living area above ground (sq ft)
3. **TotalBsmtSF** - Total basement area (sq ft)
4. **GarageCars** - Garage capacity (number of cars)
5. **FullBath** - Number of full bathrooms
6. **YearBuilt** - Original construction year

## Project Structure

```
HousePrice_Project_EjikeChiamaka_22CG031853/
├── app.py                          # Flask web application
├── requirements.txt                # Project dependencies
├── HousePrice_hosted_webGUI_link.txt # Deployment information
├── model/
│   ├── model_building.ipynb        # Model training and evaluation
│   ├── house_price_model.pkl       # Trained model artifact
│   ├── scaler.pkl                  # Feature scaler artifact
│   └── selected_features.pkl       # Feature list artifact
├── templates/
│   └── index.html                  # Web interface
└── static/
    └── style.css                   # Styling
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/HousePrice_Project_EjikeChiamaka_22CG031853
cd HousePrice_Project_EjikeChiamaka_22CG031853
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare the Dataset
Download the House Prices dataset and place `house_prices_train.csv` in the `model/` directory.

### 4. Train the Model (Optional - Pre-trained model included)
Navigate to the `model/` directory and run:
```bash
jupyter notebook model_building.ipynb
```
Execute all cells to train the model and save artifacts.

### 5. Run the Web Application
```bash
python app.py
```
The application will be available at `http://localhost:5000`

## API Endpoints

### GET `/`
Serves the main web interface with prediction form.

**Response**: HTML page

### POST `/predict`
Makes a prediction based on provided house features.

**Request Body**:
```json
{
    "OverallQual": 7,
    "GrLivArea": 2000,
    "TotalBsmtSF": 1000,
    "GarageCars": 2,
    "FullBath": 2,
    "YearBuilt": 2010
}
```

**Response**:
```json
{
    "success": true,
    "predicted_price": 185000.50,
    "confidence_std": 25000.75,
    "features_used": ["OverallQual", "GrLivArea", "TotalBsmtSF", "GarageCars", "FullBath", "YearBuilt"],
    "input_values": {
        "OverallQual": 7,
        "GrLivArea": 2000,
        "TotalBsmtSF": 1000,
        "GarageCars": 2,
        "FullBath": 2,
        "YearBuilt": 2010
    }
}
```

### GET `/features`
Returns the list of features used by the model.

**Response**:
```json
{
    "success": true,
    "features": ["OverallQual", "GrLivArea", "TotalBsmtSF", "GarageCars", "FullBath", "YearBuilt"]
}
```

### GET `/health`
Health check endpoint for deployment monitoring.

**Response**:
```json
{
    "status": "OK",
    "model_loaded": true,
    "features": ["OverallQual", "GrLivArea", "TotalBsmtSF", "GarageCars", "FullBath", "YearBuilt"]
}
```

## Model Development

### Data Preprocessing
1. **Feature Selection**: Selected 6 features from 9 recommended features
2. **Missing Values**: Removed rows with missing values
3. **Train/Test Split**: 80/20 split BEFORE scaling (prevents data leakage)
4. **Feature Scaling**: StandardScaler fitted ONLY on training data
5. **Encoding**: All selected features are numerical - no encoding needed

### Model Architecture
- **Algorithm**: Random Forest Regressor
- **Hyperparameters**:
  - n_estimators: 100 trees
  - max_depth: 15
  - min_samples_split: 5
  - min_samples_leaf: 2

### Evaluation Metrics
The model is evaluated using standard regression metrics:
- **MAE** (Mean Absolute Error): Average absolute prediction error
- **MSE** (Mean Squared Error): Average squared prediction error
- **RMSE** (Root Mean Squared Error): Square root of MSE
- **R²** (Coefficient of Determination): Proportion of variance explained

## Model Persistence

The project uses **Joblib** for model serialization:
- `house_price_model.pkl` - Trained Random Forest model
- `scaler.pkl` - StandardScaler for feature normalization
- `selected_features.pkl` - List of features for validation

All artifacts are automatically loaded on application startup.

## Deployment

The application is deployment-ready and follows best practices:

### Environment Variables
- `PORT`: Application port (default: 5000)
- `FLASK_ENV`: Set to 'development' for debug mode (default: 'production')

### Example Deployment (Render.com)
```bash
# The application reads PORT from environment
# Debug mode is disabled in production
gunicorn app:app
```

## Key Implementation Details

### Correct Inference Logic
```python
# For regression with Random Forest:
predicted_price = float(model.predict(input_scaled)[0])  # Single value
# NOT: np.argmax(prediction) - this is for classification!
```

### Data Leakage Prevention
```python
# CORRECT: Split first, then scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler.fit(X_train)  # Fit on training data only
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

## Technologies Used

- **Python 3.9+**
- **Flask 2.3.3** - Web framework
- **scikit-learn 1.3.0** - Machine learning library
- **pandas 2.0.3** - Data manipulation
- **joblib 1.3.1** - Model serialization
- **Gunicorn 21.2.0** - Production server

## Troubleshooting

### Model Not Loading
- Verify all `.pkl` files are in the `model/` directory
- Check file permissions
- Ensure joblib version matches training environment

### Prediction Errors
- Verify all 6 input features are provided
- Check that feature values are within valid ranges
- See `/health` endpoint for model status

### Port Already in Use
The application uses environment variables for the port. Set a different port:
```bash
set PORT=8000  # Windows
python app.py
```

Or on Linux/Mac:
```bash
export PORT=8000
python app.py
```

## Future Improvements

1. Add more features for better predictions
2. Implement model versioning
3. Add prediction confidence intervals
4. Create API documentation with Swagger
5. Add database for prediction history
6. Implement user authentication

## Academic Information

- **Course**: CSC 415 - Artificial Intelligence
- **Institution**: [Your Institution]
- **Student**: Ejike Chiamaka
- **Matric Number**: 22CG031853
- **Submission Deadline**: Friday, January 22, 2026, 11:59 PM

## License

This project is submitted for academic purposes.

## Support

For issues or questions, please contact:
- Email: [Your Email]
- GitHub Issues: [GitHub Repository Issues]

---

**Note**: This is an academic project built to demonstrate machine learning model development, web application creation, and deployment best practices.
