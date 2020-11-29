from flask import Flask, request, render_template

from wtform_registro import *

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = Registro()
    if reg_form.validate_on_submit():
        return "Registro completado"
    return render_template("index.html", form=reg_form)
        

if __name__ == "__main__":

    app.run(debug=True)