from langsmith import Client
import os
from dotenv import load_dotenv

load_dotenv()

profile_sets = [
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
                },
                {
                    "role": "assistant",
                    "content": "I found a matching listing for you:\n\n- **Location**: Queenstown\n- **Unit**: Queens\n- **Room**: MBR Ensuite\n- **Rent**: $2350 (available for immediate move-in)\n\nTo proceed, I'll need a bit more information from you:\n\n1. Your Name\n2. Gender\n3. Profession\n4. Age\n5. Citizen (yes/no)\n6. Pass type\n7. Lease period (proposed)\n8. Move-in date (proposed)\n9. Number of members\n10. Cooking (yes/no)\n11. Visitors (yes/no)\n\nPlease provide these details so we can evaluate your profile and schedule a viewing."
                },
                {
                    "role": "user",
                    "content": "- Name: Kavya\n- Gender: Female\n- Profession: Working Professional\n- Age: 26\n- Citizen (yes/no): yes\n- Lease period: 1 year\n- Move-in date: 1 feb\n- Number of members: 1\n- Cooking (yes/no): no\n- Visitors (yes/no): no"
                },
                {
                    "role": "assistant",
                    "content": "Function call: get_available_timings\nArguments:\n{}"
                },
                {
                    "role": "function",
                    "name": "get_available_timings",
                    "content": "{\"Monday\":[\"10:00 AM\",\"11:00 AM\",\"2:00 PM\"],\"Tuesday\":[\"10:00 AM\",\"11:00 AM\",\"2:00 PM\"],\"Wednesday\":[\"10:00 AM\",\"11:00 AM\",\"2:00 PM\"],\"Thursday\":[\"10:00 AM\",\"11:00 AM\",\"2:00 PM\"],\"Friday\":[\"10:00 AM\",\"11:00 AM\",\"2:00 PM\"],\"Saturday\":[\"10:00 AM\",\"11:00 AM\",\"2:00 PM\"],\"Sunday\":[\"10:00 AM\",\"11:00 AM\",\"2:00 PM\"]}"
                }
            ],
        },
        "outputs": {
            "expected": "Your profile matches the listing requirements! The earliest available viewing slots are: \n\n - **Monday to Sunday**: 10:00 AM, 11:00 AM, or 2:00 PM \n\n Please let me know your preferred day and time for the viewing."
        }
    },
    {
        "inputs": {
            "time": "28 Apr 2025 04:23am",
            "messages": [
                {
                    "role": "user",
                    "content": "I'm looking to rent: RENT - Queenstown / Condo - Queens/ Original Common for 1800. Thanks."
                },
                {
                    "role": "assistant",
                    "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"common\", \n \"rent\": \"1800\"\n}"
                },
                {
                    "role": "function",
                    "name": "check_enquiry",
                    "content": "[{\"S.No.\":2,\"Availability\":\"2024-09-19 00:00:00\",\"Location\":\"Queenstown\",\"Condo Name\":\"Queens\",\"Unit Number\":\"Blk 16 #33-19\",\"Room\":\"Common\",\"Rent\":1750,\"Max no of pax in room\":1,\"Type of Bed\":\"Single\",\"Number of common toilet\":2,\"Links\":\"Link2\",\"Landlord Profile Preferences\":\"{'gender': 'Female', 'no_cooking': True, 'type_of_pass': 'EP', 'profession': 'Working Professional', 'no_visitors': True}\"},{\"S.No.\":3,\"Availability\":\"2024-10-18 00:00:00\",\"Location\":\"Queenstown\",\"Condo Name\":\"Queens\",\"Unit Number\":\"Blk 16 #33-19\",\"Room\":\"Common\",\"Rent\":1800,\"Max no of pax in room\":1,\"Type of Bed\":\"Single\",\"Number of common toilet\":2,\"Links\":\"Link3\",\"Landlord Profile Preferences\":\"{'profession': 'Student', 'move_in_date': 'Immediate', 'lease_period': '3-12 months'}\"}]"
                },
                {
                    "role": "assistant",
                    "content": "I found a couple of listings that match your preferences for a common room at Queens in Queenstown. One is available for $1,800 and the other for $1,750.\n\nTo proceed, could you please provide me with the following details?\n\n1. Name\n2. Gender\n3. Profession\n4. Age\n5. Citizen (yes/no)\n6. Pass type\n7. Lease period\n8. Move-in date\n9. No. of members\n10. Cooking (yes/no)\n11. Visitors (yes/no)\n\nThank you!"
                },
                {
                    "role": "user",
                    "content": "- Name: Ramkrishnani\n- Gender: Female\n- Profession: Working Professional\n- Age: 26\n- Citizen (yes/no): yes\n- Lease period: 1 year\n- Move-in date: 1 feb\n- Number of members: 1\n- Cooking (yes/no): yes\n- Visitors (yes/no): yes"
                }
            ],
        },
        "outputs": {
            "expected": "Unfortunately, the landlord doesn't allow cooking or visitors. Please let me know if you are flexible with these conditions. \n Additionally, can you also share your pass type (e.g. EP, S Pass)?"
        },
    },
  {
    "inputs": {
      "time": "8 May 2025 4:30pm",
      "messages": [
        {
          "role": "user",
          "content": "Interested in Common Room at Queens for 1800."
        },
        {
          "role": "assistant",
          "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"Common\",\n  \"rent\": \"1800\"\n}"
        },
        {
          "role": "function",
          "name": "check_enquiry",
          "content": "[{\"Condo Name\": \"Queens\", \"Room\": \"Common\", \"Rent\": 1750, \"Landlord Profile Preferences\": {\"gender\": \"Female\", \"no_cooking\": true, \"no_visitors\": true, \"profession\": \"Working Professional\", \"citizen\": \"yes\", \"lease_period\": \"1 year\", \"move_in_date\": \"Immediate\", \"max_members\": 1}}]"
        },
        {
          "role": "assistant",
          "content": "I found a matching listing for a Common room in the Queens condo. Could you please provide your profile details?"
        },
        {
          "role": "user",
          "content": "- Name: Shweta\n- Gender: Female\n- Profession: Working Professional\n- Age: 29\n- Citizen: yes\n- Pass type: EP\n- Lease period: 6 months\n- Move-in date: 1 July\n- Number of members: 2\n- Cooking: yes\n- Visitors: yes"
        }
      ]
    },
    "outputs": {
      "expected": "Your profile mostly matches the listing. However, only 1 person is allowed. Are you flexible to stay alone? Cooking and visitors are not allowed in this unit – would that be acceptable? Also, the landlord prefers a 1-year lease and immediate move-in. Can you consider adjusting your dates?"
    }
  },
  {
    "inputs": {
      "time": "8 May 2025 6:00pm",
      "messages": [
        {
          "role": "user",
          "content": "Can I rent a common room at Queens for $1800?"
        },
        {
          "role": "assistant",
          "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"Common\",\n  \"rent\": \"1800\"\n}"
        },
        {
          "role": "function",
          "name": "check_enquiry",
          "content": "[{\"Condo Name\": \"Queens\", \"Room\": \"Common\", \"Rent\": 1750, \"Landlord Profile Preferences\": {\"gender\": \"Female\", \"profession\": \"Working Professional\", \"citizen\": \"yes\"}}]"
        },
        {
          "role": "assistant",
          "content": "Found a possible match! Please share your profile details."
        },
        {
          "role": "user",
          "content": "- Name: Rohan\n- Gender: Male\n- Profession: Working Professional\n- Age: 30\n- Citizen: yes"
        }
      ]
    },
    "outputs": {
      "expected": "Unfortunately, the landlord requires a female tenant for this unit."
    }
  },
  {
    "inputs": {
      "time": "9 May 2025 9:15am",
      "messages": [
        {
          "role": "user",
          "content": "Looking for a common room at Queens. Max $1800."
        },
        {
          "role": "assistant",
          "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"Common\",\n  \"rent\": \"1800\"\n}"
        },
        {
          "role": "function",
          "name": "check_enquiry",
          "content": "[{\"Condo Name\": \"Queens\", \"Room\": \"Common\", \"Rent\": 1750, \"Landlord Profile Preferences\": {\"gender\": \"Female\", \"profession\": \"Working Professional\"}}]"
        },
        {
          "role": "assistant",
          "content": "Found a possible match! Can you share your profile details?"
        },
        {
          "role": "user",
          "content": "- Name: Meera\n- Gender: Female\n- Profession: Student\n- Age: 27\n- Citizen: yes"
        }
      ]
    },
    "outputs": {
      "expected": "This listing is only available for working professionals."
    }
  },
  {
    "inputs": {
      "time": "9 May 2025 12:30pm",
      "messages": [
        {
          "role": "user",
          "content": "Renting a common room at Queens – can go up to 1800."
        },
        {
          "role": "assistant",
          "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"Common\",\n  \"rent\": \"1800\"\n}"
        },
        {
          "role": "function",
          "name": "check_enquiry",
          "content": "[{\"Condo Name\": \"Queens\", \"Room\": \"Common\", \"Rent\": 1750, \"Landlord Profile Preferences\": {\"gender\": \"Female\", \"profession\": \"Working Professional\", \"age\": \"25-35\", \"citizen\": \"yes\"}}]"
        },
        {
          "role": "assistant",
          "content": "We have a good match! Please share your profile."
        },
        {
          "role": "user",
          "content": "- Name: Divya\n- Gender: Female\n- Profession: Working Professional\n- Age: 28\n- Citizen: yes\n- Pass type: EP\n- Lease period: 1 year\n- Move-in date: Immediate\n- Number of members: 1\n- Cooking: no\n- Visitors: no"
        }
      ]
    },
    "outputs": {
      "expected": "Your profile matches the listing! Let's schedule a viewing."
    }
  },
  {
    "inputs": {
      "time": "10 May 2025 10:45am",
      "messages": [
        {
          "role": "user",
          "content": "I'm looking to rent in Queens – common room – $1800 max"
        },
        {
          "role": "assistant",
          "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"Common\",\n  \"rent\": \"1800\"\n}"
        },
        {
          "role": "function",
          "name": "check_enquiry",
          "content": "[{\"Condo Name\": \"Queens\", \"Room\": \"Common\", \"Rent\": 1750, \"Landlord Profile Preferences\": {\"gender\": \"Female\", \"age\": \"25-35\", \"profession\": \"Working Professional\"}}]"
        },
        {
          "role": "assistant",
          "content": "Found a possible match. Could you share your profile details?"
        },
        {
          "role": "user",
          "content": "- Name: Anita\n- Gender: Female\n- Profession: Working Professional\n- Age: 40\n- Citizen: yes"
        }
      ]
    },
    "outputs": {
      "expected": "Unfortunately, the age requirement for this listing is between 25 and 35."
    }
  },
  {
    "inputs": {
      "time": "10 May 2025 1:00pm",
      "messages": [
        {
          "role": "user",
          "content": "Renting common room in Queens. $1800"
        },
        {
          "role": "assistant",
          "content": "Function call: check_enquiry\nArguments:\n{\n  \"unit_name\": \"Queens\",\n  \"room\": \"Common\",\n  \"rent\": \"1800\"\n}"
        },
        {
          "role": "function",
          "name": "check_enquiry",
          "content": "[{\"Condo Name\": \"Queens\", \"Room\": \"Common\", \"Rent\": 1750, \"Landlord Profile Preferences\": {\"gender\": \"Female\", \"citizen\": \"yes\"}}]"
        },
        {
          "role": "assistant",
          "content": "This unit may be a fit. Could you share your profile?"
        },
        {
          "role": "user",
          "content": "- Name: Latha\n- Gender: Female\n- Profession: Working Professional\n- Age: 30\n- Citizen: no"
        }
      ]
    },
    "outputs": {
      "expected": "The landlord prefers a citizen for this unit."
    }
  } 
]

client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
dataset_name = "profile_eval"
dataset = client.create_dataset(dataset_name)
client.create_examples(
    inputs=[e["inputs"] for e in profile_sets],
    outputs=[e["outputs"] for e in profile_sets],
    dataset_id=dataset.id,
)
