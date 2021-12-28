import json
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django.test import TestCase
from .models import Candidate, Job, CandidateSkill
from .views import candidate_finder
from django.test.client import RequestFactory

class CadidateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Set jobs
        Job.objects.create(id=1, title="Software Developer", skill="Python")
        Job.objects.create(id=2, title="Backend Developer", skill="C#")
        Job.objects.create(id=3, title="Sourcer", skill="PowerPoint")
        Job.objects.create(id=4, title="Data Analyst", skill="SQL Server")
        Job.objects.create(id=5, title="Fullstack Developer", skill="NodeJS")

        # Set candidates
        Candidate.objects.create(id=1, title="Software Developer", first_name="Israel", last_name="Israeli", email="Israel@gmail.com")
        Candidate.objects.create(id=2, title="Software Engineer", first_name="Moshe", last_name="Cohen", email="Moshe@gmail.com")
        Candidate.objects.create(id=3, title="Talent Sourcer", first_name="Gilad", last_name="Erlich", email="Gilad@gmail.com")
        Candidate.objects.create(id=4, title="Senior Developer", first_name="Ariel", last_name="Somech", email="Ariel@gmail.com")

        # Set candidates skills
        CandidateSkill.objects.create(candidate=Candidate.objects.get(id=1), name="Python")
        CandidateSkill.objects.create(candidate=Candidate.objects.get(id=1), name="C++")
        CandidateSkill.objects.create(candidate=Candidate.objects.get(id=2), name="C#")
        CandidateSkill.objects.create(candidate=Candidate.objects.get(id=3), name="Excel")
        CandidateSkill.objects.create(candidate=Candidate.objects.get(id=4), name="NodeJS")

    def test_bad_request_when_job_id_is_invalid(self):
        # Arrange
        job_id = 0
        request = self.factory.get(f'/candidate/job/{job_id}/')

        # Act
        response = candidate_finder(request, job_id)

        # Assert
        self.assertTrue(response.status_code == HttpResponseBadRequest.status_code, 'invalid job id')

    def test_job_id_not_found_when_id_not_stored_in_db(self):
        # Arrange
        job_id = 999
        request = self.factory.get(f'/candidate/job/{job_id}/')

        # Act
        response = candidate_finder(request, job_id)

        # Assert
        self.assertTrue(response.status_code == HttpResponseNotFound.status_code, 'job id not found')

    def test_empty_response_when_matching_candidate_to_job_not_exists(self):
        # Arrange
        job_id = 4
        request = self.factory.get(f'/candidate/job/{job_id}/')

        # Act
        response = candidate_finder(request, job_id)

        # Assert
        self.assertTrue(response.status_code == 200)
        self.assertEqual(response.content, b'{}', 'couldn\'t found matched candiadte for job')

    def test_get_candiadte_with_the_exact_title(self):
        # Arrange
        job_id = 1
        request = self.factory.get(f'/candidate/job/{job_id}/')

        # Act
        response = candidate_finder(request, job_id)

        # Assert
        self.assertTrue(response.status_code == 200)
        
        req_body = json.loads(response.content)
        self.assertEqual(req_body['id'], 1)

    def test_get_candiadte_with_partly_title(self):
        # Arrange
        job_id = 2
        request = self.factory.get(f'/candidate/job/{job_id}/')

        # Act
        response = candidate_finder(request, job_id)
        
        # Assert
        self.assertTrue(response.status_code == 200)

        req_body = json.loads(response.content)
        self.assertEqual(req_body['id'], 1)

    def test_get_candiadte_with_matched_skill(self):
        # Arrange
        job_id = 5
        request = self.factory.get(f'/candidate/job/{job_id}/')

        # Act
        response = candidate_finder(request, job_id)
        
        # Assert
        self.assertTrue(response.status_code == 200)

        req_body = json.loads(response.content)
        self.assertEqual(req_body['id'], 4)