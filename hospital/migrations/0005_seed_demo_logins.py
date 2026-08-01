from django.db import migrations


DEMO_ACCOUNTS = [
    {
        'username': 'patient@gmail.com',
        'password': 'patient123',
        'flags': {'is_patient': True},
        'profile_model': 'Patient',
    },
    {
        'username': 'doctor@gmail.com',
        'password': 'doctor123',
        'flags': {'is_doctor': True},
        'profile_model': 'Doctor_Information',
        'profile_fields': {'register_status': 'Accepted'},
    },
    {
        'username': 'admin@gmail.com',
        'password': 'admin123',
        'flags': {'is_hospital_admin': True},
        'profile_model': 'Admin_Information',
        'profile_fields': {'role': 'hospital'},
    },
]


def create_demo_accounts(apps, schema_editor):
    User = apps.get_model('hospital', 'User')
    Patient = apps.get_model('hospital', 'Patient')
    DoctorInformation = apps.get_model('doctor', 'Doctor_Information')
    AdminInformation = apps.get_model('hospital_admin', 'Admin_Information')

    profile_models = {
        'Patient': Patient,
        'Doctor_Information': DoctorInformation,
        'Admin_Information': AdminInformation,
    }

    for account in DEMO_ACCOUNTS:
        user, created = User.objects.get_or_create(
            username=account['username'],
            defaults={
                'email': account['username'],
                **account['flags'],
            },
        )

        updated = False
        for field_name, field_value in account['flags'].items():
            if getattr(user, field_name) != field_value:
                setattr(user, field_name, field_value)
                updated = True
        if user.email != account['username']:
            user.email = account['username']
            updated = True
        if created or updated:
            user.set_password(account['password'])
            user.save()

        profile_model = profile_models[account['profile_model']]
        profile_fields = account.get('profile_fields', {})
        profile_defaults = {'user': user, **profile_fields}

        if account['profile_model'] == 'Patient':
            profile_model.objects.get_or_create(user=user, defaults=profile_defaults)
        else:
            profile_model.objects.get_or_create(user=user, defaults=profile_defaults)


def remove_demo_accounts(apps, schema_editor):
    User = apps.get_model('hospital', 'User')
    usernames = [account['username'] for account in DEMO_ACCOUNTS]
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_alter_user_login_status'),
        ('doctor', '0044_appointment_message'),
        ('hospital_admin', '0005_admin_information_hospital'),
    ]

    operations = [
        migrations.RunPython(create_demo_accounts, reverse_code=remove_demo_accounts),
    ]