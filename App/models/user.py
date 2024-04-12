from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    desc = db.Column(db.String(5000), nullable=False)
    type = db.Column(db.String(256), nullable=False)  
    bodypart = db.Column(db.String(256), nullable=False)  
    equipment = db.Column(db.String(256), nullable=False)  
    level = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer)  
    rating_desc = db.Column(db.String(256)) 

    def get_json(self):  
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'type': self.type,
            'bodypart': self.bodypart,
            'equipment': self.equipment,
            'level': self.level,
            'rating': self.rating,
            'rating_desc': self.rating_desc
        }

class UserRoutine(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)  # Fixed ForeignKey spelling
    routine_name = db.Column(db.String(256), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_routines', lazy=True))

    def add_exercise(self, exercise_id):
        new_exercise = UserRoutine(exercise_id=exercise_id, routine_name=self.routine_name, user_id=self.user_id)
        db.session.add(new_exercise)
        db.session.commit()

    def remove_exercise(self, exercise_id):
        exercise_to_remove = UserRoutine.query.filter_by(exercise_id=exercise_id, routine_name=self.routine_name, user_id=self.user_id).first()
        if exercise_to_remove:
            db.session.delete(exercise_to_remove)
            db.session.commit()

    def clear_routine(self):
        exercises = UserRoutine.query.filter_by(routine_name=self.routine_name, user_id=self.user_id).all()
        for exercise in exercises:
            db.session.delete(exercise)
        db.session.commit()

    def get_exercises(self):
        exercises = UserRoutine.query.filter_by(routine_name=self.routine_name, user_id=self.user_id).all()
        return exercises

    def update_routine_name(self, new_name):
        self.routine_name = new_name
        db.session.commit()

    @staticmethod
    def get_user_routines(user_id):
        user_routines = UserRoutine.query.filter_by(user_id=user_id).all()
        return user_routines
