from flask import Flask, request, render_template

from wtform_fields import *

# Configuracion de app
app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return"Great success!"
        
    return render_template("index.html", form=reg_form)


if __name__ == "__main__":

    app.run(debug=True)