import requests
import json
import time

class ISROChatbotTester:
    def __init__(self):
        self.base_url = "http://localhost:5001/api"
        self.headers = {"Content-Type": "application/json"}

    def test_chat(self):
        """Test the chat endpoint"""
        print("\nTesting Chat Endpoint...")
        url = f"{self.base_url}/chat"
        
        # Test basic query
        query = "What is the salary of JRF?"
        data = {"query": query}
        
        response = requests.post(url, json=data, headers=self.headers)
        print(f"Query: {query}")
        print("Response:", json.dumps(response.json(), indent=2))

        # Test with model selection
        query = "Tell me about Aditya L1 mission"
        data = {
            "query": query,
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct"
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        print(f"\nQuery with model selection: {query}")
        print("Response:", json.dumps(response.json(), indent=2))

    def test_models(self):
        """Test the models endpoint"""
        print("\nTesting Models Endpoint...")
        url = f"{self.base_url}/models"
        
        response = requests.get(url)
        print("Available Models:", json.dumps(response.json(), indent=2))

    def test_stats(self):
        """Test the stats endpoint"""
        print("\nTesting Stats Endpoint...")
        url = f"{self.base_url}/stats"
        
        response = requests.get(url)
        print("Stats:", json.dumps(response.json(), indent=2))

    def run_multiple_queries(self):
        """Test multiple queries in succession"""
        print("\nTesting Multiple Queries...")
        url = f"{self.base_url}/chat"
        
        queries = [
            "What is the salary of JRF?",
            "Tell me about Aditya L1 mission",
            "What are the RAC-S centers in India?"
        ]

        for query in queries:
            data = {"query": query}
            response = requests.post(url, json=data, headers=self.headers)
            print(f"\nQuery: {query}")
            print("Response:", json.dumps(response.json(), indent=2))
            time.sleep(1)  # Add delay between requests

def main():
    tester = ISROChatbotTester()
    
    # Test individual endpoints
    tester.test_chat()
    tester.test_models()
    tester.test_stats()
    
    # Test multiple queries
    tester.run_multiple_queries()

if __name__ == "__main__":
    main()