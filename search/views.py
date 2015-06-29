# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Document
import subprocess


class SearchForm(forms.Form):
    docfile = forms.FileField(required=False)
    search_by = forms.CharField(initial='sift')
    search_limit = forms.CharField(initial='10')
    distance_model = forms.CharField(initial='euclidean')


def index(request):
    # Handle file upload
    context = {}
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                newdoc = Document(docfile=request.FILES['docfile'])
                newdoc.save()
                query = str(newdoc.docfile)
            except:
                query = str(Document.objects.all().order_by('-id')[0].docfile)
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
