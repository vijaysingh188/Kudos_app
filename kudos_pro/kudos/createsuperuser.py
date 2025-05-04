from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.exceptions import ValidationError
from kudos.models import Organization

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create a default organization if none exists
        org, created = Organization.objects.get_or_create(
            name="Default Organization",
            defaults={'name': "Default Organization"}
        )
        
        options['organization'] = org.id
        return super().handle(*args, **options)

    def get_input_data(self, field, message, default=None):
        val = super().get_input_data(field, message, default)
        if field == 'organization':
            while True:
                try:
                    org_id = input("Organization ID (default=1): ") or "1"
                    return Organization.objects.get(pk=org_id)
                except Organization.DoesNotExist:
                    self.stderr.write("Error: That organization doesn't exist.")
        return val