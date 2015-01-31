from django.contrib import admin
from models import UserProfile, job, Category, Skill

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(job)
admin.site.register(Category)
admin.site.register(Skill)
