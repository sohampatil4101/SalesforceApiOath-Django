import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SalesforceToken
from django.conf import settings

from simple_salesforce import Salesforce

@login_required
def login_with_salesforce(request):
    salesforce_oauth_settings = {
        'consumer_key': settings.SALESFORCE_CLIENT_ID,
        'consumer_secret': settings.SALESFORCE_CLIENT_SECRET,
        'redirect_uri': settings.SALESFORCE_REDIRECT_URI,
    }
    
    oauth_url = f"https://login.salesforce.com/services/oauth2/authorize?client_id={salesforce_oauth_settings['consumer_key']}&redirect_uri={salesforce_oauth_settings['redirect_uri']}&response_type=code"

    return redirect(oauth_url)

@login_required
def welcome(request):
    if 'code' in request.GET:
        auth_code = request.GET['code']

        salesforce_oauth_settings = {
            'consumer_key': settings.SALESFORCE_CLIENT_ID,
            'consumer_secret': settings.SALESFORCE_CLIENT_SECRET,
            'redirect_uri': settings.SALESFORCE_REDIRECT_URI,
        }

        token_url = "https://login.salesforce.com/services/oauth2/token"

        token_data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': salesforce_oauth_settings['consumer_key'],
            'client_secret': salesforce_oauth_settings['consumer_secret'],
            'redirect_uri': salesforce_oauth_settings['redirect_uri'],
        }

        response = requests.post(token_url, data=token_data)

        if response.status_code == 200:
            token_info = response.json()

            access_token = token_info['access_token']
            refresh_token = token_info['refresh_token']
            instance_url = token_info['instance_url']

            user = request.user
            salesforce_token, created = SalesforceToken.objects.get_or_create(user=user)
            salesforce_token.access_token = access_token
            salesforce_token.refresh_token = refresh_token
            salesforce_token.instance_url = instance_url
            salesforce_token.save()

            print(f"Access Token: {access_token}")
            print(f"Refresh Token: {refresh_token}")
            print(f"Instance URL: {instance_url}")
            
            data = SalesforceToken( user = user, access_token = access_token, refresh_token = refresh_token, instance_url = instance_url )
            data.save()

    return render(request, 'welcome.html')




























# # start herefrom django.shortcuts import redirect
# from requests_oauthlib import OAuth2Session

# def salesforce_oauth(request):
#     sf_oauth = OAuth2Session(settings.SALESFORCE_CLIENT_ID, redirect_uri=settings.SALESFORCE_REDIRECT_URI)
    
#     # Generate the authorization URL
#     authorization_url, state = sf_oauth.authorization_url('https://login.salesforce.com/services/oauth2/authorize')
    
#     # Save the state to compare in the callback
#     request.session['oauth_state'] = state
    
#     # Redirect to the Salesforce authorization URL
#     print("refresh_token: ", authorization_url)
    
#     return redirect(authorization_url)


# def oauth_callback(request):

#     # Check the state to prevent CSRF attacks
#     if request.GET.get('state') != request.session.get('oauth_state'):
#         # Handle the error
#         return HttpResponse("CSRF Error: State does not match")

#     # Create an OAuth2Session with your Salesforce client ID
#     sf_oauth = OAuth2Session(settings.SALESFORCE_CLIENT_ID, redirect_uri=settings.SALESFORCE_REDIRECT_URI)
    
#     # Exchange the authorization code for an access token
#     token = sf_oauth.fetch_token(
#         'https://login.salesforce.com/services/oauth2/token',
#         code=request.GET['code'],
#         client_secret=settings.SALESFORCE_CLIENT_SECRET,
#     )

    
#     print("code", token)
    
#     access_token = token['access_token']
#     instance_url = token['instance_url']
    
#     print("soham is great")
#     print("Access Token:", access_token)
#     print("Instance URL:", instance_url)

#     # Store the access_token and instance_url in your database
#     # You can use Django models to create a table for storing this information
    
#     # Redirect to the "Welcome to Mavlon" page
    
#     return redirect('welcome_page')

# # end here

def home(request):
    return render(request, 'home.html')

# def welcome_page(request):
#     return render(request, 'welcome.html')