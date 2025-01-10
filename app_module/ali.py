from flask import Blueprint, request,send_file
import logging
from utils.utils import generate_message, message_context
import logging
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from langchain_community.adapters.openai import convert_message_to_dict
from langchain_openai import ChatOpenAI
import httpx
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
httpx_client = httpx.Client(http2=True, verify=False)

ali_model = ChatOpenAI(model="qwen-plus",
                   base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                   api_key="sk-644d3a0a557b420aa9389beba8b5d898",
                   http_client=httpx_client)


ali_module = Blueprint('ali_model', __name__)

def wantEndChat(userMessage):
    messages = [
    SystemMessage("请通过以下用户的消息判断用户是否想结束聊天。用户想结束聊天输出yes，不想结束聊天输出no。不要有任何其它输出。"),
    HumanMessage(userMessage),
    ]
    start_time = time.time()
    openai_response = ali_model.invoke(messages)
    logging.info(f'time:{start_time-time.time()} end chat?: {openai_response.content}')
    return openai_response.content

@ali_module.route("/chat",methods=['POST'])
def chat():
    data = request.get_json()
    logging.info(f'data: {data}')
    userMessage = data.get("message")
    
    messages = generate_message(userMessage)

    start_time = time.time()
    openai_response = ali_model.invoke(messages)
    logging.info(f'time:{time.time()-start_time} response: {openai_response.content}')
    message_context.append(AIMessage(openai_response.content))
    if wantEndChat(userMessage)=="yes":
        return convert_message_to_dict(openai_response), 201
    return convert_message_to_dict(openai_response), 200

