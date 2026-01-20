from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.candidate_routes import candidate_bp
from routes.job_routes import job_bp
from routes.interview_routes import interview_bp    
from routes.company_routes import company_bp
from routes.user_routes import user_bp
from routes.dashboard_routes import dashboard_bp
from routes.pipeline_routes import pipeline_bp
from routes.notification_routes import notification_bp
from routes.lead_routes import lead_bp
from routes.candidate_auth_routes import candidate_auth_bp
from routes.candidate_self_routes import candidate_self_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(candidate_bp)
app.register_blueprint(job_bp)
app.register_blueprint(interview_bp)    
app.register_blueprint(company_bp)
app.register_blueprint(user_bp) 
app.register_blueprint(dashboard_bp)
app.register_blueprint(pipeline_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(lead_bp)
app.register_blueprint(candidate_auth_bp)
app.register_blueprint(candidate_self_bp)
@app.route("/")
def health():
    return "Auth API Running ye dekh babbe"

if __name__ == "__main__":
    app.run(debug=True)


