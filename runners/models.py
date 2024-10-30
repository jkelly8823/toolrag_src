import getpass
import os
from dotenv import load_dotenv
from typing import Literal
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from PIL import Image
import io

# Model Specific
from langchain_anthropic import ChatAnthropic

# Custom Files
from sasts import *
from prompts import *
from prompters import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOGIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
load_dotenv()

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("ANTHROPIC_API_KEY")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEFINE TOOLS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@tool
def run_flawfinder(code_sample: str, file_suffix: str) -> str:
    """Call to run the Flawfinder static analysis tool."""
    return go_flawfinder(code_sample, file_suffix)

tools = [run_flawfinder]
tool_node = ToolNode(tools)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODELS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

model_with_tools = ChatAnthropic(
    model="claude-3-haiku-20240307", temperature=0
).bind_tools(tools)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ReAct AGENTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Control number of previous messages used
def filter_messages(messages: list):
    return messages
    # # This is very simple helper function which only ever uses the last message
    # return messages[-1:]

def call_model(state: MessagesState):
    messages = filter_messages(state["messages"])
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ReAct AGENTS GRAPH VIEWER
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# try:
#     # Get the PNG image as bytes
#     img_data = app.get_graph().draw_mermaid_png()  # Image data in bytes

#     # Use BytesIO to open the image directly from bytes
#     img = Image.open(io.BytesIO(img_data))
#     img.show()  # This opens the image with the default viewer without saving it to disk
# except Exception as e:
#     print(f"Error displaying image: {e}")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PROMPTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

samples = form_prompt('BRYSON',PROMPT_INST, 1)

msgs = [("human",entry["prompt"]) for entry in samples if "prompt" in entry]
msgs.insert(0,("system", SYS_INST))
msgs = truncate_tokens_from_messages(msgs, "claude-3-haiku-20240307", 2048)
# print(msgs)

# One-Off Sample
# test_code_snip = (
#     "void calculateDiscountedPrice(char *userInput, int itemPrice, float discountRate) {\n"
#     "    char buffer[10];\n"
#     "    int discountedPrice;\n"
#     "    float discountAmount;\n"
#     "    if (isLoggedIn) {\n"
#     "        strcpy(buffer, userInput);\n"
#     "        discountAmount = (itemPrice * discountRate) / 100;\n"
#     "        discountedPrice = itemPrice - (int)discountAmount;\n"
#     "        sprintf(buffer, \"Discounted Price: %d\", discountedPrice);\n"
#     "        printf(\"%s\\n\", buffer);\n"
#     "    } else {\n"
#     "        printf(\"User is not logged in.\\n\");\n"
#     "    }\n"
# "}\n"
# )
# test_code_ext = ".cpp"
# msgs = [("human", f"Is this {test_code_ext} code vulnerable?\n\n{test_code_snip}")]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Sample Calls to ReAct Agent
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# example with a single tool call
for chunk in app.stream({"messages": msgs}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
