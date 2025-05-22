from django.shortcuts import render

# Create your views here.
def survey_list(request):
    return render(request, 'survey/survey_list.html')

def survey_detail(request):
    return render(request, 'survey/survey_detail.html')