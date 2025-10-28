from flask import render_template
from project import create_app

app = create_app()
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/', methods=['GET'])
def Home():
    print(">>> HOME ROUTE REACHED <<<")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

