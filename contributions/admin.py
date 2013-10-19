from django.contrib import admin
from contributions.models import Prop, Campaign, Committee, Contribution

admin.site.register(Prop)
admin.site.register(Campaign)
admin.site.register(Committee)
admin.site.register(Contribution)