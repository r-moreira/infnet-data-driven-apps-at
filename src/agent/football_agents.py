from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor, Tool
from typing import List
from langchain import hub
from langchain_core.tools import Tool
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from .football_tools import get_player_info, get_match_events

def load_tools() -> List[Tool]:
    """
        Carrega as ferramentas/tools disponíveis para o agente
    """
    tools = [
        get_player_info,
        get_match_events,
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
    prompt = """
    Answer the following questions as best you can. You have access to the following tools:
    {tools}

    Use the following format:

    Question: the input question you must answer

    Thought: you should always think about what to do

    Action: the action to take, should be one of [{tool_names}]

    Action Input: the input to the action

    Observation: the result of the action

    ... (this Thought/Action/Action Input/Observation can repeat N times)

    Thought: I now know the final answer

    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}

    Information Related to the Question: {related_info}

    Thought: {agent_scratchpad}
    """
    
    prompt = PromptTemplate(
       input_variables=[
                        "related_info",
                        "input",
                        "agent_scratchpad",
                        "tool_names",
                        "tools"
                    ],
       template=prompt
    )
    
    # llm = GoogleGenerativeAI(model="gemini-pro", temperature=0.2)
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    tools = load_tools()
    agent = create_react_agent(llm, tools=tools, prompt=prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        verbose=True,
        max_iterations=5
    )
