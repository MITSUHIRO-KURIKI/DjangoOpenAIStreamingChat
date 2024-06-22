# Token
# GPT-4 turbo: 128000, GPT-4 32K: 32768, GPT-4 8K: 8192, GPT-3.5: 4096
MIN_TOKENS      = 50
MAX_TOKENS      = 2048
SEND_MAX_TOKENS = 8192

# Process
RETRY_LIMIT_N  = 2
MAX_HISSTORY_N = 30

# Models
MAX_LEN_SYSTEM_SENTENCE    = 1500
MAX_LEN_ASSISTANT_SENTENCE = 1500
DEFAULT_ROOM_NAME          = 'NewChatRoom'
MAX_LEN_ROOM_NAME          = 50

# Enbedding LLM
## Falseの場合には OpenAI Embedding を使用
IS_USE_EmbeddingVertexAi= True

# LLM回答の中に ALLOWD_DOMAINS_LIST 以外のURLドメインが含まれていた場合には削除してからDBに保存する
ALLOWD_DOMAINS_LIST = ['go.jp', 'or.jp', 'google.com',]