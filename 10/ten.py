## 參考連結:https://python.langchain.com/v0.1/docs/modules/agents/agent_types/react/
import os  
from langchain import hub  
from langchain.agents import AgentExecutor, create_react_agent 
from langchain_community.tools.tavily_search import TavilySearchResults  
from langchain_groq import ChatGroq 


groq_key = os.environ.get("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")
tavily_api_key = os.environ.get("TAVILY_API_KEY", "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")

tools = [TavilySearchResults(max_results=1)]

### 從hub中拉取指定的模型(prompt)
prompt = hub.pull("hwchase17/react")


llm = ChatGroq(api_key=groq_key)

###使用create_react_agent函式創建一個代理人(agent)，並將ChatGroq物件(llm)、tools列表和prompt作為參數
agent = create_react_agent(llm, tools, prompt)

### 創建一個AgentExecutor物件，並將代理人(agent)、tools列表和verbose=True作為參數
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "請幫我列出NBA從2012到2022的冠軍隊伍?"})
