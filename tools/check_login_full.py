import sys, os
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from project import create_app


def main():
    app = create_app()
    with app.test_client() as c:
        # GET forgot-password page
        r = c.get('/forgot-password')
        print('/forgot-password GET ->', r.status_code)

        # POST forgot-password
        r = c.post('/forgot-password', data={'email': 'test@example.com'}, follow_redirects=True)
        print('/forgot-password POST ->', r.status_code)
        print('  final path:', r.request.path)
        print('  contains login?', 'Login' in r.get_data(as_text=True))


if __name__ == '__main__':
    main()
