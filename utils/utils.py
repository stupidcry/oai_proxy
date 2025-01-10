import logging
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage

message_context = []
def generate_message(userMessage):
    global message_context
    messages = [
    SystemMessage("你是智能助手，回答用户的消息不超过200字，不要有换行。"),
    ]
    message_context.append(HumanMessage(userMessage))
    messages += message_context
    message_context = message_context[-12:]
    logging.info(f'context: {message_context}')
    return messages