#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
from oauth2app.authenticate import Authenticator, AuthenticationException
from .forms import AuthorizeForm, InfoForm
from oauth2app.models import Client, AccessToken, Code
from .models import Router
from base64 import b64encode
from django.contrib.auth.forms import UserCreationForm
import time

def router(request): 
    if request.method == 'POST': 
	return redirect('http://' + request.POST.get('gateway') + '/cgi-bin/luci/oauth/genkey?token=' + token[0].token)
    template ={}
    return render_to_response(
        'router.html',
        template,
        RequestContext(request))

@login_required
def profile(request): 
    template = {
	'user': request.user.email, 
	'router': Router.objects.filter(user=request.user)}
    return render_to_response(
	'registration/profile.html', 
	template, 
	RequestContext(request))

@login_required
def cont_register(request): 
    if request.method == 'POST':
	info_form = InfoForm(data=request.POST)
        if info_form.is_valid():
	    user = request.user
	    if not Router.objects.filter(user=user).count() > 0: 
	        router = Router.objects.create(user=user)
	    else: 
	        router = Router.objects.get(user=user)
	    vars = ('isp', 'location', 'service_type', 'service_plan', 'drate', 'urate')
	    for i in vars: 
	        router.__setattr__(i, request.REQUEST.get(i))
	    router.save()
	    return HttpResponseRedirect("/oauth2/authorize?redirect_uri=http%3A%2F%2Fregister.projectbismark.net%2Fclient%2F&response_type=code")
    else:
        info_form = InfoForm()
    context = { 'info_form':info_form, 'user':request.user }
    
    return render_to_response('registration/cont_register.html', context, context_instance=RequestContext(request))


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
    return authorizer.grant_redirect()

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
        return HttpResponseRedirect('/router/')
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
    username = authenticator.user.email
    return HttpResponse(content="good token %s" % username)
