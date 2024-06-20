import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
import numpy as np
import csv
import random
import json
from http import HTTPStatus
import tensorflow as tf
from flask import Flask, jsonify, request
from google.cloud import storage
from dotenv import load_dotenv
from ...config import model_config as mconfig
from ...config import main_config as config
from .LLMController import getPromptLocally
from google.oauth2 import service_account

load_dotenv()


class StuntingController:
    bucket_name = os.environ.get('BUCKET_NAME','stuntshield-data-prediction')
    credentials_json = os.environ.get('CREDENTIALS')

    credentials_dict = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    client = storage.Client(credentials=credentials)
    bucket = storage.Bucket(client,bucket_name)

    model_stunting = tf.keras.models.load_model(
        mconfig['MODEL_CLASSIFICATION_STUNTING'], compile=False
    )
    model_weight = tf.keras.models.load_model(
        mconfig['MODEL_CLASSIFICATION_WEIGHT'], compile=False
    )
    model_ideal_024 = tf.keras.models.load_model(
        mconfig['MODEL_CLASSIFICATION_IDEAL_024'], compile=False
    )
    model_ideal_2460 = tf.keras.models.load_model(
        mconfig['MODEL_CLASSIFICATION_IDEAL_2460'], compile=False
    )
    classes_stunting = ['Stunting Berat', 'Stunting', 'Normal', 'Tinggi']
    classes_weight = [
        'Berat Badan Sangat Kurang',
        'Berat Badan Kurang',
        'Berat Badan Normal',
        'Risiko Berat Badan Lebih',
    ]
    classes_ideal = [
        'Gizi Buruk',
        'Gizi Kurang',
        'Gizi Baik (Normal)',
        'Berisiko Gizi Lebih (Overweight)',
        'Gizi Lebih (overweight)',
        'Obesitas',
    ]

    def index():
        return (
            jsonify(
                {
                    'status': {
                        'code': HTTPStatus.OK,
                        'message': 'nyambung cuy santui',
                    },
                    'data': None,
                }
            ),
            HTTPStatus.OK,
        )

    def upload_data(fieldnames,data,csv_file,path):
        file_csv = csv_file
        file_path = os.path.join(path,file_csv)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)
        blob = StuntingController.bucket.blob(path+'/'+file_csv+str(random.randint(10000,99999)) )
        blob.upload_from_filename(file_path)
        os.remove(file_path)

    def predict_stunting():
        if request.method == 'POST':
            year = float(request.form['year'])
            month = float(request.form['month'])
            day = float(request.form['day'])
            jenis_kelamin = request.form['jenis_kelamin']
            tinggi_badan = float(request.form['tinggi_badan'])
            berat_badan = float(request.form['berat_badan'])
            if (
                year is not None
                and month is not None
                and day is not None
                and jenis_kelamin is not None
                and tinggi_badan is not None
                and berat_badan is not None
            ):
                umur = ((year * 12) + month) + (day / 30)
                jenis_kelamin_map = {'laki-laki': 0, 'perempuan': 1}
                jenis_kelamin_num = jenis_kelamin_map[jenis_kelamin]
                fieldstunting = [
                    'Umur (bulan)',
                    'Jenis Kelamin',
                    'Tinggi Badan (cm)',
                    'Status Gizi',
                ]
                fieldideal = [
                    'Jenis Kelamin',
                    'Tinggi Badan (cm)',
                    'Berat Badan (kg)',
                    'Status',
                ]
                fieldweight = [
                    'Umur (bulan)',
                    'Jenis Kelamin',
                    'Berat Badan (kg)',
                    'Status',
                ]

                input_data_stunting_predict = pd.DataFrame(
                    {
                        'Umur': [umur],
                        'Jenis Kelamin': [jenis_kelamin_num],
                        'Tinggi Badan': [tinggi_badan],
                    }
                )
                prediction_stunting_result = (
                    StuntingController.model_stunting.predict(
                        input_data_stunting_predict
                    )
                )

                input_data_weight_predict = pd.DataFrame(
                    {
                        'Umur': [umur],
                        'Jenis Kelamin': [jenis_kelamin_num],
                        'Berat Badan': [berat_badan],
                    }
                )
                prediction_weight_result = (
                    StuntingController.model_weight.predict(
                        input_data_weight_predict
                    )
                )

                data_stunting = {
                    'Umur (bulan)': umur,
                    'Jenis Kelamin': jenis_kelamin,
                    'Tinggi Badan (cm)': tinggi_badan,
                    'Status Gizi': StuntingController.classes_stunting[
                        np.argmax(prediction_stunting_result)
                    ],
                }
                StuntingController.upload_data(fieldstunting,data_stunting,'inputan_stunting.csv',config['UPLOAD_FOLDER_STUNTING'])

                data_weight = {
                    'Umur (bulan)': umur,
                    'Jenis Kelamin': jenis_kelamin,
                    'Berat Badan (kg)': berat_badan,
                    'Status': StuntingController.classes_weight[
                        np.argmax(prediction_weight_result)
                    ],
                }
                StuntingController.upload_data(fieldweight,data_weight,'inputan_weight.csv',config['UPLOAD_FOLDER_WEIGHT'])

                if umur <= 24:
                    input_data_ideal_024_predict = pd.DataFrame(
                        {
                            'Jenis Kelamin': [jenis_kelamin_num],
                            'Tinggi Badan': [tinggi_badan],
                            'Berat Badan': [berat_badan],
                        }
                    )
                    prediction_ideal_result = (
                        StuntingController.model_ideal_024.predict(
                            input_data_ideal_024_predict
                        )
                    )
                    data_ideal = {
                        'Jenis Kelamin': jenis_kelamin,
                        'Tinggi Badan (cm)': tinggi_badan,
                        'Berat Badan (kg)': berat_badan,
                        'Status': StuntingController.classes_ideal[
                            np.argmax(prediction_ideal_result)
                        ],
                    }
                    StuntingController.upload_data(fieldideal,data_ideal,'inputan_ideal_024.csv',config['UPLOAD_FOLDER_IDEAL_024'])
                else:
                    input_data_ideal_2460_predict = pd.DataFrame(
                        {
                            'Jenis Kelamin': [jenis_kelamin_num],
                            'Tinggi Badan': [tinggi_badan],
                            'Berat Badan': [berat_badan],
                        }
                    )
                    prediction_ideal_result = (
                        StuntingController.model_ideal_2460.predict(
                            input_data_ideal_2460_predict
                        )
                    )
                    data_ideal = {
                        'Jenis Kelamin': jenis_kelamin,
                        'Tinggi Badan (cm)': tinggi_badan,
                        'Berat Badan (kg)': berat_badan,
                        'Status': StuntingController.classes_ideal[
                            np.argmax(prediction_ideal_result)
                        ],
                    }
                    StuntingController.upload_data(fieldideal,data_ideal,'inputan_ideal_2460.csv',config['UPLOAD_FOLDER_IDEAL_2460'])

                result_prediction_stunting = {
                    'class': StuntingController.classes_stunting[
                        np.argmax(prediction_stunting_result)
                    ],
                    'presentase': str(
                        '{:.1f}'.format(
                            np.max(prediction_stunting_result) * 100
                        )
                    ),
                }
                result_prediction_weight = {
                    'class': StuntingController.classes_weight[
                        np.argmax(prediction_weight_result)
                    ],
                    'presentase': str(
                        '{:.1f}'.format(np.max(prediction_weight_result) * 100)
                    ),
                }
                result_prediction_ideal = {
                    'class': StuntingController.classes_ideal[
                        np.argmax(prediction_ideal_result)
                    ],
                    'presentase': str(
                        '{:.1f}'.format(np.max(prediction_ideal_result) * 100)
                    ),
                }

                result_str = 'prediksi tinggi badan bersarkan usianya :{},prediksi berat badan berdasarkan usianya {},prediksi ideal berat badan berdasarkan tingginya : {}'.format(
                    StuntingController.classes_stunting[np.argmax(prediction_stunting_result)],
                    StuntingController.classes_weight[np.argmax(prediction_weight_result)],
                    StuntingController.classes_ideal[np.argmax(prediction_ideal_result)]
                )
                umur_str = "{} Tahun {} bulan".format(year,month)
                result_all = {
                    'stunting': result_prediction_stunting,
                    'weight': result_prediction_weight,
                    'ideal': result_prediction_ideal,
                    'recommendation': getPromptLocally(
                        tinggi_badan,
                        umur_str,
                        result_str,
                        berat_badan,
                        jenis_kelamin,
                    ),
                }
                return (
                    jsonify(
                        {
                            'status': {
                                'code': HTTPStatus.OK,
                                'message': 'Success predicting',
                            },
                            'data': result_all,
                        }
                    ),
                    HTTPStatus.OK,
                )
            else:
                return (
                    jsonify(
                        {
                            'status': {
                                'code': HTTPStatus.BAD_REQUEST,
                                'message': 'Client side error',
                            },
                            'data': None,
                        }
                    ),
                    HTTPStatus.BAD_REQUEST,
                )
        else:
            return (
                jsonify(
                    {
                        'status': {
                            'code': HTTPStatus.METHOD_NOT_ALLOWED,
                            'message': 'Method not allowed',
                        },
                        'data': None,
                    }
                ),
                HTTPStatus.METHOD_NOT_ALLOWED,
            )