
from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from models import model
from objects import Answer
from prompts import agent_system_prompt
from tools import (
    calculate_right_refund_amount,
    get_today_time,
    get_user_purchase_history,
    issue_refund_ticket,
)

load_dotenv()

agent = create_agent(
    model=model,
    system_prompt=agent_system_prompt,
    tools=[
        calculate_right_refund_amount,
        get_today_time,
        get_user_purchase_history,
        issue_refund_ticket,
    ],
    response_format=Answer,
    checkpointer=InMemorySaver(),
)


def run_conversation():
    config = {
        "configurable": {
            "thread_id": str(uuid4()),
        }
    }

    user_input = "I would like to request a refund"

    while True:
        print(user_input)

        response = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=user_input),
                ]
            },
            config=config,
        )

        structured_response = response["structured_response"]
        print(structured_response.answer)

        if not structured_response.conversation:
            break

        user_input = input("reply:\n")

    print("The job is done!")

run_conversation()