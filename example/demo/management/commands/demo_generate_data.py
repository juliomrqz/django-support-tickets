# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import NoArgsCommand

from faker import Faker

from ...mommy_recipes import user
from ...utils import generate_fake_list


fake = Faker()
User = get_user_model()


class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        TOTAL_USERS = 10

        # Clean tables
        User.objects.all().delete()

        # Generate users
        users = {}
        fake_emails = generate_fake_list(fake.email, TOTAL_USERS)
        fake_usernames = generate_fake_list(fake.user_name, TOTAL_USERS)
        for i in range(TOTAL_USERS - 2):

            generated_user = user.make(
                first_name=fake.first_name(), last_name=fake.last_name(),
                email=fake_emails[i], username=fake_usernames[i],
                password=make_password(fake_usernames[i])
            )

            users[i] = generated_user

        # Generate static users
        admin_user = user.make(
            first_name=fake.first_name(), last_name=fake.last_name(),
            email='admin@example.com', username='admin',
            password=make_password('admin'), is_superuser=True, is_staff=True
        )
        users[TOTAL_USERS - 2] = admin_user

        demo_user = user.make(
            first_name=fake.first_name(), last_name=fake.last_name(),
            email='demo@example.com', username='demo',
            password=make_password('demo')
        )
        users[TOTAL_USERS - 1] = demo_user
