import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from flask import jsonify, request
import requests
import json
from ...config import main_config as conf
from dotenv import load_dotenv

load_dotenv()

def getArticles():
    perPage = (
        int(request.args.get('perPage'))
        if request.args.get('perPage') is not None
        else 5
    )
    api_key = os.environ.get('SEARCH_ENGINE_KEY')
    se_id = conf['SEARCH_ENGINE_ID']
    s_query = 'Artikel Stunting'
    url = conf['SEARCH_ENGINE_URL']
    params = {
        'q': s_query,
        'key': api_key,
        'cx': se_id,
        'lr': 'lang_id',
        'gl': 'ID',
        'num': perPage,
        'filter': 0
        # 'searchType': 'link'
    }

    filtered_results = []
    while len(filtered_results) <= perPage:
        req = requests.get(url, params=params)
        resp = req.json()['items']
        for row in resp:
            if 'cse_thumbnail' in row['pagemap']:
                filtered_results.append(row)
    mapped_result = []
    for row in filtered_results[:perPage]:
        mapped_result.append(
            {
                'title': row['title'],
                'description': row['snippet'],
                'thumbnail': (
                    row['pagemap']['cse_thumbnail'][0]['src']
                    if 'cse_thumbnail' in row['pagemap']
                    else None
                ),
                'link': row['link'],
            }
        )
    mapped_result = sorted(mapped_result, key=lambda x: x['thumbnail'] is None)
    return jsonify({'results': mapped_result, 'message': 'OK'}), 200