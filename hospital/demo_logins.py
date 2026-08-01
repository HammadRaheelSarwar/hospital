DEMO_LOGINS = {
    'patient@gmail.com': {
        'password': 'patient123',
        'role': 'patient',
    },
    'doctor@gmail.com': {
        'password': 'doctor123',
        'role': 'doctor',
    },
    'admin@gmail.com': {
        'password': 'admin123',
        'role': 'admin',
    },
}


def get_demo_login(username, password):
    account = DEMO_LOGINS.get(username)
    if account and account['password'] == password:
        return account['role']
    return None