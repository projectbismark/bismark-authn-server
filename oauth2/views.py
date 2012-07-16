#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
from oauth2app.authenticate import Authenticator, AuthenticationException
from .forms import AuthorizeForm
from oauth2app.models import Client, AccessToken, Code
from oauth2.models import Router
from base64 import b64encode
from django.contrib.auth.forms import UserCreationForm
import time

@login_required
def profile(request): 
    template = {
	'user': request.user, 
	'router': Router.objects.filter(user=request.user)[0]}
    return render_to_response(
	'registration/profile.html', 
	template, 
	RequestContext(request))

@login_required
def cont_register(request): 
    template = {
        'user': request.user}
    if request.method == 'GET':
        return render_to_response(
	    'registration/cont_register.html', 
	    template, 
	    RequestContext(request))
    elif request.method == 'POST':
	user = request.user
	if not Router.objects.filter(user=user).count() > 0: 
	    router = Router.objects.create(user=user)
	vars = ('isp', 'location', 'service_type', 'service_plan', 'drate', 'urate')
	for i in vars: 
	    router.__setattr__(i, request.REQUEST.get(i))
	router.save()
	return HttpResponseRedirect("/oauth2/authorize?redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fclient%2F&response_type=code")
    return HttpResponseRedirect("/register/")

@login_required
def missing_redirect_uri(request):
    return render_to_response(
        'oauth2/missing_redirect_uri.html', 
        {}, 
        RequestContext(request))


@login_required
def authorize(request):
    authorizer = Authorizer()
    try:
        authorizer.validate(request)
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically 
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    #if request.method == 'GET':
        # Make sure the authorizer has validated before requesting the client
        # or access_ranges as otherwise they will be None.
	#template = {
            #"client":authorizer.client, 
            #"access_ranges":authorizer.access_ranges, 
	    #"form_action":'/oauth2/authorize?%s' % authorizer.query_string}
        #template["form"] = AuthorizeForm()
        #helper = FormHelper()
        #yes_submit = Submit('connect', 'Click to Continue')
        #helper.add_input(yes_submit)
        #helper.form_action = '/oauth2/authorize?%s' % authorizer.query_string
        #helper.form_method = 'POST'
        #template["helper"] = helper
        #return render_to_response(
            #'oauth2/authorize.html', 
            #template, 
            #RequestContext(request))
    #elif request.method == 'POST':
        #form = AuthorizeForm(request.POST)
        #if form.is_valid():
    return authorizer.grant_redirect()
    #return HttpResponseRedirect("/")

@login_required
def client(request):
    client = Client.objects.get(user=request.user)
    token = AccessToken.objects.filter(client=client).select_related().order_by("expire").reverse()
    template = {
        "client":client,
        "basic_auth":"Basic %s" % b64encode(client.key + ":" + client.secret),
        "code":Code.objects.filter(client=client).select_related().order_by("expire").reverse(),
        "access_tokens":AccessToken.objects.filter(client=client).select_related()}
    template["error_description"] = request.GET.get("error_description")
    if AccessToken.objects.filter(client=client).select_related().count() > 0 and token[0].expire > time.time():
        return redirect('http://myrouter.projectbismark.net/cgi-bin/luci/oauth/genkey?token=' + token[0].token)
    else:
	return render_to_response(
            'oauth2/client.html',
            template,
            RequestContext(request))

def check(request):
    authenticator = Authenticator()
    try:
        # Validate the request.
        authenticator.validate(request)
    except AuthenticationException:
        # Return an error response.
        return authenticator.error_response(content="You didn't authenticate.")
    username = authenticator.user.username
    return HttpResponse(content="good token %s" % username)
