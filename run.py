from project import create_app

# Create the Flask app using your factory
app = create_app()

if __name__ == "__main__":
    # Enable debug mode so changes reload automatically
    app.run(debug=True, host="127.0.0.1", port=5000)
