import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from flask import jsonify
import json
from openai import OpenAI, AssistantEventHandler
from ...config import main_config
from dotenv import load_dotenv

load_dotenv()

def getPrompt():
    tinggi_badan = 97.5
    usia = 24
    status = 'stunted,overweight'
    berat_badan = 65
    jenis_kelamin = 'laki-laki'
    messages = getPromptLocally(
        tinggi_badan, usia, status, berat_badan, jenis_kelamin
    )
    return jsonify({'success': 'OK', 'message': str(messages)}), 200


def getPromptLocally(tinggi_badan, usia, status, berat_badan, jenis_kelamin):
    env_openai = os.environ.get('OPENAI_KEY')
    client = OpenAI(api_key=env_openai)
    # Create a new thread
    thread = client.beta.threads.create()
    input_message = 'tinggi badan: {}, usia: {} tahun, status_gizi:{}, berat badan:{}, jenis kelamin:{}'.format(
        tinggi_badan, usia / 12, status, berat_badan, jenis_kelamin
    )

    message = client.beta.threads.messages.create(
        thread_id=thread.id, role='user', content=input_message
    )

    # Define the instructions for the assistant
    instructions = 'Berikan rekomendasi makanan anak - anak berdasarkan input. tampilkan berupa list dan juga berikan rekomendasi penanganannya'
    assistant_id = 'asst_BZ2loRreVsga2g26VYYrSWAi'

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions=instructions,
    )

    messages = 'gagal membuat rekomendasi.'
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        messages = messages.data[0].content[0].text.value

    return str(messages)