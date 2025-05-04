from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from kudos.models import Organization, User, Kudo
import random
from datetime import datetime, timedelta
from django.utils import timezone
from faker import Faker  # For more realistic fake data

class Command(BaseCommand):
    help = 'Generates demo data for the Kudos application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users per organization (default: 5)'
        )
        parser.add_argument(
            '--kudos',
            type=int,
            default=20,
            help='Number of kudos to generate (default: 20)'
        )

    def handle(self, *args, **options):
        fake = Faker()
        
        # Clear existing data (optional)
        if input("Clear existing data? (y/n): ").lower() == 'y':
            Kudo.objects.all().delete()
            User.objects.all().delete()
            Organization.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        # Create organizations
        org_names = ["TechCorp", "DesignHub", "MarketingPros", "FinanceTeam"]
        orgs = [Organization.objects.create(name=name) for name in org_names[:2]]
        self.stdout.write(self.style.SUCCESS(f'Created {len(orgs)} organizations'))

        # Sample messages with more variety
        messages = [
            "Great job on the project! Your hard work really paid off.",
            "That presentation was outstanding - clear, concise, and compelling!",
            "Thanks for helping me debug that tricky issue. You saved the day!",
            "Your attention to detail on this report was fantastic!",
            "The creative solution you proposed was brilliant!",
            "Thanks for mentoring the new team members - they're learning so much!",
            "Your positive attitude makes the whole team more productive!",
            "The extra hours you put in didn't go unnoticed. Thank you!",
            "You handled that difficult client situation perfectly!",
            "Your code review comments were incredibly helpful and thorough!",
        ]

        # Create users for each organization
        users_per_org = options['users']
        users = {}
        
        for org in orgs:
            for i in range(1, users_per_org + 1):
                username = f"user{i}_{org.name.lower().replace(' ', '')}"
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = f"{first_name.lower()}.{last_name.lower()}@{org.name.lower()}.com"
                
                user = User.objects.create(
                    username=username,
                    password=make_password("password123"),
                    organization=org,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    remaining_kudos=random.randint(0, 3),
                    last_kudo_reset=timezone.now() - timedelta(days=random.randint(0, 6)))
                users[user.id] = user

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        # Create kudos between users
        kudos_count = options['kudos']
        user_ids = list(users.keys())
        
        for _ in range(kudos_count):
            from_user = users[random.choice(user_ids)]
            to_user = users[random.choice(user_ids)]
            
            # Ensure users are in same org and not giving to themselves
            while (to_user.organization != from_user.organization or 
                   to_user == from_user):
                to_user = users[random.choice(user_ids)]
            
            # Random date in the past 30 days
            created_at = timezone.now() - timedelta(days=random.randint(0, 30))
            
            Kudo.objects.create(
                from_user=from_user,
                to_user=to_user,
                message=random.choice(messages),
                created_at=created_at
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {kudos_count} kudos'))
        self.stdout.write(f"Superuser credentials: username=admin, password=admin123")



