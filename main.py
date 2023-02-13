from django.db import models

class Question(models.Model):
    question_id = models.IntegerField()
    title = models.CharField(max_length=500)
    creation_date = models.DateTimeField()
    link = models.URLField()
    tags = models.CharField(max_length=500)
    is_answered = models.BooleanField()
    view_count = models.IntegerField()
    answer_count = models.IntegerField()
    score = models.IntegerField()
