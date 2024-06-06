import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
import numpy as np
import csv
import random
import json
from http import HTTPStatus
import tensorflow as tf
from flask import Flask, jsonify, request
from google.cloud import storage, secretmanager_v1 as secretmanager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Hint for anak CC: mungkin bsa di tambahin codingan buat masukin inputan user sama outputnya ke bucket buat data tambahan training model
app.config['UPLOAD_FOLDER'] = 'Users/uploads/'
app.config['MODEL_CLASSIFICATION'] = './model/stunting_prediction.h5'

# Set variabel lingkungan untuk Google Application Credentials
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath("./credentials/gcs.json")

# Fungsi untuk mengambil key dari Secret Manager
def get_secret(secret_name):
    project_id = "capstone-test-424803"  # ID proyek kamu
    secret_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    secret_client = secretmanager.SecretManagerServiceClient()
    response = secret_client.access_secret_version(request={"name": secret_name})
    return json.loads(response.payload.data.decode("UTF-8"))

# Mengambil key dari Secret Manager
gcs_credentials = get_secret('gcs-key')

model = tf.keras.models.load_model(app.config['MODEL_CLASSIFICATION'],compile=False)

client = storage.Client.from_service_account_info(gcs_credentials)
bucket_name = os.environ.get('BUCKET_NAME','capstonecicd-bucket')
bucket = storage.Bucket(client,bucket_name)

classes = ["Stunting Berat","Stunting","Normal","Tinggi"] 

@app.route("/")
def index():
    return jsonify({
        "status" : {
            "code" : HTTPStatus.OK,
            "message" : "nyambung cuy santui...",
        },
        "data" : None
    }),HTTPStatus.OK
@app.route("/prediction",methods=["POST"])   
def predict_stunting():
    if request.method == "POST":
        year = float(request.form["year"])
        month = float(request.form["month"])
        day = float(request.form["day"])
        jenis_kelamin = request.form["jenis_kelamin"]
        tinggi_badan = float(request.form["tinggi_badan"])
        if year is not None and month is not None and day is not None and jenis_kelamin is not None and tinggi_badan is not None:
            umur = ((year*12) + month) + (day/30)
            jenis_kelamin_map = {'laki-laki': 0, 'perempuan': 1}
            jenis_kelamin_num = jenis_kelamin_map[jenis_kelamin]
            
            input_data = pd.DataFrame({'Umur': [umur], 'Jenis Kelamin': [jenis_kelamin_num], 'Tinggi Badan': [tinggi_badan]})
            prediction_result = model.predict(input_data)

            result = {
                'class' : classes[np.argmax(prediction_result)],
                'presentase' : str("{:.1f}".format(np.max(prediction_result)*100))
            }
            
            data = {
                "Umur (bulan)" : umur,
                "Jenis Kelamin" : jenis_kelamin,
                "Tinggi Badan (cm)" : tinggi_badan,
                "Status Gizi" : classes[np.argmax(prediction_result)]
            }
            file_csv = "inputan_user.csv"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],file_csv)
            with open(file_path, mode='w', newline='') as file:
                fieldnames = ["Umur (bulan)", "Jenis Kelamin", "Tinggi Badan (cm)","Status Gizi"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(data)
            blob = bucket.blob('Users_input/'+file_csv+str(random.randint(10000,99999)) )
            blob.upload_from_filename(file_path)
            os.remove(file_path)
            return jsonify({
                "status" : {
                    "code" : HTTPStatus.OK,
                    "message" : "Success predicting",
                },
                "data" : result,
            }),HTTPStatus.OK
        else :
            return jsonify({
                "status" : {
                    "code" : HTTPStatus.BAD_REQUEST,
                    "message": "Client side error"
                },
                "data": None
            }),HTTPStatus.BAD_REQUEST
    else:
        return jsonify({
            "status" : {
                "code": HTTPStatus.METHOD_NOT_ALLOWED,
                "message" : "Method not allowed",
            },
            "data": None,
        }),HTTPStatus.METHOD_NOT_ALLOWED
        

if __name__ == "__main__":
    # app.run()
    # Gunakan PORT dari variabel lingkungan
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)