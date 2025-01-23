from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, session
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

app = Flask(__name__)

# Load your trained model
model_path = 'CNN1_trained_model.keras'
model = load_model(model_path)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Function to preprocess the image
def preprocess_image(image_path, target_size):
    image = load_img(image_path, target_size=target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    return image

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('index.html')

@app.route('/background.jpg')
def background_image():
    # Serve the background image from static directory
    return send_from_directory(os.path.join(app.root_path, 'static'), 'background.jpg')

@app.route('/styles.css')
def styles():
    # Serve the styles.css from static directory
    return send_from_directory(os.path.join(app.root_path, 'static'), 'styles.css')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform login logic here (you can integrate user authentication)
        username = request.form['username']
        password = request.form['password']
        
        # Sample check (you can replace this with actual authentication logic)
        if username == 'admin' and password == 'admin':
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            return jsonify({"message": "Invalid credentials!"}), 401  # Send error if login fails

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear session
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the uploaded file
    file_path = 'temp.jpg'
    file.save(file_path)

    # Preprocess the image
    image = preprocess_image(file_path, target_size=(128, 128))

    # Make predictions
    predictions = model.predict(image)
    predicted_class = np.argmax(predictions, axis=1)[0]

    # Labels, precautions, causes, and recommendations
    labels = {
        0: "Acne", 1: "Actinic_Keratosis", 2: "Atopic Dermatitis", 3: "Basal Cell", 4: "Benign Keratosis",
        5: "Benign_tumors", 6: "Bullous", 7: "Candidiasis", 8: "Chickenpox", 9: "Melonoma", 10: "Eczema",
        11: "Infestations_Bites", 12: "Lichen", 13: "Lupus", 14: "Measles", 15: "Melanocytic", 16: "Melanoma",
        17: "Moles", 18: "Monkeypox", 19: "Normal", 20: "Psoriasis", 21: "Rosacea", 22: "Seborrh_Keratoses",
        23: "Seborrheic", 24: "SkinCancer", 25: "Sun_Sunlight_Damage", 26: "Tinea", 27: "Tinea Ringworms Candidiasis",
        28: "Unknown_Normal", 29: "Vascular_Tumors", 30: "Vasculitis", 31: "Vitiligo", 32: "Warts", 33: "Warts Molluscum"
    }

    precautions = {
        "Acne": "Keep your skin clean, avoid oily products, and consult a dermatologist for medications if necessary.",
        "Actinic_Keratosis": "Avoid excessive sun exposure, use sunscreen, and schedule regular dermatological checkups.",
        "Atopic Dermatitis": "Moisturize frequently, avoid allergens, and use prescribed creams or ointments.",
        "Basal Cell": "Protect your skin from UV radiation and consult a dermatologist for treatment options.",
        "Benign Keratosis": "Avoid irritants and protect the affected area from trauma.",
        "Benign_tumors": "Consult a specialist to monitor any changes in size or appearance.",
        "Bullous": "Keep the affected area clean and seek medical advice for proper treatment.",
        "Candidiasis": "Maintain proper hygiene, keep the skin dry, and use antifungal treatments as recommended.",
        "Chickenpox": "Avoid scratching, use soothing creams, and consult a doctor if symptoms worsen.",
        "Melonoma": "Avoid sun exposure, perform regular self-exams, and consult an oncologist immediately if suspected.",
        "Eczema": "Use moisturizing creams, avoid harsh soaps, and manage stress effectively.",
        "Infestations_Bites": "Use insect repellents, wash affected areas, and consult a doctor for severe reactions.",
        "Lichen": "Apply corticosteroid creams and avoid irritants that can worsen the condition.",
        "Lupus": "Avoid UV light exposure, manage stress, and follow prescribed medications.",
        "Measles": "Rest, stay hydrated, and consult a physician for antiviral treatments if necessary.",
        "Melanocytic": "Monitor moles for changes, use sunscreen, and consult a dermatologist.",
        "Melanoma": "Seek immediate medical attention and protect your skin from further UV damage.",
        "Moles": "Perform regular self-checks and consult a dermatologist for irregularities.",
        "Monkeypox": "Isolate, keep the affected area clean, and consult a healthcare provider.",
        "Normal": "Maintain a healthy skincare routine and avoid potential triggers.",
        "Psoriasis": "Keep your skin hydrated, avoid triggers like stress, and use medicated creams.",
        "Rosacea": "Avoid spicy foods, use gentle skincare products, and protect your skin from sun exposure.",
        "Seborrh_Keratoses": "Protect your skin and consult a doctor if irritation occurs.",
        "Seborrheic": "Use medicated shampoos and consult a dermatologist for persistent symptoms.",
        "SkinCancer": "Perform self-checks, avoid UV exposure, and consult a dermatologist regularly.",
        "Sun_Sunlight_Damage": "Apply sunscreen, wear protective clothing, and limit sun exposure.",
        "Tinea": "Keep affected areas dry and clean, and use antifungal medications.",
        "Tinea Ringworms Candidiasis": "Avoid sharing personal items and use antifungal treatments as needed.",
        "Unknown_Normal": "Monitor any changes and follow a healthy skincare routine.",
        "Vascular_Tumors": "Consult a specialist for monitoring and possible treatments.",
        "Vasculitis": "Follow prescribed medications and avoid potential triggers.",
        "Vitiligo": "Protect depigmented areas from the sun and consult a dermatologist for treatments.",
        "Warts": "Avoid picking warts, keep the area clean, and use topical treatments.",
        "Warts Molluscum": "Consult a healthcare provider for proper removal and management."
    }

    causes_and_recommendations = {
        "Acne": {"cause": "Clogged hair follicles due to excess oil, bacteria, and dead skin cells.", "recommendations": "Topical treatments (benzoyl peroxide, retinoids), oral antibiotics, hormonal treatments (for females)."},
        "Actinic_Keratosis": {"cause": "Sun damage to the skin, often from years of exposure to ultraviolet (UV) radiation.", "recommendations": "Cryotherapy, topical creams (5-fluorouracil), photodynamic therapy."},
        "Atopic Dermatitis": {"cause": "Genetic factors, environmental allergens, irritants, and immune system dysfunction.", "recommendations": "Moisturizers, corticosteroid creams, immunosuppressants, antihistamines."},
        "Basal Cell": {"cause": "Prolonged sun exposure, leading to UV-induced damage in the basal cells of the skin.", "recommendations": "Surgical removal, cryotherapy, topical treatments (imiquimod)."},
        "Benign Keratosis": {"cause": "Age, sun exposure, and genetic factors.", "recommendations": "Cryotherapy, laser therapy, or surgical removal if necessary."},
        "Benign_tumors": {"cause": "Genetic predisposition, environmental factors.", "recommendations": "Monitoring, surgical excision if they grow or cause discomfort."},
        "Bullous": {"cause": "Autoimmune conditions, skin disorders like pemphigus vulgaris, or allergic reactions.", "recommendations": "Corticosteroids, immunosuppressive drugs, and wound care."},
        "Candidiasis": {"cause": "Fungal infections caused by Candida species, typically due to moisture and warmth.", "recommendations": "Antifungal creams, oral antifungals (fluconazole)."},
        "Chickenpox": {"cause": "Varicella-zoster virus infection.", "recommendations": "Antiviral drugs (acyclovir), calamine lotion, and antihistamines for itching."},
        "Melonoma": {"cause": "Excessive sun exposure, genetic factors, and fair skin.", "recommendations": "Surgical removal, immunotherapy, targeted therapy, radiation."}
    }

    # Get the predicted label
    predicted_label = labels.get(predicted_class, "Unknown")
    precaution = precautions.get(predicted_label, "No specific precautions available.")
    cause = causes_and_recommendations.get(predicted_label, {}).get("cause", "Unknown cause")
    recommendations = causes_and_recommendations.get(predicted_label, {}).get("recommendations", "No specific recommendations available.")

    # Return the result as JSON
    return jsonify({
        'predicted_class': predicted_label,
        'precautions': precaution,
        'cause': cause,
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
