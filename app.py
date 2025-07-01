from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load model, scaler, and features
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
feature_names = joblib.load('feature_names.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = {
        'Gender': request.form['Gender'],
        'Married': request.form['Married'],
        'Dependents': request.form['Dependents'],
        'Education': request.form['Education'],
        'Self_Employed': request.form['Self_Employed'],
        'ApplicantIncome': float(request.form['ApplicantIncome']),
        'CoapplicantIncome': float(request.form['CoapplicantIncome']),
        'LoanAmount': float(request.form['LoanAmount']),
        'Loan_Amount_Term': float(request.form['Loan_Amount_Term']),
        'Credit_History': float(request.form['Credit_History']),
        'Property_Area': request.form['Property_Area']
    }

    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)

    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_names]

    df_scaled = scaler.transform(df)
    prediction = model.predict(df_scaled)[0]
    result = "Eligible ✅" if prediction == 1 else "Not Eligible ❌"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
