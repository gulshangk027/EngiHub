"""
EngiHub Flask Application Factory
"""
from flask import Flask
from app.config import Config


def create_app():
    app = Flask(
        __name__,
        template_folder="../app/templates",
        static_folder="../static",
    )
    app.config.from_object(Config)

    # Register blueprints
    from app.routes.main       import main_bp
    from app.routes.doubt_solver import doubt_bp
    from app.routes.career     import career_bp
    from app.routes.internships import internship_bp
    from app.routes.research   import research_bp
    from app.routes.interview  import interview_bp
    from app.routes.placement  import placement_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(doubt_bp,     url_prefix="/doubt")
    app.register_blueprint(career_bp,    url_prefix="/career")
    app.register_blueprint(internship_bp, url_prefix="/internships")
    app.register_blueprint(research_bp,  url_prefix="/research")
    app.register_blueprint(interview_bp, url_prefix="/interview")
    app.register_blueprint(placement_bp, url_prefix="/placement")

    return app
