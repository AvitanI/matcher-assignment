from django.contrib import admin
from .models import Candidate, CandidateSkill, Job

admin.site.register(Candidate)
admin.site.register(CandidateSkill)
admin.site.register(Job)