# import os
# from langchain_ollama import ChatOllama

# def build_ollama(model_name):
#     return ChatOllama(
#         model_name=model_name,
#         temperature=0.0,
#         base_url=os.environ["LOCAL_OLLAMA_URL"]
#     )