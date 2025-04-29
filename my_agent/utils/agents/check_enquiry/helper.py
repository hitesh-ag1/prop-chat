
import pandas as pd
from dotenv import load_dotenv
import os
import asyncio


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


def match_enquiry(condo, room, rent, listings):
    matching = {
        "condo": True,
        "booked": True,
        "room": True,
        "rent": True,
    }

    matched_data = listings[
        (listings['Condo Name'].str.lower() == condo.lower())
    ]
    if matched_data.empty:
        matching["condo"] = False
        message = "Condo is not available"
        return matching, {
            "message": message,
        }
    
    matched_data = matched_data[
        (matched_data['Availability'].str.lower() != 'booked')
    ]

    if matched_data.empty:
        matching["booked"] = False
        message = "Condo is booked"
        return matching, {
            "message": message,
        }
    
    if "common" in room.lower():
        room_type = "common"

    matched_data_room = matched_data[matched_data['Room'].str.lower() == room_type.lower()]
    if matched_data_room.empty:
        matching["room"] = False
        message = "Room Type is Not Available. Available Room Types are: " + ', '.join(matched_data['Room'].unique())
        return matching, {
            "message": message,
        }
    
    range = 400
    rent_price = int(rent)
    matched_data_rent = matched_data_room[(matched_data_room['Rent'] >= rent_price - range) & (matched_data_room['Rent'] <= rent_price + range)]
    if matched_data_rent.empty:
        matching["rent"] = False
        message = "Rent Price is Not Available. Available Rent Prices are: " + ', '.join(matched_data_room['Rent'].unique())
        return matching, {
            "message": message,
        }
    
    matched_data_rent = matched_data_rent.to_dict(orient='records')
    return matching, matched_data_rent
