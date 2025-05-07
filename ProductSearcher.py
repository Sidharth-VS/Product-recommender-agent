from dotenv import load_dotenv
import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, AgentType
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor



getenv = load_dotenv()

class ProductSearcher():
    def __init__(self):
        self.llm = ChatGroq(temperature=0, api_key=os.getenv("GROQ_API_KEY"), model_name="deepseek-r1-distill-llama-70b")
        self.searchTool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
        self.tools = [self.searchTool]
        self.systemPrompt = "You are a product Specialist. With the given category and use case you have to find products using the search tool."
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", self.systemPrompt,
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )
        self.llmWithTools = self.llm.bind_tools(self.tools)
        self.agent = (
                    {
                        "input": lambda x: x["input"],
                        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                            x["intermediate_steps"]
                        ),
                    }
                    | self.prompt
                    | self.llmWithTools
                    | OpenAIToolsAgentOutputParser()
                )
        
    def searchProduct(self, category, useCase):
        input = f"""Find 5 products that match the category and Use case by doing a web search
                    category:{category}
                    use case:{useCase}
                Output Format:
                No preamble
                Return a valid JSON array of strings of names of products with no explanation or formatting. Example:
                ["Product 1", "Product 2", "Product 3"]"""
        agentExecutor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)
        response = agentExecutor.invoke({"input":input})["output"]

        if isinstance(response, str):
            try:
                productList = json.loads(response)
            except json.JSONDecodeError:
                productList = []
        elif isinstance(response, (list, dict)):
            productList = response
        else:
            productList = [] 

        return productList  

   

       

