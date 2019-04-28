from flask import Flask
app = Flask(_name_)
 
@app.route("/")
def hello():
    return "Welcome to Python Flask!"
 
if _name_ == "_main_":
    app.run()