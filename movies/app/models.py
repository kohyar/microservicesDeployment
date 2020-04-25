from app import db
import logging as lg 





class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(200), nullable = False)
    year = db.Column(db.Integer, nullable = False)

    def __init__(self, name, year):
        self.name = name 
        self.year = year

    def serialize(self):
        return {
            'id':self.id,
            'name': self.name,
            'year': self.year
        }
    def __repr__(self):
        return '<Movie {}, year {}>'.format(self.name, self.year)

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Movie("Fight club", 1999))
    db.session.add(Movie("The social network", 2010))
    db.session.commit()
    lg.warning('Database initialized!')
