from django.db import models

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

class CandidateSkill(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    skill = models.CharField(max_length=50)