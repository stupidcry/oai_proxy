import getpass
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import httpx

httpx_client = httpx.Client(http2=True, verify=False)

model = ChatOpenAI(model="gpt-4o-mini",
                   base_url="https://api.gptsapi.net/v1",
                   api_key="sk-P1Jb666dd36a9b7f398c6c6133e8bf868e82ee21890jjWsJ",
                   http_client=httpx_client)



messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

openai_response = model.invoke(messages)
print(openai_response.content)
print(openai_response.usage_metadata )