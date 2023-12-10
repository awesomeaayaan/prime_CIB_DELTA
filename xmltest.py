# import pandas as pd
# import xml.etree.ElementTree as ET

# # Parse the XML file
# tree = ET.parse(r"D:\primeaccuityScreening\ac_UPIDGWL1\ENTITY.XML")
# root = tree.getroot()

# # Initialize empty lists to store data
# data = {'ID': [], 'Name': [], 'ListID': [], 'ListCode': [], 'EntityType': [],
#         'CreatedDate': [], 'LastUpdateDate': [], 'Source': [], 'OriginalSource': [],
#         'Title': [], 'OtherInformation': [], 'DirectID': [], 'EntityLevel': [],
#         'NameSource': [], 'OriginalID': [], 'SubCategory': [],
#         'City': [], 'State': [], 'StateName': [], 'Country': [], 'CountryName': [],
#         'Address1': [], 'AddressCity': [], 'AddressState': [], 'AddressStateName': [],
#         'AddressCountry': [], 'AddressCountryName': [], 'PostalCode': []}

# # Loop through entities in the XML
# for entity in root.findall('.//entity'):
#     data['ID'].append(entity.attrib['id'])
#     data['Name'].append(entity.find('name').text)
#     data['ListID'].append(entity.find('listId').text)
#     data['ListCode'].append(entity.find('listCode').text)
#     data['EntityType'].append(entity.find('entityType').text)
#     data['CreatedDate'].append(entity.find('createdDate').text)
#     data['LastUpdateDate'].append(entity.find('lastUpdateDate').text)
#     data['Source'].append(entity.find('source').text)
#     data['OriginalSource'].append(entity.find('OriginalSource').text)

#     # Titles
#     title = entity.find('.//titles/title')
#     data['Title'].append(title.text if title is not None else '')

#     # # SDFs
#     # sdfs = entity.find('.//sdfs')
#     # for sdf in sdfs.findall('sdf'):
#     #     data[sdf.attrib['name']].append(sdf.text if sdf.text is not None else '')
#     # SDFs
#     # SDFs
#     sdfs = entity.find('.//sdfs')
#     for sdf in sdfs.findall('sdf'):
#         sdf_name = sdf.attrib['name']
#         sdf_text = sdf.text if sdf.text is not None else ''

#         # Check if the key exists in the data dictionary
#         if sdf_name in data:
#             data[sdf_name].append(sdf_text)
#         else:
#             # If the key doesn't exist, create it with an empty list
#             data[sdf_name] = [sdf_text]

#     # Ensure that all keys are present, even if not found in this entity
#     for key in data.keys():
#         if key not in sdfs.attrib:
#             data[key].append('')

#     # Addresses
#     addresses = entity.find('.//addresses/address')
#     if addresses is not None:
#         city_element = addresses.find('city')
#         data['City'].append(city_element.text if city_element is not None else '')
#         # data['City'].append(addresses.find('city').text)

#         state_element = addresses.find('state')
#         data['State'].append(state_element.text if state_element is not None else '')
#         # data['State'].append(addresses.find('state').text)
#         statename_element = addresses.find('stateName')
#         data['StateName'].append(statename_element.text if statename_element is not None else '')
#         # data['StateName'].append(addresses.find('stateName').text)
#         country_element = addresses.find('country')
#         data['Country'].append(country_element.text if country_element is not None else '')
#         # data['Country'].append(addresses.find('country').text)
#         countryname_element = addresses.find('countryName')
#         data['CountryName'].append(countryname_element.text if countryname_element is not None else '')
#         # data['CountryName'].append(addresses.find('countryName').text)

#         # Check if 'address1' element exists before accessing 'text'
#         address1_element = addresses.find('address1')
#         data['Address1'].append(address1_element.text if address1_element is not None else '')
        
#         addresscity_element = addresses.find('city')
#         data['AddressCity'].append(addresscity_element.text if addresscity_element is not None else '')
#         # data['AddressCity'].append(addresses.find('city').text)
#         addressstate_element = addresses.find('state')
#         data['AddressState'].append(addressstate_element.text if addressstate_element is not None else '')
#         # data['AddressState'].append(addresses.find('state').text)
#         addressstatename = addresses.find('stateName')
#         data['AddressStateName'].append(addressstatename.text if addressstatename is not None else '')
#         # data['AddressStateName'].append(addresses.find('stateName').text)
#         addresscountry_element = addresses.find('country')
#         data['AddressCountry'].append(addresscountry_element.text if addresscountry_element is not None else '')
#         # data['AddressCountry'].append(addresses.find('country').text)
#         addresscountryname_element = addresses.find('countryName')
#         data['AddressCountryName'].append(addresscountryname_element.text if addresscountryname_element is not None else '')
#         # data['AddressCountryName'].append(addresses.find('countryName').text)
#         #check  'postal code' elemnt exists before accessing 'text'
#         postal_code_element = addresses.find('postalCode')
#         data['PostalCode'].append(postal_code_element.text if postal_code_element is not None else '')
#         # data['PostalCode'].append(addresses.find('postalCode').text)
#     else:
#         # If 'addresses' element is not present, fill address-related fields with empty strings
#         for key in ['City', 'State', 'StateName', 'Country', 'CountryName', 'Address1',
#                     'AddressCity', 'AddressState', 'AddressStateName', 'AddressCountry',
#                     'AddressCountryName', 'PostalCode']:
#             data[key].append('')

# # Check the lengths of all lists in the 'data' dictionary
# lengths = set(len(value) for value in data.values())

# # Ensure all lists have the same length
# if len(lengths) == 1:
#     # Create a DataFrame from the data
#     df = pd.DataFrame(data)
    
#     # Save the DataFrame to an Excel file
#     df.to_excel('accuity.xlsx', index=False)
# else:
#     print("Error: All lists must be of the same length.")
# # Save the DataFrame to an Excel file
# # df.to_excel('accuity.xlsx', index=False)

# xml_file_path = r"D:\primeaccuityScreening\ac_UPIDGWL1\ENTITY.XML"
# excel_file_path = "output/accuityfile.xlsx"


# import xml.etree.ElementTree as ET
# from openpyxl import Workbook

# def parse_xml(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#     return root

# def create_excel_from_xml(xml_file, excel_file):
#     root = parse_xml(xml_file)

#     # Create Excel workbook and sheet
#     wb = Workbook()
#     ws = wb.active

#     # Write header row with element tags as column headers
#     header_row = ["Element"]
#     for element in root.iter():
#         for attr, value in element.attrib.items():
#             header = f"{element.tag}_{attr}"
#             if header not in header_row:
#                 header_row.append(header)
#     ws.append(header_row)

#     # Iterate through XML elements and write data to Excel
#     for element in root.iter():
#         row_data = [element.tag]
#         for attr, value in element.attrib.items():
#             header = f"{element.tag}_{attr}"
#             row_data.append(value)
#         ws.append(row_data)

#     # Save the Excel file
#     wb.save(excel_file)

# if __name__ == "__main__":
#     xml_file_path = r"D:\primeaccuityScreening\ac_UPIDGWL1\ENTITY.XML"
#     excel_file_path = "output/accuityfile.xlsx"


#     create_excel_from_xml(xml_file_path, excel_file_path)



import pandas as pd
import xml.etree.ElementTree as ET
xml_file = r"D:\primeaccuityScreening\ac_UPIDGWL1\ENTITY.XML"
# Parse the XML data
root = ET.parse(xml_file) 

# Create empty lists to store data
entity_data = []
columns = ['id', 'name', 'listId', 'listCode', 'entityType', 'createdDate', 'lastUpdateDate', 'source', 'OriginalSource','dobs','Alias','OtherID','NATIONAL NO', 'pob','title', 'OtherInformation', 'DirectID', 'EntityLevel', 'NameSource','Org_PID','Gender', 'OriginalID','Relationship', 'SubCategory','address1', 'city', 'state', 'stateName', 'country', 'countryName','province','postalCode']

# Extract data from XML and append to the entity_data list
for entity in root.findall('./entities/entity'):
    entity_dict = {}
    entity_dict['id'] = entity.get('id')
    entity_dict['name'] = entity.find('name').text
    entity_dict['listId'] = entity.find('listId').text
    entity_dict['listCode'] = entity.find('listCode').text
    entity_dict['entityType'] = entity.find('entityType').text
    entity_dict['createdDate'] = entity.find('createdDate').text
    entity_dict['lastUpdateDate'] = entity.find('lastUpdateDate').text
    entity_dict['source'] = entity.find('source').text
    entity_dict['OriginalSource'] = entity.find('OriginalSource').text
    entity_dict['dobs'] = entity.find('dobs/dob').text if entity.find('dobs/dob') is not None else ''
    entity_dict['pob'] = entity.find('pobs/pob').text if entity.find('pobs/pob') is not None else ''

    aliases_element = entity.find('aliases/alias[@type="Alias"]')
    entity_dict['Alias'] = aliases_element.text if aliases_element is not None else ''
    # OtherID
    other_id_element = entity.find('ids/id[@type="OtherID"]')
    entity_dict['OtherID'] = other_id_element.text if other_id_element is not None else ''
    # entity_dcit['OtherID'] = entity.find('ids/id[@type="OtherID"]').text if entity.find('ids/id[@type = "OtherID"]') is not None else ''
    # NATIONAL NO
    national_no_element = entity.find('ids/id[@type="NATIONAL NO"]')
    entity_dict['NATIONAL NO'] = national_no_element.text if national_no_element is not None else ''
    # entity_dicts['NATIONAL NO'] = entity.find('ids/id[@type="NATIONAL NO"]').text if entity.find('ids/id[@type = "NATIONAL NO"]') is not None else ''
    entity_dict['title'] = entity.find('titles/title').text if entity.find('titles/title') is not None else ''
    entity_dict['OtherInformation'] = entity.find('sdfs/sdf[@name="OtherInformation"]').text if entity.find('sdfs/sdf[@name="OtherInformation"]') is not None else ''
    entity_dict['DirectID'] = entity.find('sdfs/sdf[@name="DirectID"]').text if entity.find('sdfs/sdf[@name="DirectID"]') is not None else ''
    entity_dict['EntityLevel'] = entity.find('sdfs/sdf[@name="EntityLevel"]').text if entity.find('sdfs/sdf[@name="EntityLevel"]') is not None else ''
    # entity_dict['EntityLevel'] = entity.find('sdfs/sdf[@name="EntityLevel"]').text if entity.find('sdfs/sdf[@name="EntityLevel"]') is not None else ''
    entity_dict['NameSource'] = entity.find('sdfs/sdf[@name="NameSource"]').text if entity.find('sdfs/sdf[@name="NameSource"]') is not None else ''
    entity_dict['Org_PID'] = entity.find('sdfs/sdf[@name="Org_PID"]').text if entity.find('sdfs/sdf[@name="Org_PID"]') is not None else ''
    entity_dict['Gender'] = entity.find('sdfs/sdf[@name="Gender"]').text if entity.find('sdfs/sdf[@name="Gender"]') is not None else ''
    entity_dict['OriginalID'] = entity.find('sdfs/sdf[@name="OriginalID"]').text if entity.find('sdfs/sdf[@name="OriginalID"]') is not None else ''
    entity_dict['Relationship'] = entity.find('sdfs/sdf[@name="Relationship"]').text if entity.find('sdfs/sdf[@name="Relationship"]') is not None else ''
    entity_dict['SubCategory'] = entity.find('sdfs/sdf[@name="SubCategory"]').text if entity.find('sdfs/sdf[@name="SubCategory"]') is not None else ''
    entity_dict['address1'] = entity.find('addresses/address/address1').text if entity.find('addresses/address/address1') is not None else ''
    entity_dict['city'] = entity.find('addresses/address/city').text if entity.find('addresses/address/city') is not None else ''
    entity_dict['state'] = entity.find('addresses/address/state').text if entity.find('addresses/address/state') is not None else ''
    entity_dict['stateName'] = entity.find('addresses/address/stateName').text if entity.find('addresses/address/stateName') is not None else ''
    entity_dict['country'] = entity.find('addresses/address/country').text if entity.find('addresses/address/country') is not None else ''
    entity_dict['countryName'] = entity.find('addresses/address/countryName').text if entity.find('addresses/address/countryName') is not None else ''
    entity_dict['province'] = entity.find('addresses/address/province').text if entity.find('addresses/address/province') is not None else ''
    entity_dict['postalCode'] = entity.find('addresses/address/postalCode').text if entity.find('addresses/address/postalCode') is not None else ''

    entity_data.append(entity_dict)


# Create DataFrame
df = pd.DataFrame(entity_data, columns=columns)
df.to_excel('accuity_data.xlsx',index=False)
# Display DataFrame
# print(df)
