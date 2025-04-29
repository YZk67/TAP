import os

VICUNA_PATH = "D:/models/vicuna-13b-v1.5-gptq/" # ADD PATH
LLAMA_PATH = ".../project/Llama-2-7b-chat-hf" # ADD PATH

VICUNA_API_LINK = None # ADD LINK
LLAMA_API_LINK = "https://..." # ADD LINK
MIXTRAL_API_LINK = "https://api.deepinfra.com/v1/inference/mistralai/Mixtral-8x7B-Instruct-v0.1"
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

ATTACK_TEMP = 1
TARGET_TEMP = 0
ATTACK_TOP_P = 0.9
TARGET_TOP_P = 1

# Increase the above allow more streams in parallel
# Decrease it to reduce the memory requirement 
MAX_PARALLEL_STREAMS = 5
