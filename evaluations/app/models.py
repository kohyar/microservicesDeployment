from app import db
import logging as lg 





class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    description = db.Column(db.String(600), nullable = False)
    movie_id = db.Column(db.Integer, nullable = False)

    def __init__(self, description, movie_id):
        self.description = description 
        self.movie_id = movie_id

    def serialize(self):
        return {
            'id':self.id,
            'description': self.description,
            'movie_id': self.movie_id
        }
    def __repr__(self):
        return '<Movie id {}: \n Description {}: \n {}>'.format(self.movie_id, self.id, self.description)

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Evaluation("What a baaad movie!", 1))
    db.session.add(Evaluation("Fincher at his best!", 2))
    db.session.commit()
    lg.warning('Database initialized!')
