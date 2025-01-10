import logging
from flask import Flask, request, jsonify, send_file, Blueprint
import requests
from scipy.io import wavfile
from pydub import AudioSegment
import io
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from langchain_community.adapters.openai import convert_message_to_dict
import httpx
import openai
import numpy as np
import os
from flask import Flask, send_file, request
import azure.cognitiveservices.speech as speechsdk
import io
import time
from app_module.azure import azure_module
from app_module.oai import oai_module
from app_module.ali import ali_module

app = Flask(__name__)

# 注册多个 Blueprint
app.register_blueprint(azure_module, url_prefix='/az')
app.register_blueprint(oai_module, url_prefix='/oai')
app.register_blueprint(ali_module, url_prefix='/ali')


if __name__ == "__main__":
    #wantEndChat("你好啊")
    app.run(host="0.0.0.0", port=15000, debug=True)