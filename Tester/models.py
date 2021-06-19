from django.db import models


class User(models.Model):
    userEmail = models.EmailField(primary_key=True, max_length=50)
    userName = models.CharField(max_length=50)
    userPassword = models.CharField(max_length=50)


class Test(models.Model):
    code = models.IntegerField(primary_key=True)
    testName = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    questionPaper = models.FileField()
    author = models.CharField(max_length=50)
    date = models.DateField()
    totalMarks = models.IntegerField(default=0)


class CreatedTests(models.Model):
    userEmail = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('userEmail', 'code'),)


class CompletedTests(models.Model):
    userEmail = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Test, on_delete=models.CASCADE)
    marksObtained = models.IntegerField()

    class Meta:
        unique_together = (('userEmail', 'code'),)


class Result(models.Model):
    code = models.ForeignKey(Test, on_delete=models.CASCADE)
    userEmail = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=0)
    totalMarks = models.IntegerField(default=0)


"""
class UserTestMapping(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    action = models.CharField()


class Result(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)

"""
