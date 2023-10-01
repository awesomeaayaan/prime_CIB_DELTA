# import hashlib
# import hmac
 
# key = 's6p7vJtUvRv5sz8JoBi7OHfW5klS0jxD'
# message = """<BulkOffLoading>
#     <SerialNumber>123</SerialNumber>
#     <RequestType>BulkOffLoading</RequestType>
# </BulkOffLoading>"""
 
# # Generate the hash.
# signature = hmac.new(
#     key,
#     message,
#     hashlib.sha256
# ).hexdigest()
# import hmac
# import hashlib

# # Your secret key
# secret_key = "s6p7vJtUvRv5sz8JoBi7OHfW5klS0jxD"  # Replace with your actual secret key

# # Data to be hashed
# data = """<BulkOffLoading>
#     <SerialNumber>123</SerialNumber>
#     <RequestType>BulkOffLoading</RequestType>
# </BulkOffLoading>"""

# # Encode the key and data as bytes (UTF-8 encoding)
# key_bytes = secret_key.encode('utf-8')
# data_bytes = data.encode('utf-8')

# # Create an HMAC SHA-256 hash object with the key
# sha256_hmac = hmac.new(key_bytes, data_bytes, hashlib.sha256)

# # Get the hexadecimal representation of the HMAC
# hashed_data = sha256_hmac.hexdigest()

# # Print the SHA-256 HMAC
# print("SHA-256 HMAC:", hashed_data)
# import requests
# import hashlib
# import hmac

# # Define the data in XML format
# xml_data = """
# <BulkOffLoading>
#     <SerialNumber>123</SerialNumber>
#     <RequestType>BulkOffLoading</RequestType>
# </BulkOffLoading>
# """

# # Your secret key
# secret_key = "CIBirkzbvwb"

# # Calculate the SHA-256 hash of the XML data
# key_bytes = secret_key.encode('utf-8')
# data_bytes = xml_data.encode('utf-8')
# sha256_hmac = hmac.new(key_bytes, data_bytes, hashlib.sha256)
# hashed_data = sha256_hmac.hexdigest()

# # API endpoint URL
# api_url = "https://backlist.cibnepal.org.np/api/v2/blacklist/bulk-offloading"  # Replace with your actual API endpoint

# # Create the headers for the request
# headers = {
#     "Content-Type": "application/xml",
#     "MerchantID": "CIBirkzbvwb",
#     "HASH":'e0c9aa7abbb690ef60e21f0b05c020ddcf7d75cf27c16e734e5e6155d0cfce10',
# }

# # Send the POST request with XML data and headers
# response = requests.post(api_url,headers==headers)

# # Check the response
# if response.status_code == 200:
#     print("Request was successful.")
#     print("Response:", response.text)
# else:
#     print(f"Request failed with status code {response.status_code}.")

import hmac
import hashlib

# Your secret key
secret_key = "s6p7vJtUvRv5sz8JoBi7OHfW5klS0jxD"  # Replace with your actual secret key

# Data to be hashed
data = """<BulkOffLoading>
    <SerialNumber>123</SerialNumber>
    <RequestType>BulkOffLoading</RequestType>
</BulkOffLoading>"""

# Encode the key and data as bytes (UTF-8 encoding)
key_bytes = secret_key.encode('utf-8')
data_bytes = data.encode('utf-8')

# Create an HMAC SHA-256 hash object with the key
sha256_hmac = hmac.new(key_bytes, data_bytes, hashlib.sha256)

# Get the hexadecimal representation of the HMAC
hashed_data = sha256_hmac.hexdigest()

# Print the SHA-256 HMAC
print("SHA-256 HMAC:", hashed_data)
