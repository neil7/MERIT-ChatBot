<!-- ```markdown -->
# Multi-Agent Chatbot API 🚀

<div align="center">

A cutting-edge Flask-based API powered by a multi-agent LLM architecture, leveraging Retrieval-Augmented Generation (RAG) for highly contextual and accurate responses.

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents designed for diverse domains:
  - Missions & Programs
  - Technology Information
  - Applications & Services
  - General Information
  - Education & Outreach
  - Research Opportunities

- **State-of-the-Art RAG Implementation**: Ensures accurate, contextually rich answers.
- **Support for Multiple LLMs**: Compatibility with advanced language models:
  - Meta Llama 3.1/3.2
  - Mistral
  - Phi-3
  - LLaVa (Multimodal)
- **Real-Time Metrics**: Tracks inference time and agent performance.

## 🛠️ Technology Stack

- **Framework**: Flask
- **Language Models**: Meta Llama, Mistral, Phi-3
- **Vector Store**: ChromaDB
- **Embeddings**: HuggingFace
- **Memory Management**: Langchain ConversationBufferMemory

## 🚀 Quick Start

### Prerequisites

```bash
# Create and activate a conda environment
conda create -n chatbot-api python=3.10
conda activate chatbot-api

# Install required dependencies
pip install -r requirements.txt
```

### Running the API

```bash
python run.py
```

Access the API at `http://localhost:5001/api/`.

## 📚 API Documentation

### Endpoints

1. **Chat Endpoint**
   ```http
   POST /api/chat
   ```
   **Request Body:**
   ```json
   {
       "query": "Your question here",
       "model": "meta-llama/Meta-Llama-3.1-8B-Instruct" // optional
   }
   ```

2. **Models Endpoint**
   ```http
   GET /api/models
   ```

3. **Stats Endpoint**
   ```http
   GET /api/stats
   ```

## 📁 Project Structure

```
chatbot-api/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── multiagent.py
│   └── utils/
│       ├── __init__.py
│       └── prompts.py
├── config/
│   ├── __init__.py
│   └── config.py
├── VectorDB/
├── requirements.txt
└── run.py
```

## 🧪 Testing

Run the following command to test all API endpoints:

```bash
python test_api.py
```

Alternatively, use Postman with the provided collection:
[Download Postman Collection](postman/Chatbot_API.json).

## 📊 Performance Metrics

The API provides detailed performance insights:
- Response time
- Inference statistics
- Agent selection accuracy

Access metrics via the `/api/stats` endpoint.

## 🛣️ Roadmap

- [ ] Add user authentication
- [ ] Implement rate limiting
- [ ] Expand LLM support
- [ ] Improve response caching
- [ ] Add Docker support for deployment

## 🤝 Contributing

We welcome contributions to improve this project! Refer to our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`.
3. Commit your changes: `git commit -m 'Add AmazingFeature'`.
4. Push to the branch: `git push origin feature/AmazingFeature`.
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ✨ Acknowledgments

- The open-source community for invaluable tools and libraries.
- All contributors who have helped shape this project.

## 📧 Contact

For more information, visit the project repository: [https://github.com/yourusername/chatbot-api](https://github.com/yourusername/chatbot-api).

---

<div align="center">
Built with ❤️ for the Open Source Community
</div>
<!-- ``` -->
