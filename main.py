import pickle
import pandas as pd
import random
from flask import session
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static')
app.secret_key = "sri_vasavi_engineering_college"
model = pickle.load(open('model1.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        snoring_rate = request.form.get('snoring rate')
        respiration_rate = request.form.get('respiration rate')
        body_temperature = request.form.get('body temperature')
        limb_movement = request.form.get('limb movement')
        blood_oxygen = request.form.get('blood oxygen')
        eye_movement = request.form.get('eye movement')
        sleeping_hours = request.form.get('sleeping hours')
        heart_rate = request.form.get('heart rate')

        new_data = pd.DataFrame([[snoring_rate, respiration_rate, body_temperature, limb_movement, blood_oxygen, 
                                  eye_movement, sleeping_hours, heart_rate]],
                                columns=['snoring rate', 'respiration rate', 'body temperature', 'limb movement', 
                                         'blood oxygen', 'eye movement', 'sleeping hours', 'heart rate'])

        stress_level = model.predict(new_data)
        stress_level_labels = {
            0: "Minimal-[0]",
            1: "Low-[1]",
            2: "Medium-[2]",
            3: "High-[3]",
            4: "Extreme High-[4]"
        }
        Detecting_stress_label = stress_level_labels[stress_level[0]]

        # Define multiple health tips for each stress level
        health_tips = {
            0: [
                "Keep up the good work! Maintain a balanced diet and regular physical activity.",
                "You're doing great! Try adding mindfulness exercises to stay stress-free.",
                "Continue engaging in hobbies that relax you and promote mental well-being."
            ],
            1: [
                "Your stress is low, but it’s important to stay active. Consider a daily walk or light yoga.",
                "Incorporate deep breathing or meditation into your routine to stay relaxed.",
                "Keep stress low by maintaining a good work-life balance and practicing self-care."
            ],
            2: [
                "Moderate stress detected. Try managing it with regular exercise, such as jogging or cycling.",
                "Take breaks during work and practice mindfulness to reduce stress.",
                "Engage in relaxation techniques such as progressive muscle relaxation or nature walks."
            ],
            3: [
                "High stress levels detected. Consider talking to someone or journaling to manage your feelings.",
                "Incorporate relaxation methods like yoga or breathing exercises to calm your mind.",
                "Take time off for self-care and reduce time spent on screens and social media."
            ],
            4: [
                "Your stress is extremely high. It’s crucial to seek professional help and talk to a counselor.",
                "Practice mindfulness and consider guided meditation to help manage extreme stress.",
                "Prioritize mental health. Consider reducing workload or taking a mental health day."
            ]
        }

        # Randomly select a health tip based on the stress level
        tip = random.choice(health_tips[stress_level[0]])

        # Store the prediction result and random health tip in the session
        session['detected_stress'] = f"Detected stress level is {Detecting_stress_label}"
        session['health_tip'] = f" {tip}"
        # Redirect to the result page
        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    # Get the prediction result and tip from the session
    detected_stress = session.get('detected_stress')
    stress_tip=session.get('health_tip')

    # Render the result page with the prediction and health tips
    return render_template('out.html', detected_stress=detected_stress,stress_tip=stress_tip)

if __name__ == '__main__':
    app.run(debug=True)
