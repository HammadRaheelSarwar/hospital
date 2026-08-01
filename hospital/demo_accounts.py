from hospital.models import User, Patient
from doctor.models import Doctor_Information
from hospital_admin.models import Admin_Information


DEMO_ACCOUNTS = [
    {
        'username': 'patient@gmail.com',
        'password': 'patient123',
        'flags': {'is_patient': True},
        'profile_model': Patient,
        'profile_defaults': {},
    },
    {
        'username': 'doctor@gmail.com',
        'password': 'doctor123',
        'flags': {'is_doctor': True},
        'profile_model': Doctor_Information,
        'profile_defaults': {'register_status': 'Accepted'},
    },
    {
        'username': 'admin@gmail.com',
        'password': 'admin123',
        'flags': {'is_hospital_admin': True},
        'profile_model': Admin_Information,
        'profile_defaults': {'role': 'hospital'},
    },
]


def ensure_demo_accounts():
    for account in DEMO_ACCOUNTS:
        user, created = User.objects.get_or_create(
            username=account['username'],
            defaults={
                'email': account['username'],
                **account['flags'],
            },
        )

        changed = created
        if user.email != account['username']:
            user.email = account['username']
            changed = True

        for field_name, field_value in account['flags'].items():
            if getattr(user, field_name) != field_value:
                setattr(user, field_name, field_value)
                changed = True

        if changed:
            user.set_password(account['password'])
            user.save()

        profile_defaults = {'user': user, **account['profile_defaults']}
        profile_model = account['profile_model']

        profile, profile_created = profile_model.objects.get_or_create(
            user=user,
            defaults=profile_defaults,
        )

        profile_changed = profile_created
        for field_name, field_value in account['profile_defaults'].items():
            if getattr(profile, field_name) != field_value:
                setattr(profile, field_name, field_value)
                profile_changed = True

        if profile_changed:
            profile.save()