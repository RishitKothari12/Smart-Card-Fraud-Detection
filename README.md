# 🔐 Smart Card Fraud Detection  
Detecting fraudulent credit card transactions using an XGBoost-based machine learning pipeline with a Flask web application.

---

## 📌 Overview  
This project aims to identify fraudulent credit card transactions using a trained **XGBoost model** and a **preprocessing pipeline** built on a **synthetic transaction dataset from Kaggle**.  
A simple **Flask-based web interface** allows users to enter transaction details and instantly receive fraud predictions.

---

## 🚀 Features  
- ✔ XGBoost classifier for high-accuracy fraud detection  
- ✔ End-to-end preprocessing pipeline (`fraud_pipeline.pkl`)  
- ✔ Flask web app with clean UI (HTML templates + CSS + JS)  
- ✔ Input validation + formatted prediction results  
- ✔ Modular project structure  
- ✔ Ready for deployment on Render/Heroku/AWS  

---

## 📊 Dataset  
- **Source:** Synthetic Credit Card Fraud Dataset (Kaggle)  
- Dataset contains generated transaction behavior with labeled fraud cases.  
- Features include amount, category, user demographics, transaction mode, etc.  
- Cleaned, encoded, and scaled before training.

---

## 🤖 Model  
- **Algorithm:** XGBoost Classifier  
- **Why XGBoost?**  
  - Handles imbalanced datasets well  
  - Strong performance on tabular data  
  - Fast training + built-in regularization  

The model is bundled within the **fraud_pipeline.pkl** file, which includes preprocessing:
- Scaling  
- Encoding  
- Feature engineering  
- Model prediction  

---

## 🧱 Project Structure  
```plaintext
Smart_Card_Fraud_Detection/
│
├── app.py                     # Flask application
├── fraud_pipeline.pkl         # Trained model + preprocessing pipeline
├── model_metadata.json        # Model info (optional)
├── demo_case_logs.csv         # Sample logs
│
├── templates/
│   ├── index.html             # Home page
│   └── result.html            # Result page
│
├── static/
│   ├── style.css              # Frontend styles
│   └── script.js              # Frontend JS
│
├── Smart_Card_Fraud_Detection.ipynb # Notebook (training + analysis)
├── README.md
└── requirements.txt


```
## 🚀 How to Run

```
### 1️⃣ Clone the repository
```bash
git clone https://github.com/RishitKothari12/Smart-Card-Fraud-Detection.git
cd Smart-Card-Fraud-Detection
```


### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask app
```bash
python app.py
```

### 4️⃣ Open in browser
```
http://127.0.0.1:5000
```
