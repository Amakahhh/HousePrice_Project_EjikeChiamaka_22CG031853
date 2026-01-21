# DEPLOYMENT GUIDE - STEP BY STEP

## Choose Your Platform

### OPTION 1: Render.com (EASIEST - RECOMMENDED) ⭐

**Why Render?**: Easiest deployment, free tier, automatic scaling

#### Steps:

1. **Create Render Account**
   - Go to: https://render.com
   - Sign up with GitHub

2. **Push Project to GitHub First**
   ```bash
   # In project root
   git init
   git add .
   git commit -m "House Price Prediction System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/HousePrice_Project_EjikeChiamaka_22CG031853
   git push -u origin main
   ```

3. **Deploy on Render**
   - Login to Render.com
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub repository
   - Select: HousePrice_Project_EjikeChiamaka_22CG031853
   - Fill in:
     * **Name**: house-price-prediction (lowercase, no spaces)
     * **Runtime**: Python 3
     * **Build Command**: `pip install -r requirements.txt`
     * **Start Command**: `gunicorn app:app`
   - Click "Advanced"
     * Add Environment Variable:
       - Key: `FLASK_ENV`
       - Value: `production`
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Get your URL: https://house-price-prediction.render.com

4. **Test Your Deployment**
   ```
   - Visit: https://house-price-prediction.render.com
   - Fill form and test
   - Test /health: https://house-price-prediction.render.com/health
   ```

---

### OPTION 2: PythonAnywhere

**Why PythonAnywhere?**: Good for Python apps, web-based interface

#### Steps:

1. **Create Account**
   - Go to: https://www.pythonanywhere.com
   - Sign up (free tier available)

2. **Upload Code**
   - Consoles → Bash
   - ```bash
     git clone https://github.com/YOUR_USERNAME/HousePrice_Project_EjikeChiamaka_22CG031853
     cd HousePrice_Project_EjikeChiamaka_22CG031853
     pip install -r requirements.txt
     ```

3. **Configure Web App**
   - Web → Add a new web app
   - Python 3.9
   - Flask
   - Path: `/home/YOUR_USERNAME/HousePrice_Project_EjikeChiamaka_22CG031853`
   - Edit WSGI file:
     ```python
     import sys
     sys.path.insert(0, '/home/YOUR_USERNAME/HousePrice_Project_EjikeChiamaka_22CG031853')
     from app import app as application
     ```

4. **Reload & Test**
   - Web → Reload
   - Visit: https://YOUR_USERNAME.pythonanywhere.com

---

### OPTION 3: Streamlit Cloud

**Why Streamlit?**: Easiest for quick deployment

#### Steps:

1. **Modify app.py** (Create alternative app_streamlit.py)
   ```python
   import streamlit as st
   import joblib
   import numpy as np
   import pandas as pd
   
   st.set_page_config(page_title="House Price Prediction")
   st.title("🏠 House Price Prediction System")
   
   # Load model
   model = joblib.load('model/house_price_model.pkl')
   scaler = joblib.load('model/scaler.pkl')
   features = joblib.load('model/selected_features.pkl')
   
   # Create form
   col1, col2, col3 = st.columns(3)
   
   with col1:
       overall_qual = st.number_input("Overall Quality", 1, 10, 7)
       gr_liv_area = st.number_input("Living Area (sq ft)", 0, 10000, 2000)
       total_bsmt_sf = st.number_input("Basement Area (sq ft)", 0, 10000, 1000)
   
   with col2:
       garage_cars = st.number_input("Garage Cars", 0, 5, 2)
       full_bath = st.number_input("Full Bathrooms", 0, 10, 2)
       year_built = st.number_input("Year Built", 1800, 2100, 2010)
   
   # Make prediction
   if st.button("Predict Price"):
       input_data = pd.DataFrame([[
           overall_qual, gr_liv_area, total_bsmt_sf,
           garage_cars, full_bath, year_built
       ]], columns=features)
       
       input_scaled = scaler.transform(input_data)
       prediction = float(model.predict(input_scaled)[0])
       
       st.success(f"Predicted Price: ${prediction:,.2f}")
   ```

2. **Push to GitHub**
   ```bash
   git add app_streamlit.py
   git commit -m "Add Streamlit version"
   git push
   ```

3. **Deploy on Streamlit**
   - Go to: https://streamlit.io/cloud
   - Sign up with GitHub
   - New app
   - Select repository
   - Main file path: `app_streamlit.py`
   - Deploy
   - URL: https://your-app-name.streamlit.app

---

## After Deployment

### 1. Test Your Live App
```bash
# Test the web interface
Visit your live URL and test the form

# Test health endpoint
curl YOUR_LIVE_URL/health

# Test features endpoint
curl YOUR_LIVE_URL/features

# Test prediction (use curl or Postman)
curl -X POST YOUR_LIVE_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "OverallQual": 7,
    "GrLivArea": 2000,
    "TotalBsmtSF": 1000,
    "GarageCars": 2,
    "FullBath": 2,
    "YearBuilt": 2010
  }'
```

### 2. Update HousePrice_hosted_webGUI_link.txt
```
Name: Ejike Chiamaka
Matric Number: 22CG031853
Machine Learning Algorithm Used: Random Forest Regressor
Model Persistence Method: Joblib
Live URL of the Hosted Application: https://house-price-prediction.render.com
GitHub Repository Link: https://github.com/YOUR_USERNAME/HousePrice_Project_EjikeChiamaka_22CG031853
```

### 3. Final Verification
- [ ] App loads without errors
- [ ] Form displays all 6 fields
- [ ] Prediction works correctly
- [ ] Results format with currency
- [ ] /health endpoint returns 200 OK
- [ ] /features endpoint returns feature list

### 4. Submit to Scorac
- [ ] Verify all files present
- [ ] HousePrice_hosted_webGUI_link.txt filled correctly
- [ ] Upload entire folder to Scorac
- [ ] Submit before Friday 11:59 PM

---

## Troubleshooting Deployment

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Ensure requirements.txt in root, run pip install -r requirements.txt |
| ".pkl files not found" | Ensure model, scaler, features .pkl files in model/ directory |
| Port error | For Render, don't specify port - it uses $PORT environment variable |
| 500 error | Check platform logs, test /health endpoint |
| CORS error | Not an issue - app only serves its own frontend |
| Slow prediction | This is normal on free tiers - model size ~10MB |
| "Permission denied" | Ensure .pkl files have read permissions |
| App crashes | Check that house_prices_train.csv exists and is valid |

---

## Environment Variables (Render.com)

In Render dashboard, under "Environment":

```
FLASK_ENV=production
PYTHONUNBUFFERED=true
```

These ensure:
- Flask runs in production mode (debug=False)
- Logs stream in real-time

---

## Performance Tips

### For Free Tier:
- First request takes ~30 seconds (cold start)
- Subsequent requests faster
- Model fits in free tier memory
- Requests limited to 100/min - more than enough for testing

### If You Hit Limits:
- Upgrade to paid tier ($7/month)
- Or use different platform
- Or optimize model size (unlikely needed)

---

## Keeping App Running

### Render.com
- Free tier: App sleeps after 15 min inactivity
- Wake it: Visit URL again
- Paid tier: Always on (~$7/month)

### PythonAnywhere
- Free tier: 100 CPU seconds/day
- Paid tier: More CPU time

### Streamlit Cloud
- Free tier: Always on (limited)
- Paid tier: More resources

---

## Success Indicators

Your deployment is successful when:
✅ You can visit your live URL
✅ Form displays correctly
✅ You can enter values
✅ Prediction returns a price
✅ /health endpoint shows model loaded
✅ No console errors

---

## After Successful Deployment

1. **Update GitHub README** (Optional)
   - Add live URL link
   - Add screenshot of deployed app
   
2. **Save deployment URL**
   - Keep in HousePrice_hosted_webGUI_link.txt
   
3. **Test one more time before submission**
   - Make prediction on live app
   - Verify everything works
   
4. **Submit to Scorac**
   - Deadline: Friday 11:59 PM

---

**Your deployment is production-ready! Choose Render.com for easiest experience.**
