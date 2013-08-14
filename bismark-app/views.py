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

@login_required
def router(request): 
    """Page attempts to redirect and pass token to router url. 
	On GET emulates myrouter.projectbismark.net. On failure, user enters gateway into form which is handled by POST."""

    client = Client.objects.get(user=request.user)
    token = AccessToken.objects.filter(client=client).select_related().order_by("expire").reverse()
    if request.method == 'POST': 
	return redirect('http://' + request.POST.get('gateway') + '/cgi-bin/luci/oauth/genkey?token=' + token[0].token)
    template ={
	'token': token[0].token}
    return render_to_response(
        'oauth2/router.html',
        template,
        RequestContext(request))

@login_required
def profile(request): 
    """Generic profile page, contains navigation to edit profile and download
    token.  """
    template = {
	'user': request.user.email, 
	'router': Router.objects.filter(user=request.user)}
    return render_to_response(
	'registration/profile.html', 
	template, 
	RequestContext(request))

@login_required
def cont_register(request): 
    """Page contains router info form and creates user's router object. On submit begins OAuth protocol. """
    if request.method == 'POST':
	info_form = InfoForm(data=request.POST)
        if info_form.is_valid():
	    user = request.user
	    if not Router.objects.filter(user=user).count() > 0: 
	        router = Router.objects.create(user=user)
	    else: 
	        router = Router.objects.get(user=user)
	    vars = ('isp', 'service_type', 'service_plan', 'drate', 'urate', 'city', 'state', 'country', 'node_id')
	    for i in vars: 
	        router.__setattr__(i, request.REQUEST.get(i))
	    router.save()
	    return HttpResponseRedirect("/oauth2/authorize?redirect_uri=https%3A%2F%2Fregister.projectbismark.net%2Fclient%2F&response_type=code")
    else:
	if not Router.objects.filter(user=request.user).count() > 0:
            info_form = InfoForm()
	else: 
	    info_form = InfoForm(data=Router.objects.filter(user=request.user).values()[0])
    context = { 'info_form':info_form, 'user':request.user }
    return render_to_response('registration/cont_register.html', context, context_instance=RequestContext(request))


@login_required
def missing_redirect_uri(request):
    """Error page required by oauth2app. """
    return render_to_response(
        'oauth2/missing_redirect_uri.html', 
        {}, 
        RequestContext(request))


@login_required
def authorize(request):
    """Client authorize page (protocol ignored since there are no clients). For more information see oauth2app docs. http://oauth2app.readthedocs.org/en/latest/ """
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
    """Page sends token request if token does not exist, otherwise redirects to download token to router. """
    client = Client.objects.get(user=request.user)
    token = AccessToken.objects.filter(client=client).select_related().order_by("expire").reverse()
    template = {
        "client":client,
        "basic_auth":"Basic %s" % b64encode(client.key + ":" + client.secret),
        "code":Code.objects.filter(client=client).select_related().order_by("expire").reverse(),
        "access_tokens":AccessToken.objects.filter(client=client).select_related()}
    template["error_description"] = request.GET.get("error_description")
    if AccessToken.objects.filter(client=client).select_related().count() > 0 and token[0].expire > time.time():
        return HttpResponseRedirect('/router')
    else:
	return render_to_response(
            'oauth2/client.html',
            template,
            RequestContext(request))

def check(request):
    """"Page accessed by check script to verify router has token. """
    authenticator = Authenticator()
    try:
        # Validate the request.
        authenticator.validate(request)
    except AuthenticationException:
        # Return an error response.
        return authenticator.error_response(content="You didn't authenticate.")
    username = authenticator.user.email
    return HttpResponse(content="good token %s" % username)

def help(request):
    return render_to_response('registration/help.html', {}, RequestContext(request))
