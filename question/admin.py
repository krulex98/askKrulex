from django.contrib import admin
from .models import *

# Register your models here.

admin.register(User)
admin.register(Question)
admin.register(Tag)
admin.register(Answer)
