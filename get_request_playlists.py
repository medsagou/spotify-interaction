# token = {
#   "access_token": "BQDBKJ5eo5jxbtpWjVOj7ryS84khybFpP_lTqzV7uV-T_m0cTfwvdn5BnBSKPxKgEb11",
#   "token_type": "Bearer",
#   "expires_in": 3600
# }
token = 'BQCjM80ee31kXJx5eZuWZdVjhTQFduVXJnwqqCkPJQHYaXG9ONnZ9oGPJaS-gc5eMtvIB_1sqRi_abL5X-S_Pk5kperccR2amtT3r_yJmjYi6poq5ICIGWLZOiunXcr2NCUpeyFTIBqyxHMatWufQc7iZMEP5UCV6Dcu5umBZaNHDDAiPGrYy1x5KcUV1gW0cP51YkmDQE_71DjW4UnR5eqwEe-HD1-F6KF4Ly4m0Z41h8bCpbQOzqXbb0EWOtbvLuoTinBzNW8oMLmRfWM2bnJUKE88yyYlbFY'
import requests
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get("https://api.spotify.com/v1/me/tracks?limit=50", headers=headers)

print(response.json())