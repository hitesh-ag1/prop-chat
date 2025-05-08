from langsmith import Client
import os
from dotenv import load_dotenv

load_dotenv()

enquiry_sets = [
    {
        "inputs": {
            "time": "8 May 2025 9:45am",
            "messages": [
                {
                    "role": "user",
                    "content": "Hi Alice, I'm looking to rent: RENT – Queenstown / Condo – Queens / Original Common for 1800. Thanks"
                },
                {
                    "role": "assistant",
                    "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"Original Common\",\n  \"rent\": \"1800\"\n}"
                },
                {
                    "role": "function",
                    "name": "check_enquiry",
                    "content": "{\n  \"S.No.\": 2,\n  \"Availability\": \"2024-09-19 00:00:00\",\n  \"Location\": \"Queenstown\",\n  \"Condo Name\": \"Queens\",\n  \"Unit Number\": \"Blk 16 #33-19\",\n  \"Room\": \"Common\",\n  \"Rent\": 1750,\n  \"Max no of pax in room\": 1,\n  \"Type of Bed\": \"Single\",\n  \"Number of common toilet\": 2,\n  \"Links\": \"Link2\",\n  \"Landlord Profile Preferences\": {\n    \"gender\": \"Female\",\n    \"no_cooking\": true,\n    \"type_of_pass\": \"EP\",\n    \"profession\": \"Working Professional\",\n    \"no_visitors\": true\n  }\n}"
                }
            ],
        },
        "outputs": {
            "expected": "I found a matching listing for a Common room in the Queens condo.\n\nCould you please provide the following details to proceed?\n- Name\n- Gender\n- Profession\n- Age\n- Citizen (yes/no)\n- Pass type\n- Lease period\n- Move-in date\n- No. of members\n- Cooking (yes/no)\n- Visitors (yes/no)"
        },
    },
    {
        "inputs": {
            "time": "30 Nov 2026 2:50am",
            "messages": [
                {
                    "role": "user",
                    "content": "Hey Alice, do you have anything in Tiong Bahru around 2.2k budget? Prefer ensuite."
                },
                {
                    "role": "assistant",
                    "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Tiong Bahru\",\n  \"room\": \"ensuite\",\n  \"rent\": \"2200\"\n}"
                },
                {
                    "role": "function",
                    "name": "check_enquiry",
                    "content": "Error: ValueError(\"Sorry, 'Tiong Bahru' is not currently available with this agent. Please try another property.\")\n Please fix your mistakes."
                }
            ],
        },
        "outputs": {
            "expected": "Sorry, can you please provide the exact condo name in Tiong Bahru? I can help you find a match if you have a specific property in mind."
        },
    },
    {
        "inputs": {
            "time": "16 Nov 2025 12:00am",
            "messages": [
                {
                    "role": "user",
                    "content": "Looking to rent: MBR Ensuite – Queens – Queenstown. Max $2500."
                },
                {
                    "role": "assistant",
                    "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"MBR Ensuite\",\n  \"rent\": \"2500\"\n}"
                },
                {
                    "role": "function",
                    "name": "check_enquiry",
                    "content": [{"S.No.":1,"Availability":"Immediate","Location":"Queenstown","Condo Name":"Queens","Unit Number":"Blk 16 #33-19","Room":"MBR Ensuite","Rent":2350,"Max no of pax in room":"Upto 2","Type of Bed":"Queen","Number of common toilet":"-","Links":"Link1","Landlord Profile Preferences":"{'gender': 'Any', 'age': '25-35', 'profession': 'Working Professional', 'move_in_date': 'ASAP', 'lease_period': '1 year'}"}]
                }
            ],
        },
        "outputs": {
            "expected": "I found a match for your enquiry: \n- **Unit:** Queens, Queenstown \n- **Room Type:** MBR Ensuite \n- **Rent:** $2350 (available immediately)\n\n Please provide the following details to proceed:\n1. Name\n2. Gender\n3. Profession\n4. Age\n5. Are you a Singapore Citizen (Yes/No)?\n6. Pass type\n7. Lease period\n8. Move-in date\n9. Number of members\n10. Cooking (Yes/No)\n11. Visitors (Yes/No)"
        }
    },
    {
        "inputs": {
            "time": "28 Apr 2025 04:23am",
            "messages": [
                {
                    "role": "user",
                    "content": "Hi, is there anything in D’Leedon with attached bathroom? Need asap."
                },
                {
                    "role": "assistant",
                    "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"D’Leedon\",\n  \"room\": \"master\"}"
                },
                {
                    "role": "function",
                    "name": "check_enquiry",
                    "content": "Error: ValueError('Please provide all required details: unit name, room type, and rent.')\n Please fix your mistakes."
                }
            ],
        },
        "outputs": {
            "expected": "Could you please provide the desired rent amount along with your enquiry for D’Leedon with an attached bathroom (master room)?"
        },
    },
    {
        "inputs": {
            "time": "9 May 2025 10:50am",
            "messages": [
                {
                    "role": "user",
                    "content": "I'm interested in Trevista but flexible with area. Budget 2.5k max."
                },
                {
                    "role": "assistant",
                    "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Trevista\",\n  \"room\": null,\n  \"rent\": \"2500\"\n}"
                },
                {
                    "role": "function",
                    "name": "check_enquiry",
                    "content": "Error: ValueError('Please provide all required details: unit name, room type, and rent.')\n Please fix your mistakes."
                }
            ],
        },
        "outputs": {
            "expected": "Could you please provide the desired room type (e.g., common, master) along with your enquiry for Trevista?"
        },
    },
    {
        "inputs": {
            "time": "29 Mar 2021 08:34am",
            "messages": [
                {
                    "role": "user",
                    "content": "Hey, are you free for kopi later? Got something to tell you."
                },
            ],
        },
        "outputs": {
            "expected": "I'm here to assist with rental enquiries only. Let me know how I can help with your property search!"
        },
    },
    {
        "inputs": {
            "time": "23 Nov 2025 12:50am",
            "messages": [
                {
                    "role": "user",
                    "content": "Hey Alice! Can you send me the floor plan for Trevista?"
                },
            ],
        },
        "outputs": {
            "expected": "I'm here to assist with rental enquiries only. Let me know how I can help with your property search!"
        },
    },
    {
        "inputs": {
            "time": "14 Apr 2025 1:00am",
            "messages": [
                {
                    "role": "user",
                    "content": "Are visitors allowed at Senja Gateway units?"
                },
            ],
        },
        "outputs": {
            "expected": "I'm here to assist with rental enquiries only. Let me know how I can help with your property search!"
        },
    },
    {
        "inputs": {
            "time": "1 Jan 2025 12:00pm",
            "messages": [
                {
                    "role": "user",
                    "content": "Good afternoon Benjamin, I'm looking to rent Junior MBR Ensuite in Kensington Park Condo for 2,100. Thanks"
                },
                {
                    "role": "assistant",
                    "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Kensington Park Condo\",\n  \"room\": \"Junior MBR Ensuite\",\n  \"rent\": \"2100\"\n}"
                }
            ]
        },
        "outputs": {
            "expected": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Kensington Park\",\n  \"room\": \"Junior MBR Ensuite\",\n  \"rent\": \"2100\"\n}"
        },
    },
]

client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
dataset_name = "enquiry_eval"
dataset = client.create_dataset(dataset_name)
client.create_examples(
    inputs=[e["inputs"] for e in enquiry_sets],
    outputs=[e["outputs"] for e in enquiry_sets],
    dataset_id=dataset.id,
)
