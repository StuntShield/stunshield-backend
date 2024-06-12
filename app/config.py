main_config = {
    'DEBUG': True,
    'BASE_URL': 'http://localhost',
    'PORT': '5000',
    'UPLOAD_FOLDER_STUNTING': 'app/assets/users_uploads/data_stunting',
    'UPLOAD_FOLDER_WEIGHT': 'app/assets/users_uploads/data_weight',
    'UPLOAD_FOLDER_IDEAL_024': 'app/assets/users_uploads/data_ideal/umur_0_24_bulan',
    'UPLOAD_FOLDER_IDEAL_2460': 'app/assets/users_uploads/data_ideal/umur_24_60_bulan',
    'SEARCH_ENGINE_URL': 'https://www.googleapis.com/customsearch/v1',
    'SEARCH_ENGINE_ID': 'c37f4842282914b17',
    # 'SEARCH_ENGINE_KEY': '',
    # 'OPENAI_KEY': ,
    # 'GCS_CREDENTIALS': '',
    # 'GCP_CREDIT': ''
}

model_config = {
    'MODEL_CLASSIFICATION_STUNTING': 'app/assets/ml_models/stunting_prediction.h5',
    'MODEL_CLASSIFICATION_WEIGHT': 'app/assets/ml_models/weight_prediction.h5',
    'MODEL_CLASSIFICATION_IDEAL_024': 'app/assets/ml_models/ideal_prediction_024.h5',
    'MODEL_CLASSIFICATION_IDEAL_2460': 'app/assets/ml_models/ideal_prediction_2460.h5',
    # 'OPENAI_API_KEY': ''
}