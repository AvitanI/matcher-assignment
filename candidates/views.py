from django.http.response import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from .serializers import CandidateSerializer
from .models import Candidate, Job
from rest_framework.decorators import api_view
from django.db.models import Q
from functools import reduce
from django.db.models import Case, When, IntegerField
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_swagger import renderers
from rest_framework.decorators import api_view, renderer_classes

@api_view(['GET'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def candidate_finder(request, job_id):
    """ Finds candidate for a specific job """

    try:
        # Validate job id
        if job_id <= 0:
            return HttpResponseBadRequest(f'Invalid job id: {job_id}')

        # Find job by id
        try:
            job = Job.objects.get(pk=job_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound(f'Job not found for job id: {job_id}')

        # Filter relevant jobs
        splitted_job_title = job.title.split(" ")
        candidates = Candidate.objects.all().filter(Q(title__iexact=job.title) | reduce(lambda x, y: x | y, [Q(title__contains=word) for word in splitted_job_title]))

        # Order by matching skill + select the first candidate
        candidate = candidates.annotate(has_matching_skill=Case(When(Q(candidateskill__name__contains=job.skill), then=1), default=0, output_field=IntegerField())).order_by('-has_matching_skill').first()

        # Validate candidate
        if candidate is None:
            return JsonResponse({})

        # Serialize candidate object
        serializer = CandidateSerializer(candidate, many=False)

        return JsonResponse(serializer.data, safe=False)
    except Exception:
        # TO-DO: Write to log
        # logger.log_error(...)

        return HttpResponseServerError('Something went wrong...')