import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.adapters.openai import convert_message_to_dict
import httpx

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
httpx_client = httpx.Client(http2=True, verify=False)

model = ChatOpenAI(model="gpt-4o-mini",
                   base_url="https://api.gptsapi.net/v1",
                   api_key="sk-P1Jb666dd36a9b7f398c6c6133e8bf868e82ee21890jjWsJ",
                   http_client=httpx_client)


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

@app.route("/chat",methods=['POST'])
def chat():
    data = request.get_json()
    logging.info(f'data: {data}')
    userMessage = data.get("message")

    messages = [
    SystemMessage("你是智能助手，回答用户的消息不拆过200字。"),
    HumanMessage(userMessage),
    ]

    openai_response = model.invoke(messages)
    print(openai_response.content)
    print(openai_response.usage_metadata )
    return convert_message_to_dict(openai_response), 200


@app.route("/tts",methods=['POST'])
def chat():
    data = request.get_json()
    logging.info(f'data: {data}')
    userMessage = data.get("message")

    messages = [
    SystemMessage("你是智能助手，回答用户的消息不拆过200字。"),
    HumanMessage(userMessage),
    ]

    openai_response = model.invoke(messages)
    print(openai_response.content)
    print(openai_response.usage_metadata )
    return convert_message_to_dict(openai_response), 200

if __name__ == "__main__":
    app.run()