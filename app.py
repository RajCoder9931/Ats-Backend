from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.candidate_routes import candidate_bp
from routes.job_routes import job_bp

app = Flask(__name__)

# allow frontend
CORS(app)
# Api lists
app.register_blueprint(auth_bp)  # login and signup
app.register_blueprint(candidate_bp) # candidate create and fetech 
app.register_blueprint(job_bp) # create job and  fetech 

@app.route("/")
def health():
    return "Auth API Running ye dekh babbe"

if __name__ == "__main__":
    app.run(debug=True)
