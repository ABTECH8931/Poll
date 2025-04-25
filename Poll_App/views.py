from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from . models import Question, Choice
from django.views import View
from . forms import QuestionForm

# Create your views here.
#Home View
def home_view(request):
    question_list = Question.objects.all().order_by('-pub_date')
    return render(request, 'Poll_App/home.html', {'question_list': question_list})

#Detail view
def detail_view(request, question_id):
    question = get_object_or_404(Question.objects.prefetch_related('choice_set'), pk=question_id)
    
    if question.pub_date > timezone.now():
        messages.warning(request, "This poll is not yet available")
        return redirect('Poll_App:home')
    
    context = {
        'question': question,
        'choices': question.choice_set.all(),
        'total_votes': sum(c.votes for c in question.choice_set.all()),
    }
    return render(request, 'Poll_App/detail.html', context)

#Results View
def results_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = { 'question': question }

    return render(request, 'Poll_App/results.html', context)

#Vote View
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
        messages.success(request, "Vote recorded successfully!")
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a valid choice")
    return redirect('Poll_App:detail', question_id=question.id)

#Create View
def question_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            
            for i in range(1, 5):
                choice_text = request.POST.get(f'choice{i}')
                if choice_text:
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        votes=0
                    )
            
            messages.success(request, "Poll created successfully!")
            return redirect('Poll_App:home')
        else:
            messages.error(request, f"Form errors: {form.errors}")
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'Poll_App/create.html', context)

#Update View
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method != 'POST':
        form = QuestionForm(instance=question)
        context = {
            'form': form,
            'question': question,
            'existing_choices': question.choice_set.all(),
            'choice_count': question.choice_set.count()
        }
        return render(request, 'Poll_App/update.html', context)

    form = QuestionForm(request.POST, instance=question)
    if not form.is_valid():
        context = {
            'form': form,
            'question': question,
            'existing_choices': question.choice_set.all(),
            'choice_count': question.choice_set.count()
        }
        return render(request, 'Poll_App/update.html', context)
        
    form.save()

    for choice in question.choice_set.all():
        if choice_text := request.POST.get(f'choice_{choice.id}'):
            choice.choice_text = choice_text
            choice.save()
        else:
            choice.delete()

    for i in range(1, 5): 
        if new_choice := request.POST.get(f'new_choice_{i}'):
            Choice.objects.create(
                question=question,
                choice_text=new_choice,
                votes=0
            )

    messages.success(request, "Poll updated successfully!")
    return redirect('Poll_App:home')


#Delete View
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question deleted successfully!")
        return redirect('Poll_App:home')
    context = {'question': question}
    return render(request, 'Poll_App/delete.html', context)
