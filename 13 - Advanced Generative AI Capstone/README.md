# Chevrolet Helpdesk Assistant

## CHECKOUT THE APP HERE: https://huggingface.co/spaces/krax1337/advanced_gen_ai_2025

## TRELLO BOARD: https://trello.com/b/Y71prDqG/advancedgenai2025

## How to run it?

```bash
docker run -it -p 7860:7860 --platform=linux/amd64 \
	-e TRELLO_API_KEY="YOUR_VALUE_HERE" \
	-e TRELLO_TOKEN="YOUR_VALUE_HERE" \
	-e TRELLO_LIST_ID="YOUR_VALUE_HERE" \
	-e OPENAI_API_KEY="YOUR_VALUE_HERE" \
	-e PDF_KNOWLEDGE_BASE_PATH="./pdf" \
	registry.hf.space/krax1337-advanced-gen-ai-2025:latest 
```

An AI-powered Chevrolet dealership chatbot that helps customers with questions about Corvette, Escalade, and Tahoe models.

## Features

- **AI Chatbot Interface**: Streamlit-based web interface for interacting with the assistant
- **PDF Knowledge Base**: ChromaDB vector database for semantic search of car manuals
- **Ticket Management**: Automatic creation of support tickets in Trello for escalated issues
- **OpenAI Integration**: Uses GPT models for natural language understanding and responses

## Architecture

### Components

- **Frontend**: Streamlit web application
- **Vector Database**: ChromaDB for PDF document storage and retrieval
- **LLM Integration**: OpenAI API for conversational AI capabilities
- **Ticket System**: Trello API integration for support ticket creation

### Technologies

- Python 3.12
- Streamlit
- ChromaDB
- OpenAI API
- Trello API
- Docker

## Setup

### Prerequisites

- Python 3.12+
- Docker (optional)
- OpenAI API key
- Trello API key, token, and list ID

### Environment Variables

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
TRELLO_API_KEY=your_trello_api_key
TRELLO_TOKEN=your_trello_token
TRELLO_LIST_ID=your_trello_list_id
PDF_KNOWLEDGE_BASE_PATH=pdf/
```

### Installation

#### Using Docker

```bash
docker build -t chevrolet-helpdesk .
docker run -p 7860:7860 chevrolet-helpdesk
```

#### Local Development

```bash
# Install uv package manager
pip install uv

# Install dependencies
uv sync

# Run the application
streamlit run main.py
```

## Usage

1. Access the web interface at http://localhost:7860
2. Ask questions about supported Chevrolet models (Corvette, Escalade, Tahoe)
3. The assistant will search the knowledge base for answers
4. For complex issues, the assistant can create a support ticket in Trello

## Adding Knowledge

Place PDF manuals in the `pdf/` directory. The system will automatically:

1. Extract text from the PDFs
2. Split content into appropriate chunks
3. Generate embeddings
4. Store in the ChromaDB database