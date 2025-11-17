from flask import Flask, jsonify
from routes.users import users_bp
from routes.products import products_bp
from routes.interactions import interactions_bp
from routes.recommend import recommend_bp
import sentry_sdk
import time
from flask import request

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0
)



app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})


@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_response_time(response):
    if hasattr(request, "start_time"):
        duration = round(time.time() - request.start_time, 4)
        print(f"[API LOG] {request.method} {request.path} took {duration}s")
    return response


# register routes
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(interactions_bp)
app.register_blueprint(recommend_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
