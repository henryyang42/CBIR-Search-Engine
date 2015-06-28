# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Document
import subprocess


class SearchForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )
    search_by = forms.ChoiceField((('sift', 'SIFT'), ('color', 'Color')))
    search_limit = forms.ChoiceField(
        (('10', '10'), ('20', '20'), ('50', '50')))
    distance_model = forms.ChoiceField((('euclidean', 'euclidean'), ('hamming', 'hamming'), ('cosine', 'cosine')))  # noqa


def index(request):
    # Handle file upload
    context = {}
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            query = str(newdoc.docfile)
            limit = form.cleaned_data['search_limit']
            search_method = form.cleaned_data['search_by']
            distance_model = form.cleaned_data['distance_model']
            if search_method == 'sift':
                results = subprocess.Popen('python sift_feature/search.py -v sift_feature/vocabulary.npy -i sift_feature/index.csv -q media/%s -l %s -d %s' % (query, limit, distance_model), shell=True, stdout=subprocess.PIPE).stdout.read()  # noqa
            else:
                results = subprocess.Popen('python color_feature/search.py -i color_feature/index.csv -q media/%s -l %s -d %s' % (query, limit, distance_model), shell=True, stdout=subprocess.PIPE).stdout.read()  # noqa
            print results
            context['results'] = results.split('\n')[:-1]
            context['query'] = query

    else:
        form = SearchForm()  # A empty, unbound form

    context['form'] = form
    # Render list page with the documents and the form
    return render_to_response(
        'index.html',
        context,
        context_instance=RequestContext(request)
    )
