
def patch_profile(currProfile: dict, newProfile: dict) -> dict:
    print("------Adding Profile------")
    print(currProfile)
    print(newProfile)
    if (len(newProfile)==0):
        return currProfile
    for key, value in newProfile.items():
        currProfile[key] = value
    return currProfile

def add_enquiries(currEnquiries: dict, newEnquiry: dict) -> dict:
    print("------Adding Enquiries------")
    print(currEnquiries)
    print(newEnquiry)
    if (len(newEnquiry)==0 or newEnquiry==currEnquiries):
        return currEnquiries
    # try:
    #     newEnquiry = eval(newEnquiry)
    # except:
    #     print(newEnquiry)
    #     print("Cannot convert string to dict")
    #     return currEnquiries
    for key, val in currEnquiries.items():
        if newEnquiry['condo_name']==val['condo_name']:
            if newEnquiry['room_type']!='':
                val['room_type'] = newEnquiry['room_type']
            if newEnquiry['rent_value']!='':
                val['rent_value'] = newEnquiry['rent_value']
            if newEnquiry['rent_price']!='':
                val['rent_price'] = newEnquiry['rent_price']
            return currEnquiries
    currEnquiries[len(currEnquiries)+1] = newEnquiry
    print("------After Adding Enquiries------")
    print(currEnquiries)
    return currEnquiries
