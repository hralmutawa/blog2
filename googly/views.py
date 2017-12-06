from django.http import JsonResponse
import requests
from django.shortcuts import render


# Create your views here.

def place_text_search(request):
	key = "AIzaSyC0l34lf47XCZKSu-TuHsszibWzd6nnMQM"
	query= request.GET.get('query', 'coded')
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s&region=kw"%(query, key)

	next_page = request.GET.get('nextpage')
	if next_page is not None:
		url += "&pagetoken="+next_page

	response = requests.get(url)
	context = {"response":response.json()}
	return render(request, 'search.html', context)
	#return JsonResponse(response.json(),safe=False) #return the response in JSON format


def place_detail(request):
	key = "AIzaSyC0l34lf47XCZKSu-TuHsszibWzd6nnMQM"
	place_id = request.GET.get('place_id', '') #get the place ID. get is from the form
	url = "https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s"%(key, place_id)

	map_key = "AIzaSyBNC7btXkp81ZnuV7qdwMbZp9Y8sTLa-uc"


	response = requests.get(url)
	context = {"response": response.json(), "map": map_key}
	return render(request, 'search_detail.html', context)

