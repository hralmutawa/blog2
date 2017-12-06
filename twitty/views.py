from django.shortcuts import render

#twitter api takes client token, client id, client secret
# Create your views here.
from urllib.parse import quote
import requests
from django.http import JsonResponse
from allauth.socialaccount.admin import SocialApp
from requests_oauthlib import OAuth1 #importing the OAuth library to use it

def tweet_search(request): #access API Endpoint to get all tweets with #Python
	search_term = "#Python"
	query = quote(search_term) #quotify the query from the quote library
	#url = "https://api.twitter.com/1.1/search/tweets.json?q=%23freebandnames&since_id=24012619984051000&max_id=250126199840518145&result_type=mixed&count=4"
	url = "https://api.twitter.com/1.1/search/tweets.json?q=%s"%(query)

	user = request.user;
	social_account = user.socialaccount_set.get(user = user) #get the social account #many social accounts to user. social account objects related to user. We want one with the id = user.id (one that is currently logged in)
	social_token = social_account.socialtoken_set.get(account=social_account.id) # each social account has token. get me one from the social account.
	token = social_token.token #token also has secret
	token_secret = social_token.token_secret

	social_app = SocialApp.objects.get(provider=social_account.provider) #get the social apps
	client_id = social_app.client_id
	client_secret = social_app.secret

	auth_value = OAuth1(client_id, client_secret, token, token_secret) #takes all these values and combines them into authentication string

	resp = requests.get(url, auth = auth_value)

	return JsonResponse(resp.json(), safe=False)
