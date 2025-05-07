from .user import db # Import db from user model to avoid circular imports

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prompt = db.Column(db.Text, nullable=False) # Simplified prompt for MVP
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Add other agent fields as needed (persona details, LLM config - later phases)
    knowledge_bases = db.relationship("KnowledgeBase", backref="agent", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Agent {self.name}>"

class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False) # e.g., "text", "pdf", "url"
    content = db.Column(db.Text, nullable=True) # For direct text input
    file_path = db.Column(db.String(255), nullable=True) # For uploaded files
    agent_id = db.Column(db.Integer, db.ForeignKey("agent.id"), nullable=False)

    def __repr__(self):
        return f"<KnowledgeBase {self.id} for Agent {self.agent_id}>"

