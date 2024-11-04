from decouple import config
from flask import jsonify

from config import create_app
from db import db

# from models.user import *
# from models.category import *
# from models.enums import *
# from models.recipe import *


environment = config("CONFIG_ENV")
app = create_app(environment)


@app.teardown_request
def commit_transaction_on_teardown(exception=None):
    if exception is None:
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            return (
                jsonify(
                    {
                        "error": "An error occurred while saving data. Please try again later"
                    }
                ),
                500,
            )
    else:
        db.session.rollback()

        return (
            jsonify(
                {
                    "error": "An unexpected error occurred. Please contact support if the issue persists"
                }
            ),
            500,
        )


@app.teardown_appcontext
def shutdown_session(response, exception=None):
    db.session.remove()
    return response


if __name__ == "__main__":
    app.run(debug=True)
