#! /bin/bash

pip uninstall chromadb
pip install -U langchain-community
pip install langchain
pip install chromadb
pip install pypdf
pip install pytest
pip install boto3
pip install -U langchain-ollama
pip install -U langchain-chroma
# pip install -qU langchain-community faiss-cpu

curl https://ollama.ai/install.sh | sh

# chmod +x ollama_server/start_ollama_server.sh
# chmod +x ollama_server/pull_llms.sh

# ./ollama_server/start_ollama_server.sh
# ./ollama_server/pull_llms.sh