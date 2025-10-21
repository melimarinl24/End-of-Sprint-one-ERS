import sys
import os

# Ensure repo root is on sys.path so 'project' can be imported when running the script
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from project import create_app


def main():
    app = create_app()
    with app.test_request_context():
        rules = sorted([(r.rule, r.endpoint, ','.join(sorted(r.methods))) for r in app.url_map.iter_rules()], key=lambda x: x[0])
        for rule, endpoint, methods in rules:
            print(f"{rule} -> {endpoint} [{methods}]")


if __name__ == '__main__':
    main()
