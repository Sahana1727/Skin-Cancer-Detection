import os
import numpy as np
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_USE_LEGACY_KERAS"] = "1"

app = Flask(__name__)

# Load model once
model = load_model("C:/Users/Sahana/Documents/Skin_Cancer/models/V2model.h5",compile=False)

# Class labels
class_names = [
    'Basal_cell_carcinoma',
    'Melanoma',
    'Nevus',
    'benign_keratosis',
    'no_cancer'
]

# Ensure upload folder exists
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Preprocess image
def preprocess(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    img_path = None
    results = None

    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename != '':
            # Secure filename
            filename = secure_filename(file.filename)

            # Save image
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)

            # Preprocess
            img = preprocess(img_path)

            # Predict
            preds = model.predict(img)[0]

            # Top 3 predictions
            top3_idx = preds.argsort()[-3:][::-1]
            results = [(class_names[i], round(preds[i] * 100, 2)) for i in top3_idx]

            # Best prediction
            prediction = results[0][0]
            confidence = results[0][1]

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        img_path=img_path,
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)docker run -p 5000:5000 shreyasbk2406/skin-cancer-app