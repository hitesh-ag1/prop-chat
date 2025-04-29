from langgraph.types import Command
from typing import Literal
from langgraph.graph import END
from my_agent.utils.agents.check_enquiry.model import (    
        State,
    )
from my_agent.utils.agents.check_enquiry.helper import read_excel, match_enquiry
from my_agent.logging import logger

async def enquiry_chk_agent(state: State) -> Command[Literal["check_profile_agent", END]]:
    logger.info("-----Enquiry Check Agent-----")
    update = {
        "messages": state['messages'], 
        "listing_available": False, 
    }
    goto=END

    df = await read_excel()
    result, out = match_enquiry(state["condo_name"], state["room_type"], state["rental_price"], df)
    if all(result[k] for k in ("condo", "booked", "room", "rent")):
        update['listing_available'] = True
        update["listing_details"] = out
        goto = "check_profile_agent"
    else:
        update["followup"] = out["message"]                
    
    return Command(update=update, goto=goto)