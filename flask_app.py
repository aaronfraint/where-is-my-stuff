
# A very simple Flask Hello World app for you to get started with...

from my_stuff import create_app, db

app = create_app()


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
