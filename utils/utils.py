import logging
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage

message_context = []

def generate_message(userMessage):
    global message_context
    messages = [
    SystemMessage("你是智能语音助手，回答用户的消息不超过200字;可以适当多加些语气词和停顿，不要有换行，不要有emoji"),
    ]
    message_context.append(HumanMessage(userMessage))
    messages += message_context
    message_context = message_context[-12:]
    logging.info(f'all message: {messages}')
    return messages

def add_context_message(userMessage):
    global message_context
    message_context.append(AIMessage(userMessage))
    message_context = message_context[-12:]
    logging.info(f'context: {message_context}')
    return message_context