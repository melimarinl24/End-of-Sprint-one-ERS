import sys, os
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from project import create_app

ENDPOINTS = ['/', '/signup/student', '/student/signup', '/login', '/signup/faculty', '/forgot-password']


def short(s, n=200):
    if not s:
        return ''
    return (s[:n] + '...') if len(s) > n else s


def main():
    app = create_app()
    with app.test_client() as c:
        for ep in ENDPOINTS:
            resp = c.get(ep)
            loc = resp.headers.get('Location')
            print(f"{ep} -> {resp.status_code} {resp.status}")
            if loc:
                print(f"  Location: {loc}")
            data = resp.get_data(as_text=True)
            print('  Body preview:', short(data.replace('\n', ' '), 300))
            print()


if __name__ == '__main__':
    main()
