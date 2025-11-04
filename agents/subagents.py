from agents.utils import llm, get_engine_for_chinook_db
from langchain_community.utilities.sql_database import SQLDatabase
from typing_extensions import TypedDict
from typing import Annotated, NotRequired
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed.is_last_step import RemainingSteps
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

from agents.utils import db
from agents.prompts import invoice_subagent_prompt
from agents.tools import invoice_tools

class InputState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class State(InputState):
    customer_id: NotRequired[int]
    loaded_memory: NotRequired[str]


# ------------------------------------------------------------
# Invoice Subagent
# ------------------------------------------------------------
invoice_subagent = create_agent(
    llm, 
    tools=invoice_tools, 
    name="invoice_subagent", 
    system_prompt=invoice_subagent_prompt, 
    state_schema=State
)

# ------------------------------------------------------------
# Opensearch E-commerce Subagent
# ------------------------------------------------------------

# TODO: Add Opensearch E-commerce Subagent