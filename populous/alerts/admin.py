from django.contrib import admin
from populous.alerts.models import Alert, Subscription

admin.site.register(Alert)
admin.site.register(Subscription)