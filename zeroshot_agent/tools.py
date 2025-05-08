import pandas as pd
from dotenv import load_dotenv
import os
import asyncio
from typing import Optional
from langchain_core.tools import tool


load_dotenv()


EXCEL_PATH = os.getenv('EXCEL_PATH')

def _read_excel_sync():
    """Synchronous function to read excel file"""
    return pd.read_excel(EXCEL_PATH, engine='openpyxl')


async def read_excel():
    """Asynchronous wrapper for reading excel file"""
    # Run the blocking pandas operation in a separate thread
    df = await asyncio.to_thread(_read_excel_sync)
    return df

@tool
async def check_enquiry(
        unit_name: Optional[str]=None, 
        room: Optional[str]=None, 
        rent: Optional[str]=None
    ):
    """
    Checks if a user's property enquiry matches available agent listings based on:
    - Unit name
    - Room type
    - Rent price

    Returns matching listing details if found, or provides specific feedback on what part of the enquiry does not match (e.g., unit not found, unit already booked, room type not available, or rent mismatch).

    Args:
        unit_name (str, optional): The name of the property or condominium.
        room (str, optional): The desired room type (e.g., common, master).
        rent (str, optional): The desired rent price.

    Returns:
        list[dict]: Matching listing(s), if all details match.

    Raises:
        ValueError: If any of unit name, room type, or rent does not match. Error message provides guidance on the issue.
    """
    if unit_name is None or room is None or rent is None:
        message = "Please provide all required details: unit name, room type, and rent."
        raise ValueError(message)
    
    listings = await read_excel()
    matched_data = listings[
        (listings['Condo Name'].str.lower() == unit_name.lower())
    ]
    if matched_data.empty:
        message = f"Sorry, '{unit_name}' is not currently available with this agent. Please try another property."
        raise ValueError(message)
    
    matched_data['Availability'] = matched_data['Availability'].astype(str)
    matched_data = matched_data[
        (matched_data['Availability'].str.lower() != 'booked')
    ]

    if matched_data.empty:
        message = f"Unfortunately, all units for '{unit_name}' are already booked. Please enquire about another property."
        raise ValueError(message)
    
    if "common" in room.lower():
        room = "common"

    matched_data_room = matched_data[matched_data['Room'].str.lower() == room.lower()]
    if matched_data_room.empty:
        available_rooms = ', '.join(matched_data['Room'].unique())
        message = f"Sorry, the requested room type ('{room}') is not available at '{unit_name}'. Available room types: {available_rooms}."
        raise ValueError(message)
    
    range = 400
    rent_price = int(rent)
    matched_data_rent = matched_data_room[(matched_data_room['Rent'] >= rent_price - range) & (matched_data_room['Rent'] <= rent_price + range)]
    if matched_data_rent.empty:
        available_rents = ', '.join(str(r) for r in matched_data_room['Rent'].unique())
        message = (
            f"The requested rent price (around ${rent}) does not match available options for the chosen room at '{unit_name}'. "
            f"Available rent prices: {available_rents}."
        )
        raise ValueError(message)
    
    matched_data_rent = matched_data_rent.to_dict(orient='records')
    return matched_data_rent

@tool
def get_available_timings():
    """Get available timings for property viewings."""
    return {
        "Monday": ["10:00 AM", "11:00 AM", "2:00 PM"],
        "Tuesday": ["10:00 AM", "11:00 AM", "2:00 PM"],
        "Wednesday": ["10:00 AM", "11:00 AM", "2:00 PM"],
        "Thursday": ["10:00 AM", "11:00 AM", "2:00 PM"],
        "Friday": ["10:00 AM", "11:00 AM", "2:00 PM"],
        "Saturday": ["10:00 AM", "11:00 AM", "2:00 PM"],
        "Sunday": ["10:00 AM", "11:00 AM", "2:00 PM"]
    }