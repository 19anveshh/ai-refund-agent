from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s "
)

@tool
def get_user_purchase_history(user:str) -> dict:
    """
    this tool takes the username of the customer and return a dict of the purchased history if the user exits
    """
    logging.info(f"using get_user_purchase_history tool on user : {user}")
    if users_data.get(user):
        return users_data[user]
    return {"status":"there is no username found"}


@tool
def calculate_right_refund_amount(user:str,items:list[PurchaseItem]) -> str:
    """
    this tool takes a list of the items to be returned and the username and will return how much the refund is worth
    """

    logging.info(f"using calculate_right_refund_amount toll to get the user's :{user} refund")
    if users_data.get(user):
        total_refund = 0

        for item in items:
            if users_data[user].get(item.name):
                total_refund += users_data[user][item.name]["price"]

        return f"the value of the refund is: {total_refund} "
    return {"status":"there is no username found"}


@tool
def issue_refund_ticket(user:str,refund_amount:int)-> str:
    """
    this tool will send the ticket to the team to return the refund
    """
    logging.info(f"using issue_refund_ticket tool for user:{user}")
    return f"the refund ticket has be succesfully issued with the amount of {refund_amount}"

@tool
def get_today_time(user:str)->str:
    """
    this tool will return today's date
    """
    logging.info(f"using get_today_date")
    return date.today()


# print(get_user_purchase_history.invoke("user123"))