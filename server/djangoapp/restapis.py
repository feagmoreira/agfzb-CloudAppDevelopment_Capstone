import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if "api_key" in kwargs:
        try:
            api_key = kwargs["api_key"]
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            # Call get method of requests library with URL and parameters
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        except:
            # If any error occurs
            print("Network exception occurred")
    else:
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in a dealer object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL and dealerId parameters
    json_result = get_request(url, id=dealer_id)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Get its content in a review object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   review=review_doc["review"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"], id=review_doc["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
  sentiment = ""
  url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1b237cde-3875-4199-a65b-4aada03d00fc/v1/analyze"
  api_key = "mbbcv0x8SzZ5KlPMDuSVZQA5rz_5EMIlRjm1okQGNZJY"
  version = '2022-04-07'
  features = {"sentiment":{}}
  return_analyzed_text = Truerl, api_key=api_key, version=version, features = features, return_analyzed_text = return_analyzed_text)
  if json_result:
))(_
  _        # Get label value
    sentiment= json_result["sentiment"]["target"][0]["label"]   

  return sentiment



