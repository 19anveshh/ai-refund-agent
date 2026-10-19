from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date,datetime


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
def issue_refund_ticket(
    user: str,
    refund_amount: int,
    items: list[PurchaseItem],
) -> dict:
    """Validate eligible items and issue a refund ticket."""

    logging.info(f"Using issue_refund_ticket for user: {user}")

    if user not in users_data:
        return {"status": "error", "message": "User was not found"}

    for item in items:
        purchase = users_data[user].get(item.name)

        if purchase is None:
            return {
                "status": "error",
                "message": f"{item.name} was not purchased",
            }

        purchase_date = datetime.strptime(
            purchase["date"], "%Y-%m-%d"
        ).date()

        days_old = (date.today() - purchase_date).days

        if days_old < 0 or days_old > 30:
            return {
                "status": "error",
                "message": f"{item.name} is not eligible for a refund",
            }

    return {
        "status": "success",
        "message": (
            f"Refund ticket successfully issued for "
            f"{refund_amount} for user {user}"
        ),
    }

@tool
def get_today_time(user:str)->str:
    """
    this tool will return today's date
    """
    logging.info(f"using get_today_date")
    return date.today().isoformat()

@tool
def check_refund_eligibility(user: str, item_name: str) -> str:
    """Check whether a purchased item is eligible for a refund."""

    if user not in users_data:
        return "No user was found."

    purchase = users_data[user].get(item_name)

    if purchase is None:
        return f"{item_name} was not purchased by {user}."

    try:
        purchase_date = date.fromisoformat(purchase["date"])
    except (KeyError, TypeError, ValueError):
        return f"The purchase date for {item_name} is invalid."

    today = date.today()
    days_old = (today - purchase_date).days

    if days_old < 0:
        return f"{item_name} is not eligible because its purchase date is in the future."

    if days_old > 30:
        return f"{item_name} is not eligible because it was purchased {days_old} days ago."

    return f"{item_name} is eligible for a refund. It was purchased {days_old} days ago."

# print(get_user_purchase_history.invoke("user123"))