# Universal-Query-Translator
Universal Query Translator looks to close the gap between non-technical users and technical skills by employing LLM models, ensuring ease of access and making database management a breeze.

## Setup with vLLM

This project uses vLLM to serve the Unsloth Llama 3.1 3B model locally, providing an OpenAI-compatible API endpoint.

### Prerequisites
- NVIDIA GPU with CUDA support (RTX 5070 Ti 12GB VRAM recommended)
- Python 3.8+

### Installation

1. Install dependencies:
```bash
pip install -r src/requirements.txt
```

2. Start the vLLM server:
```bash
python start_vllm_server.py
```

Or manually:
```bash
python -m vllm.entrypoints.openai.api_server \
    --model unsloth/Llama-3.1-3B-Instruct-bnb-4bit \
    --host 0.0.0.0 \
    --port 8000 \
    --gpu-memory-utilization 0.9 \
    --trust-remote-code
```

### Configuration

Set environment variables (optional, defaults shown):
- `VLLM_BASE_URL`: vLLM server URL (default: `http://localhost:8000/v1`)
- `VLLM_MODEL_NAME`: Model name (default: `unsloth/Llama-3.1-3B-Instruct-bnb-4bit`)

Create a `.env` file in the project root:
```
VLLM_BASE_URL=http://localhost:8000/v1
VLLM_MODEL_NAME=unsloth/Llama-3.1-3B-Instruct-bnb-4bit
```

### Running the Application

1. Start the vLLM server (in one terminal):
```bash
python start_vllm_server.py
```

2. Start the Flask application (in another terminal):
```bash
python src/main.py
```

The API will be available at `http://localhost:5000/api/`