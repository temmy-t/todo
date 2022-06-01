from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#creating an instance
app = Flask(__name__)

#database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/todoapp'

#to turn the deprecation warning off
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#webapp instance: Name of app goes in the bracket(not sure) 
db = SQLAlchemy(app)

#instantiating flask-migrate
migrate = Migrate(app, db)

#class maps to tables: Table is automatically given the lowercase name of the class
class Todo (db.Model):
    #used to specify a desired tablename
    __tablename__='todos' 
    #class attributes        
    id = db.Column(db.Integer, primary_key=True)        
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)

    #used to customize string return in debugging mode
    def __repr__(self):
        return f'<Todo ID: {self.id}, Descrption: {self.description}>'


@app.route('/todos/create', methods=['POST'])
def create_todo():   
   body={}
   error = False
   try: 
       description =  request.get_json()['description']
       todo = Todo(description=description)
       body['description'] = todo.description
       db.session.add(todo)
       db.session.commit()
   except:        
        error = True
        db.session.rollback()
        print(sys.exc_info())
   finally:
        db.session.close()           
        if  error == True:
            abort(400)
        else:            
            return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())






#This should always be at the bottom of the script 
if __name__=='__main__':
    app.debug = True
    app.run(host="0.0.0.0")