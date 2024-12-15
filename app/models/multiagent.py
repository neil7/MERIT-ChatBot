import os
from langchain.memory import ConversationBufferMemory
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from pathlib import Path
import time

from app.utils.prompts import *

class Agent:
    def __init__(self, name, role, llm, retriever, promptType):
        self.name = name
        self.role = role
        self.llm = llm
        self.retrieval_chain = self.setup_retrieval_chain(retriever, promptType)

    def setup_retrieval_chain(self, retriever, promptType):
        prompt = self.get_prompt(promptType)
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            combine_docs_chain_kwargs={"prompt": prompt},
            return_source_documents=True,
            get_chat_history=lambda h: h
        )

    def get_prompt(self, promptType):
        if promptType == "context":
            template = context_prompt
        elif promptType == "cot":
            template = cot_prompt
        else:
            raise ValueError(f"Unknown prompt type: {promptType}")

        return PromptTemplate(
            input_variables=['context', 'chat_history', 'question'], 
            template=template
        )

    def process(self, query_dict):
        return self.retrieval_chain(query_dict)

class MultiAgentOrchestrator:
    def __init__(self, modelName="llama3.1"):
        self.modelName = modelName
        self.llm = ChatOllama(model=self.modelName, temperature=0.5)
        self.folder_path = "VectorDB/chroma_db_isro_d7_hkunlp"
        self.modelMap = {
            "meta-llama/Meta-Llama-3.1-8B-Instruct": "llama3.1",
            "llava/multimodal": "llava",
            "mistralai/Mistral-7B-Instruct-v0.2": "mistral",
            "microsoft/Phi-3-mini-4k-instruct": "phi3",
            "meta-llama/Meta-Llama-3.2-3B-Instruct": "llama3.2"
        }
        self.model_path = str(Path.home() / '.cache' / 'huggingface' / 'hub' / 'models--hkunlp--instructor-large' / 'snapshots' / '54e5ffb8d484de506e59443b07dc819fb15c7233')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.home() / '.cache' / 'huggingface')
        self.vectors = self.loadData()
        self.racs_vectors = self.loadracsData()
        self.agents = self.setup_agents()
        self.session_memory = ConversationBufferMemory(return_messages=True)
        self.inference_times = []
        print("Initialized inference_times list")

    def assignModel(self, option):
        self.modelName = self.modelMap[option]
        self.llm = ChatOllama(model=self.modelName, temperature=0.5)

    def loadData(self):
        embeddings = HuggingFaceEmbeddings(
            model_name=self.model_path,
            encode_kwargs={'batch_size': 32}
        )
        return Chroma(persist_directory=self.folder_path, embedding_function=embeddings)
    
    def loadracsData(self):
        embeddings = HuggingFaceEmbeddings(
            model_name=self.model_path,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'device': 'cpu', 'batch_size': 32}
        )
        return Chroma(persist_directory="VectorDB/chroma_db_isro_racs_d2_hkunlp", embedding_function=embeddings)

    def setup_agents(self):
        retriever = self.vectors.as_retriever()
        racs_retriever = self.racs_vectors.as_retriever()
        promptType = "cot"
        return {
            "Missions and Programs Agent": Agent("Missions and Programs Agent", "ISRO's space missions", self.llm, retriever, promptType),
            "Spacecraft and Technology Agent": Agent("Spacecraft and Technology Agent", "ISRO's technologies", self.llm, retriever, promptType),
            "Applications and Services Agent": Agent("Applications and Services Agent", "scientific impacts of ISRO's work", self.llm, retriever, promptType),
            "General Information and News Agent": Agent("General Information and News Agent", "general ISRO information", self.llm, retriever, promptType),
            "Education and Outreach Agent": Agent("Education and Outreach Agent", "general ISRO information", self.llm, retriever, promptType),
            "RESPOND Agent": Agent("RESPOND Agent", "ISRO RESPOND information", self.llm, racs_retriever, promptType)
        }

    def select_agent(self, query):
        prompt = f"""
        Given the following question about ISRO, select the most appropriate agent to answer it:
        Question: {query}

        Available agents:
        1. Missions and Programs Agent: Offers details about various ISRO missions (past, ongoing, and future. Provides information on different space programs and their objectives
        2. Spacecraft and Technology Agent: Gives information about different types of spacecrafts developed by ISRO. Explains key technologies and their applications in ISRO's work
        3. Applications and Services Agent: Informs about various applications of space technology in India. Provides details on services offered by ISRO (e.g., satellite data, telemedicine)
        4. General Information and News Agent: Provides overview information about ISRO, its history, and structure. Summarizes and retrieves the latest news, press releases, and updates
        5. Education and Outreach Agent: Offers information on ISRO's educational initiatives and outreach programs. Assists with queries related to student programs and opportunities
        6. RESPOND Agent: Provides overview and information about Regional Academic Centres for Space [RAC-S], which is a regional level new initiative to pursue advanced research in the areas of relevance to the future technological and programmatic needs of the Indian Space Programme. Provides research fellowship salary information under RAC-s, Sponsored Research, ISRO publishes focussed areas for research in the space domain and seek proposals from qualified academic institutions for joint research. PI will be identified by the institution, where as Co-PI will be joining from ISRO for carrying out the projects, .

        Respond with only the name of the most appropriate agent.
        """
        response = self.llm.predict(prompt)
        return response.strip()
    
    def get_inference_stats(self):
        if not self.inference_times:
            return "No inference times recorded yet."
        
        avg_time = sum(self.inference_times) / len(self.inference_times)
        max_time = max(self.inference_times)
        min_time = min(self.inference_times)
        
        return {
            "average_time": f"{avg_time:.2f}s",
            "max_time": f"{max_time:.2f}s",
            "min_time": f"{min_time:.2f}s"
        }

    def process_query(self, query):
        start_time = time.time()
        
        agent_name = self.select_agent(query)
        if agent_name in self.agents:
            agent = self.agents[agent_name]
        else:
            agent = self.agents["General Information and News Agent"]
        
        chat_history = self.session_memory.chat_memory.messages
        chat_history_str = "\n".join([f"{msg.type}: {msg.content}" for msg in chat_history])
        
        result = agent.process({
            "question": query,
            "chat_history": chat_history_str
        })

        self.session_memory.chat_memory.add_user_message(query)
        self.session_memory.chat_memory.add_ai_message(result['answer'])
        
        source_links = []
        if 'source_documents' in result:
            for doc in result['source_documents']:
                if 'source' in doc.metadata:
                    source_links.append(doc.metadata['source'])
        
        unique_links = list(set(source_links))
        
        end_time = time.time()
        inference_time = end_time - start_time
        self.inference_times.append(inference_time)
        
        return {
            "agent": agent_name,
            "response": result['answer'],
            "sources": unique_links,
            "inference_time": round(inference_time, 2)
        }

# Initialize global orchestrator
orchestrator = MultiAgentOrchestrator()