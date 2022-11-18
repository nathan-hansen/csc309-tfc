from django.contrib import admin
from subscriptions.models import SubscriptionPlan, CurrentSubscription

admin.site.register(SubscriptionPlan)
admin.site.register(CurrentSubscription)
