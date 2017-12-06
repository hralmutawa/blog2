from django.shortcuts import render
from django.http import JsonResponse
import requests #making requests

# Create your views here.
def member_list(request): #making an API request
	user = request.user;
	social_account = user.socialaccount_set.get(user = user) #get the social account #many social accounts to user. social account objects related to user. We want one with the id = user.id (one that is currently logged in)
	social_token = social_account.socialtoken_set.get(account=social_account.id) # each social account has token. get me one from the social account.
	token = social_token.token # get back the token field from the object
	#url = "https://api.github.com/orgs/joinCODED/members" 
	# url = “https://api.github.com/user/DarthHamzrepos”
	url = "https://api.github.com/user/repos"
	response = requests.get(url, headers={"Authorization": "token " + token}) #headers is many ways to pass parameters to url. Pass the auth key. Takes the token that you are giving it.
	return JsonResponse(response.json(), safe=False)


