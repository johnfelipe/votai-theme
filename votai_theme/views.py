from elections.views import SoulMateDetailView
from votai_theme.calculator import YQSCalculator
from django.http import JsonResponse
from candidator.models import TakenPosition


class MediaNaranjaView(SoulMateDetailView):
    calculator_class = YQSCalculator


class MedianaranjaJsonView(MediaNaranjaView):
    def dispatch(self, *args, **kwargs):
        super(MedianaranjaJsonView, self).dispatch(*args, **kwargs)
        election = self.object
        response = {
            'election_id': election.id,
            "election_name": election.name,
            "district": election.area.name,
            "level": election.extra_info['nivel'],
            "post": election.extra_info['cargo'],
            "categories": [],
            "candidates": []

        }
        for category in election.categories.all():
            category_dict = {'category_id': category.id,
                             'name': category.name,
                             'questions': []
                             }
            for topic in category.topics.all():
                question_dict = {"question_id": topic.id,
                                 "question_text": topic.label,
                                 "answers": []
                                 }
                for position in topic.positions.all():
                    position_dict = {"answer_id": position.id,
                                     "answer_text": position.label,
                                     "answer_value": position.answervalue.value
                                     }
                    question_dict['answers'].append(position_dict)
                category_dict['questions'].append(question_dict)
            response['categories'].append(category_dict)
        for candidate in election.candidates.all():
            candidate_dict = {'candidate_id': candidate.id,
                              'candidate_name': candidate.name,
                              'candidate_pic': candidate.image,
                              'positions': []
                              }
            taken_positions = TakenPosition.objects.filter(position__topic__category__in=election.categories.all(), person=candidate)
            for taken_position in taken_positions:
                taken_position_dict = {'question_id': taken_position.topic.id,
                                       'answer_id': taken_position.position.id
                                       }
                candidate_dict['positions'].append(taken_position_dict)
            response['candidates'].append(candidate_dict)
        return JsonResponse(response)
