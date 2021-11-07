from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# You have all fields from AbstractUser source code
class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    # Need to make migrations after adding these

# User can create an account with only one profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# .Model is a python class in side the models file
# Here, a database table called Lead is created with three
# columns, first name, last name, age.

class Lead(models.Model):
    # First value is what is stored in dB, second value is what is displayed
    """
    This is what can be done (this is for the 'source variable below')
    SOURCE_CHOICES = (
        ('YouTube', 'YouTube'),
        ('Google', 'Google'),
        ('Newsletter', 'Newsletter'),
    )
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    # The "" around Agent tells Django to search w/in same file
    # in order to find the class "Agent"
    # ForeignKeys always need to be passed the on_delete argument

    # CASCADE means if agent is deleted, the lead will be deleted
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    # SET_NULL means ForeignKey will be set to null
    # agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True)

    # SET_DEFAULT will give a defalut value (Frank) if lead is deleted
    # agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, default="Frank")
    """ These show other different fields that can be used
        We will not use these, but these are the available options
    phoned = models.BooleanField(default=False)
    source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

    profile_picture = models.ImageField(blank=True, null=True)
    special_files = models.FileField(blank=True, null=True)
    """

    def __str__(self):
        # This syntax is for python 'f string'
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    #OnetoOneField allows you to associate once user to one agent
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ForeignKey allows multiple agents to link to the same organization
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # You don't need first name and last name b/c it is associated
    # with the AbstractUser command
    #first_name = models.CharField(max_length=20)
    #last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30) # New, Contacted, Converted, Unconverted
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# **kwargs = keyword arguments
def post_user_created_signal(sender, instance, created, **kwargs):
    print(sender, instance, created)
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
