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


class CreatedTests(models.Model):
    userEmail = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Test, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('userEmail','code'),)


class CompletedTests(models.Model):
    userEmail = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Test, on_delete=models.CASCADE)
    marksObtained = models.IntegerField()
    class Meta:
        unique_together = (('userEmail','code'),)



"""
class UserTestMapping(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    action = models.CharField()


class Result(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)

"""
