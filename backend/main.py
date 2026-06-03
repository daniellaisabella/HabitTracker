import os
from flask import Flask
from backend.api.habit_routes import habit_blueprint
from backend.api.habit_log_routes import habit_log_blueprint
from backend.error_handlers import register_error_handlers
from backend.db import init_pool, create_tables

###### opretter flask instans og registrerer blueprints, error handlers og database forbindelse ######
app = Flask(__name__) 
app.register_blueprint(habit_blueprint) 
app.register_blueprint(habit_log_blueprint)

init_pool() #åbner én fælles forbindelse til db
create_tables() # create tables hvis de ik findes i db 

register_error_handlers(app)

# kør kun appen hvis denne er main. python sætter den til main når den køres direkte i terminal i Docker container 
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false") == "true", host="0.0.0.0", port=5000)