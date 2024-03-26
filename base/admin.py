from django.contrib import admin
from .models import *
# Register your models here.
models = [model for name, model in locals().items() if isinstance(model, type) and issubclass(model, models.Model)]
for model in models:
    if model != Hotel or model != Image:
        admin.site.register(model)
