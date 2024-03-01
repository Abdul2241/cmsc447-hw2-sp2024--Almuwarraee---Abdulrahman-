from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

   


@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    users = User.query.order_by(User.data_created).all()
    return render_template('index.html', users=users)


@app.route('/add', methods=['POST'])
def add_user():
    user_name = request.form['name']
    user_points = request.form['points']
    if user_name and user_points:  
        new_user = User(name=user_name, points=user_points)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except: 
            return "Erro when adding the user "
    else:
        return "Erro when adding the user"



@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Erro: when deleting the user the user "



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.points = request.form.get('points')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating the user: "
    else:
        return render_template('update.html', user=user)

    
@app.route('/search')
def search_user():
    query = request.args.get('search')
    if query:
        users = User.query.filter(User.name.contains(query)).order_by(User.data_created).all()
    else:
        users = User.query.order_by(User.data_created).all()
    return render_template('index.html', users=users)


if __name__ == "__main__":
    app.run(debug=True)
