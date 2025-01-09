import os
import logging
from flask import Flask, request, jsonify, send_file
import requests
from scipy.io import wavfile
from pydub import AudioSegment
import io
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.adapters.openai import convert_message_to_dict
import httpx
import openai
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
httpx_client = httpx.Client(http2=True, verify=False)

model = ChatOpenAI(model="gpt-4o-mini",
                   base_url="https://api.gptsapi.net/v1",
                   api_key="sk-P1Jb666dd36a9b7f398c6c6133e8bf868e82ee21890jjWsJ",
                   http_client=httpx_client)

oai_client = model.root_client
# openai.audio.speech.create

# 加载环境变量
# load_dotenv()
# 获取OpenAI API密钥
# openai_api_key = os.getenv("OPENAI_API_KEY")
# print(openai_api_key)
# 初始化Flask应用

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

def wantEndChat(userMessage):
    messages = [
    SystemMessage("请通过以下用户的消息判断用户是否想结束聊天。用户想结束聊天输出yes，不想结束聊天输出no。不要有任何其它输出。"),
    HumanMessage(userMessage),
    ]
    openai_response = model.invoke(messages)
    logging.info(f'end chat?: {openai_response.content}')
    return openai_response.content


@app.route("/chat",methods=['POST'])
def chat():
    data = request.get_json()
    logging.info(f'data: {data}')
    userMessage = data.get("message")
    
    messages = [
    SystemMessage("你是智能助手，回答用户的消息不超过200字，不要有换行。"),
    HumanMessage(userMessage),
    ]

    openai_response = model.invoke(messages)
    print(openai_response.content)
    print(openai_response.usage_metadata )
    if wantEndChat(userMessage)=="yes":
        return convert_message_to_dict(openai_response), 201
    return convert_message_to_dict(openai_response), 200

@app.route("/tts",methods=['POST'])
def tts():
    try:
        data = request.get_json()
        logging.info(f'data: {data}')
        text = data.get("text")
        response = oai_client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="wav"
        )
        # 将返回的音频数据写入内存
        audio_buffer = io.BytesIO()
        for chunk in response.iter_bytes(chunk_size=4096):
            audio_buffer.write(chunk)
        audio_buffer.seek(0)
        # 读取音频数据和采样率
        original_samplerate, audio_data = wavfile.read(audio_buffer)

        # 如果采样率不是 16000Hz，则进行重采样
        target_samplerate = 16000
        if original_samplerate != target_samplerate:
            duration = len(audio_data) / original_samplerate
            new_length = int(target_samplerate * duration)
            resampled_audio = np.interp(
                np.linspace(0, len(audio_data), new_length, endpoint=False),
                np.arange(len(audio_data)),
                audio_data
            )
            resampled_audio = resampled_audio.astype(audio_data.dtype)
        else:
            resampled_audio = audio_data

        # 将重采样后的音频数据写入内存文件
        buffer = io.BytesIO()
        wavfile.write(buffer, target_samplerate, resampled_audio)
        buffer.seek(0)

        # 返回音频文件给请求方
        return send_file(
            buffer,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="speech_16000Hz.wav"
        )
    except Exception as e:
        bomb_file_path = "bomb.wav"
        return send_file(
            bomb_file_path,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="bomb.wav"
        )

if __name__ == "__main__":
    #wantEndChat("你好啊")
    app.run(host="0.0.0.0", port=15000, debug=True)