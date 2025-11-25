import os
import json
import joblib
import random
from datetime import datetime
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for, session


DEMO_MODE = True
DEMO_PROB_THRESHOLD = 0.70

TEMPLATES_DIR = os.path.join(os.getcwd(), "templates")
STATIC_DIR = os.path.join(os.getcwd(), "static")

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)

print("Flask templates folder:", os.path.abspath(TEMPLATES_DIR))
print("Flask static folder   :", os.path.abspath(STATIC_DIR))

app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-me")

PIPE = "fraud_pipeline.pkl"
META = "model_metadata.json"
LOG_FILE = "demo_case_logs.csv"

FLAG_PROB = 0.01

pipeline = None
best_threshold = 0.5
meta = {}

try:
    pipeline = joblib.load(PIPE)
    print(f"Loaded pipeline from {PIPE}")
except Exception as e:
    print("Could not load pipeline:", e)
    pipeline = None

try:
    if os.path.exists(META):
        with open(META) as f:
            meta = json.load(f)
            best_threshold = float(meta.get("best_threshold", meta.get("chosen_threshold", 0.5)))
            print(f"Loaded metadata threshold: {best_threshold}")
    else:
        print(f"Metadata file {META} not found — using defaults.")
except Exception as e:
    print("Could not load metadata:", e)
    meta = {}

try:
    if best_threshold > 1:
        best_threshold = float(best_threshold) / 100.0
except Exception:
    best_threshold = float(best_threshold)

print("Effective best_threshold (0..1):", best_threshold)

DEFAULT_SIM_START = "2017-01-01 00:00:00"
sim_start_str = meta.get("simulation_start", DEFAULT_SIM_START)
try:
    sim_start_dt = datetime.fromisoformat(sim_start_str)
except Exception:
    try:
        sim_start_dt = datetime.strptime(sim_start_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        sim_start_dt = datetime.fromisoformat(DEFAULT_SIM_START)

def compute_step_from_datetime(dt_selected, sim_start=sim_start_dt):
    delta = dt_selected - sim_start
    delta_seconds = delta.total_seconds()
    if delta_seconds < 0:
        return None
    step = int(delta_seconds // 3600) + 1
    return step

def risk_label(prob, threshold):
    if prob >= threshold:
        return "HIGH", "risk-high"
    elif prob >= threshold * 0.5:
        return "MEDIUM", "risk-medium"
    else:
        return "LOW", "risk-low"

_now = datetime.now()

defaults = {
    'date': _now.date().isoformat(),             
    'time': _now.time().strftime("%H:%M"),       
    'type': 'PAYMENT',
    'amount': 1000.0,
    'oldbalanceOrg': 5000.0,
    'newbalanceOrig': 4000.0,
    'oldbalanceDest': 0.0,
    'newbalanceDest': 4000.0,
    'origin_account': '',
    'destination_account': ''
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date_str = request.form.get('date', defaults['date'])
        time_str = request.form.get('time', defaults['time'])
        tx_type = request.form.get('type', defaults['type'])
        origin_account = request.form.get('origin_account', defaults['origin_account'])
        destination_account = request.form.get('destination_account', defaults['destination_account'])

        try:
            amount = float(request.form.get('amount', defaults['amount']))
            oldbalanceOrg = float(request.form.get('oldbalanceOrg', defaults['oldbalanceOrg']))
            newbalanceOrig = float(request.form.get('newbalanceOrig', defaults['newbalanceOrig']))
            oldbalanceDest = float(request.form.get('oldbalanceDest', defaults['oldbalanceDest']))
            newbalanceDest = float(request.form.get('newbalanceDest', defaults['newbalanceDest']))
        except Exception as e:
            flash(f"Invalid numeric input: {e}", "danger")
            return redirect(url_for('index'))

        try:
            sel_dt = datetime.fromisoformat(f"{date_str}T{time_str}")
        except Exception:
            try:
                sel_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            except Exception as e:
                flash(f"Invalid date/time: {e}", "danger")
                return redirect(url_for('index'))

        step_val = compute_step_from_datetime(sel_dt)
        if step_val is None:
            flash("Selected datetime is before simulation start. Choose a datetime >= simulation start.", "danger")
            return redirect(url_for('index'))

        isFlaggedFraud = 1 if random.random() < FLAG_PROB else 0

        try:
            amt = float(amount)

            if amt >= 100000:
                isFlaggedFraud = 1
            if float(newbalanceOrig) == 0:
                isFlaggedFraud = 1
            if float(oldbalanceDest) == 0 and amt > 50000:
                isFlaggedFraud = 1
        except Exception:
            pass

        input_for_model = {
            'step': int(step_val),
            'type': tx_type,
            'amount': float(amount),
            'oldbalanceOrg': float(oldbalanceOrg),
            'newbalanceOrig': float(newbalanceOrig),
            'oldbalanceDest': float(oldbalanceDest),
            'newbalanceDest': float(newbalanceDest),
            'isFlaggedFraud': int(isFlaggedFraud)
        }
        X = pd.DataFrame([input_for_model])

        if pipeline is None:
            flash("Model pipeline not loaded. Place fraud_pipeline.pkl in the app folder.", "danger")
            return redirect(url_for('index'))

        try:
            prob = float(pipeline.predict_proba(X)[0,1])
        except Exception as e:
            flash(f"Prediction failed: {e}", "danger")
            return redirect(url_for('index'))

        pct = prob * 100.0

        if DEMO_MODE:
            if int(isFlaggedFraud) == 1:
                label_text, label_class = "HIGH", "risk-high"
            elif prob >= DEMO_PROB_THRESHOLD:
                label_text, label_class = "HIGH", "risk-high"
            else:
                label_text, label_class = risk_label(prob, best_threshold)
        else:
            label_text, label_class = risk_label(prob, best_threshold)

        result = {
            'input': {
                'origin_account': origin_account,
                'destination_account': destination_account,
                'type': tx_type,
                'amount': amount,
                'oldbalanceOrg': oldbalanceOrg,
                'newbalanceOrig': newbalanceOrig,
                'oldbalanceDest': oldbalanceDest,
                'newbalanceDest': newbalanceDest
            },
            'selected_datetime': sel_dt.isoformat(),
            'internal': {
                'step': int(step_val),
                'isFlaggedFraud': int(isFlaggedFraud)
            },
            'prob': prob,
            'pct': pct,
            'label_text': label_text,
            'label_class': label_class,
            'threshold': best_threshold
        }

        session['last_result'] = result

        log_row = pd.DataFrame([{
            **input_for_model,
            'origin_account': origin_account,
            'destination_account': destination_account,
            'probability': pct,
            'label': label_text,
            'ts': datetime.utcnow().isoformat()
        }])
        header = not Path(LOG_FILE).exists()
        try:
            log_row.to_csv(LOG_FILE, mode='a', header=header, index=False)
        except Exception as e:
            print("Failed to save log:", e)

        return redirect(url_for('result'))

    return render_template("index.html", defaults=defaults, best_threshold=best_threshold, meta=meta)

@app.route("/result", methods=["GET"])
def result():
    res = session.get('last_result')
    if not res:
        flash("No recent prediction to show. Please submit the form first.", "info")
        return redirect(url_for('index'))
    return render_template("result.html", res=res, meta=meta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
