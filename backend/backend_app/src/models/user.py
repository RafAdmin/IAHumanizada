from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Add other user fields as needed (name, etc.)
    agents = db.relationship("Agent", backref="owner", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

# Placeholder for password hashing/checking methods
# def set_password(self, password):
#     self.password_hash = generate_password_hash(password)

# def check_password(self, password):
#     return check_password_hash(self.password_hash, password)

