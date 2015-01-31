from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    userType = models.CharField(max_length=30)
    

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username



class Category(models.Model):
    category_string = models.CharField(max_length=100) #The name of the category

class job(models.Model):
    user = models.ForeignKey(User) #Which user posted the job
    title = models.CharField(max_length=100) #Title of job
    job_descr = models.CharField(max_length=500) #Description of the job
    deadline_date = models.DateField() # The date by which the job has to be completed
    job_duration = models.CharField(max_length=50) #A string describing the duration of the job
    posted_timestamp = models.DateTimeField() #Time that the job was posted
    category = models.ForeignKey(Category) #The category of job this is
    # skills = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title



class Skill(models.Model):
    skill_string = models.CharField(max_length=30) #The name of the skill
    user = models.ForeignKey(User) #The user who has this skill
    job = models.ForeignKey(job) # The job which requires this skill
    user.null=True
    job.null=True




    
    
