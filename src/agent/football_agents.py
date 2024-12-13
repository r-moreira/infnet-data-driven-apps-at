from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor, Tool
from typing import List
from langchain import hub
from langchain_core.tools import Tool
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun


def load_tools() -> List[Tool]:
    """
        Carrega as ferramentas/tools disponíveis para o agente
    """
    tools = [
        WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(),
            description="A comprehensive wrapper around Wikipedia, ideal for retrieving"
                        " detailed information on a wide range of topics including people,"
                        " players, teams, competitions, stadiums (history and capacity),"
                        " cities, events, and more. Simply provide a search query as input."
        )
    ]
    return tools


def load_agent() -> AgentExecutor:
    """
        Carrega o agente de chat
    """
    llm = GoogleGenerativeAI(model="gemini-pro", temperature=0.2)
        
    prompt = hub.pull("hwchase17/react")
    
    prompt = PromptTemplate(
       input_variables=["agent_scratchpad",
                        "tool_names",
                        "tools"],
       template=prompt.template
    )
    tools = load_tools()
    agent = create_react_agent(llm, tools=tools, prompt=prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        verbose=True,
        max_iterations=5
    )
