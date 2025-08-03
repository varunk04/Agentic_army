from langchain_community.chat_models import ChatOpenAI
from agents.research_agent import ResearchSynthesizerAgent
import os
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",   # or e.g., meta-llama/Llama-3-8b
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api_token
)

# writer = WriterAgent(llm)
# article = writer.write_article("The future of AI agents", style="newsletter")
# print(article)


agent = ResearchSynthesizerAgent(llm)

query = input("Enter your research question/topic: ")
print("\n--- Research Synthesizer Report ---\n")
result = agent.synthesize(query)
print(result)
