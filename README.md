# Matcher Assignment
### _Author: Idan Avitan_

API for matching candidates to jobs

## Stack

- Windows 10
- VS Code 1.63
- Python 3.10.1
- Django Framework 4.0
- Django Rest Framework 3.13.1
- sqlite3
- Django Rest Swagger 2.2.0

## How To Use
Install packages
`pip install -r requirements.txt`

Run Server
`python manage.py runserver`

Run Tests
`python manage.py test`

API
`http://127.0.0.1:8000/candidate/job/1/`

Swagger
`http://127.0.0.1:8000/swagger-ui/`

Admin UI
`http://127.0.0.1:8000/admin/candidates/`

## DB Schema
```sh
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
```

#### Sharing some thoughts about DB Schema
- At first, I wanted to create a skills table with a unique value for each skill and then use skill id as a foreign key in the 'CandidateSkill' and 'Job' tables. Since we talked at the interview that some values can be written in different ways (e.g., JavaScrpit or JS), I've chosen to store it as a simple string.
- Another way to store data is in a document model (like MongoDB), where the candidate skills are stored as a list for each record.
- the skill field at the 'Job' table should be stored as one-to-many relation since the job can be composed of multiple skills.
- We can add more fields to tables to make it easier to filter records or produce reports. For example, we can add Phone, CompanyId, AddressId to 'Candidate'. Add level to 'CandidateSkill'. Add CompanyId, Salary to 'Job' etc.
- Besides the PK indexes, which are auto-created, we can add indexes to titles/names or add text search indexes to tables.

## Improvements
- The endpoint should call to service rather than writing the business logic inside the action, so other endpoints/services can use it + it will be more testable.
- Following the first improvement, we should write the services in Clean Architecture as microservice.
- The endpoint should return a generic response (shared to all endpoints) instead of returning different responses.
- Instead of using 'try/catch', maybe we can create a global exception handler that returns some generic response, write error to log, etc.
- We should implement some authentication when sending requests to the API.
- We should cache jobs instead of a call to the DB.
- At the moment, we fetch all records, but what if we have a million records? We should add more filters when finding candidates such as CompanyId, location, etc.
- The skill finding works the same as the job title finding works. A better way is to work with mappings or AI models to ensure specific skills like 'JS' or 'JavaScript' are the same.
- Another improvement to find candidates is to process each candidate once it is created and add some classifications to search according to these classifications.
