from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from kudos.models import Organization, User, Kudo
import random
from datetime import datetime, timedelta
import uuid

class Command(BaseCommand):
    help = 'Generates demo data for the Kudos application'

    def handle(self, *args, **options):
        # Create organizations
        org1 = Organization.objects.create(name="TechCorp")
        org2 = Organization.objects.create(name="DesignHub")

        # Sample messages
        messages = [
            "Great job on the project!",
            "Your presentation was amazing!",
            "Thanks for helping me out!",
            "You're a rockstar!",
            "Impressive work this week!",
            "Your attention to detail is fantastic!",
            "Thanks for going above and beyond!",
        ]

        # Create users for each organization
        orgs = [org1, org2]
        users = {}

        for org in orgs:
            for i in range(1, 6):  # 5 users per org
                username = f"user{i}_{org.name.lower()}"
                user = User.objects.create(
                    username=username,
                    password=make_password("password123"),
                    organization=org,
                    remaining_kudos=random.randint(0, 3)
                )
                users[user.id] = user

        # Create kudos between users
        user_ids = list(users.keys())
        for _ in range(20):  # Create 20 random kudos
            from_user = users[random.choice(user_ids)]
            to_user = users[random.choice(user_ids)]
            
            # Ensure users are in same org and not giving to themselves
            while (to_user.organization != from_user.organization or 
                   to_user == from_user):
                to_user = users[random.choice(user_ids)]
            
            # Random date in the past 30 days
            created_at = datetime.now() - timedelta(days=random.randint(0, 30))
            
            Kudo.objects.create(
                from_user=from_user,
                to_user=to_user,
                message=random.choice(messages),
                created_at=created_at
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated demo data'))