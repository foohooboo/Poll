from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.db.models import F

#python function that represents the view accessed by a URL (a page and/or a task?)
def index(request):
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	latest_question_list = get_list_or_404(Question.objects.order_by('pub_date')[:5])
	#same thing as below statements, can skip importing render and httpresponse
	return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})
	#template = loader.get_template('polls/index.html')
	#context = {
	#	'latest_question_list': latest_question_list,
	#}
	#return HttpResponse(template.render(context, request))


def detail(request, question_id):
	#return HttpResponse("You're looking at question %s." % question_id)
	#using get_object_or_404 shortcut
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})
	#baby steps way
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404("Question does not exist")
	#return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
	#
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#Redisplay the voting form
		return render(request, 'polls/detail.html', {
		'question':question,
		'error_message': "You didn't select a choice.",
		})
	else:
		#lets try using django.db.models.F to "lock guard" our data
		selected_choice.votes = F('votes') + 1
		#selected_choice.votes += 1
		selected_choice.save()
		#Always return an HyypResponseRedirect after successfuly dealing with
		#POST data.  This prevents data from being posted twice if the user hits
		#the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

	#return HttpResponse("You're voting on question %s." % question_id)
