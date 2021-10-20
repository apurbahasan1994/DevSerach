from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profile/user-default')
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=True)

    def __str__(self):
        return self.name if self.name else ''


class Skill(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=True)

    def __str__(self):
        return self.name if self.name else ''


class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=200, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=True)

    def __str__(self):
        return self.title if self.title else ''

    @property
    def voteCount(self):
        reviews = self.review_set.all()
        upvotes = reviews.filter(vote='up').count()
        totalVotes = reviews.count()
        ratio = (upvotes/totalVotes)*100
        self.vote_ratio = ratio
        self.vote_total = totalVotes
        self.save()

    @property
    def reviwers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        queryset = [str(x)for x in queryset]
        return queryset


class Review(models.Model):
    VOTE_TYPE = (
        ('up', "Up vote"), ('down', 'Down Vote')
    )
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    vote = models.CharField(max_length=200, choices=VOTE_TYPE, default='up')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=True)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.vote


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=True)

    def __str__(self):
        return self.subject
