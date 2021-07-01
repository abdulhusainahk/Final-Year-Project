from django.contrib import admin
from Tester.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Test)
admin.site.register(CreatedTests)
admin.site.register(CompletedTests)
admin.site.register(Result)