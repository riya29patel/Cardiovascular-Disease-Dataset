import joblib
import numpy as np
import pandas as pd

try:
    model = joblib.load("heart_disease_model.pkl")
    print(f"Model type: {type(model)}")
    
    if hasattr(model, "n_features_in_"):
        print(f"Number of features expected: {model.n_features_in_}")
    
    if hasattr(model, "feature_names_in_"):
        print(f"Feature names: {model.feature_names_in_}")
        
    # Try predicting with app.py features (12 features)
    try:
        # app.py features: age, gender, height, weight, bmi, systolic, diastolic, chol, gluc, smoke, alco, active
        dummy_12 = np.zeros((1, 12))
        model.predict(dummy_12)
        print("Model accepts 12 features (app.py style).")
    except Exception as e:
        print(f"Failed with 12 features: {e}")

    # Try predicting with app1.py features (10 features)
    try:
        # app1.py features: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak
        dummy_10 = np.zeros((1, 10))
        model.predict(dummy_10)
        print("Model accepts 10 features (app1.py style).")
    except Exception as e:
        print(f"Failed with 10 features: {e}")
        
        # Try 11 just in case
        try:
             dummy_11 = np.zeros((1, 11))
             model.predict(dummy_11)
             print("Model accepts 11 features.")
        except:
             pass
             
        # Try 13 just in case
        try:
             dummy_13 = np.zeros((1, 13))
             model.predict(dummy_13)
             print("Model accepts 13 features.")
        except:
             pass

except Exception as e:
    print(f"Error loading or inspecting model: {e}")
