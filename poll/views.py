from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from poll.models import Choice

from poll.models import Poll

# Create your views here.
class PollListView(ListView):
    model = Poll
    template_name = "poll/poll_list.html"
    context_object_name = "polls"

class PollDetailView(DetailView):
    model = Poll
    template_name = "poll/poll_detail.html"
    context_object_name = "poll"

class PollStartView(View):

    def get(self, request, pk):
        poll = get_object_or_404(
            Poll,
            pk=pk,
            is_active=True
        )

        questions = poll.questions.prefetch_related("choices").all()

        context = {
            "poll": poll,
            "questions": questions,
        }

        return render(
            request,
            "poll/poll_start.html",
            context
        )

    def post(self, request, pk):
        poll = get_object_or_404(
            Poll,
            pk=pk,
            is_active=True
        )

        questions = poll.questions.prefetch_related("choices").all()

        answers = {}

        for question in questions:
            choice_id = request.POST.get(
                f"question_{question.pk}"
            )

            if choice_id:
                answers[str(question.pk)] = int(choice_id)

        request.session["poll_answers"] = answers
        request.session["poll_id"] = poll.pk

        return redirect(
            "poll_result",
            pk=poll.pk
        )

class PollResultView(View): 
    def get(self, request, pk): 
        poll = get_object_or_404( Poll, pk=pk )
        answers = request.session.get( "poll_answers", {} )
        questions = poll.questions.prefetch_related("choices").all()
        correct_answers = 0
        total_questions = questions.count()
        results = []
        for question in questions:
            selected_choice_id = answers.get( str(question.pk) )
            selected_choice = None
            if selected_choice_id:
                selected_choice = question.choices.filter( pk=selected_choice_id ).first()
            correct_choice = question.choices.filter( is_correct=True ).first()
            is_correct = ( selected_choice is not None and selected_choice.is_correct )
            if is_correct:
                correct_answers += 1
            results.append({
                "question": question,
                "selected_choice": selected_choice,
                "correct_choice": correct_choice,
                "is_correct": is_correct,
            })
        percentage = 0
        if total_questions > 0:
            percentage = round( correct_answers / total_questions * 100 )
        context = {
            "poll": poll,
            "results": results,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "percentage": percentage,
        }
        return render( request, "poll/poll_result.html", context )

class PollQuestionView(View):

    def get(self, request):
        return render(
            request,
            "poll/poll_question.html"
        )

    def post(self, request):

        # Створюємо тест
        poll = Poll.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            created_by=request.user
        )

        # Знаходимо всі питання
        question_numbers = []

        for key in request.POST.keys():

            if key.startswith("question_"):

                number = key.replace("question_", "")

                if number.isdigit():
                    question_numbers.append(int(number))

        # Створюємо питання
        for number in sorted(question_numbers):

            question_text = request.POST.get(
                f"question_{number}"
            )

            if not question_text:
                continue

            question = poll.questions.create(
                text=question_text,
                question_type="multiple_choice",
                order=number
            )

            # Правильна відповідь
            correct_answer = request.POST.get(
                f"correct_{number}"
            )

            # Створюємо 4 варіанти
            for choice_number in range(1, 5):

                choice_text = request.POST.get(
                    f"choice_{number}_{choice_number}"
                )

                if not choice_text:
                    continue

                Choice.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=(
                        str(choice_number) == str(correct_answer)
                    )
                )

        return redirect("poll_detail", pk=poll.pk)
