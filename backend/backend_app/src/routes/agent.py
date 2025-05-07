import os
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models.user import db
from ..models.agent import Agent, KnowledgeBase
from openai import OpenAI, OpenAIError
from openai import OpenAI, OpenAIError

agent_bp = Blueprint("agent", __name__)

# Removed global client initialization
# client = OpenAI() --- Agent Routes --- #

@agent_bp.route("/agents", methods=["POST"])
@login_required
def create_agent():
    data = request.get_json()
    name = data.get("name")
    prompt = data.get("prompt") # Simplified prompt for MVP

    if not name or not prompt:
        return jsonify({"message": "Nome e prompt do agente são obrigatórios"}), 400

    new_agent = Agent(name=name, prompt=prompt, owner=current_user)
    db.session.add(new_agent)
    db.session.commit()

    return jsonify({"message": "Agente criado com sucesso", "agent_id": new_agent.id}), 201

@agent_bp.route("/agents", methods=["GET"])
@login_required
def get_agents():
    agents = Agent.query.filter_by(user_id=current_user.id).all()
    agent_list = [
        {"id": agent.id, "name": agent.name, "prompt": agent.prompt}
        for agent in agents
    ]
    return jsonify(agent_list), 200

@agent_bp.route("/agents/<int:agent_id>", methods=["GET"])
@login_required
def get_agent(agent_id):
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first()
    if not agent:
        return jsonify({"message": "Agente não encontrado ou não autorizado"}), 404
    return jsonify({"id": agent.id, "name": agent.name, "prompt": agent.prompt}), 200

@agent_bp.route("/agents/<int:agent_id>", methods=["PUT"])
@login_required
def update_agent(agent_id):
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first()
    if not agent:
        return jsonify({"message": "Agente não encontrado ou não autorizado"}), 404

    data = request.get_json()
    agent.name = data.get("name", agent.name)
    agent.prompt = data.get("prompt", agent.prompt)
    db.session.commit()
    return jsonify({"message": "Agente atualizado com sucesso"}), 200

@agent_bp.route("/agents/<int:agent_id>", methods=["DELETE"])
@login_required
def delete_agent(agent_id):
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first()
    if not agent:
        return jsonify({"message": "Agente não encontrado ou não autorizado"}), 404

    db.session.delete(agent)
    db.session.commit()
    return jsonify({"message": "Agente excluído com sucesso"}), 200

# --- Knowledge Base Routes (Basic MVP) --- #

@agent_bp.route("/agents/<int:agent_id>/knowledge", methods=["POST"])
@login_required
def add_knowledge(agent_id):
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first()
    if not agent:
        return jsonify({"message": "Agente não encontrado ou não autorizado"}), 404

    data = request.get_json()
    kb_type = data.get("type", "text") # Default to text for MVP
    content = data.get("content")

    if kb_type == "text" and content:
        new_kb = KnowledgeBase(type=kb_type, content=content, agent_id=agent_id)
        db.session.add(new_kb)
        db.session.commit()
        return jsonify({"message": "Base de conhecimento adicionada com sucesso", "kb_id": new_kb.id}), 201
    # Add handling for file uploads later
    else:
        return jsonify({"message": "Tipo ou conteúdo inválido para base de conhecimento"}), 400

@agent_bp.route("/agents/<int:agent_id>/knowledge", methods=["GET"])
@login_required
def get_knowledge(agent_id):
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first()
    if not agent:
        return jsonify({"message": "Agente não encontrado ou não autorizado"}), 404

    kbs = KnowledgeBase.query.filter_by(agent_id=agent_id).all()
    kb_list = [
        {"id": kb.id, "type": kb.type, "content_preview": (kb.content[:50] + '...') if kb.content else None, "file_path": kb.file_path}
        for kb in kbs
    ]
    return jsonify(kb_list), 200

@agent_bp.route("/knowledge/<int:kb_id>", methods=["DELETE"])
@login_required
def delete_knowledge(kb_id):
    kb = KnowledgeBase.query.get(kb_id)
    if not kb:
        return jsonify({"message": "Base de conhecimento não encontrada"}), 404

    # Verify ownership through the agent
    agent = Agent.query.filter_by(id=kb.agent_id, user_id=current_user.id).first()
    if not agent:
        return jsonify({"message": "Não autorizado a excluir esta base de conhecimento"}), 403

    db.session.delete(kb)
    db.session.commit()
    return jsonify({"message": "Base de conhecimento excluída com sucesso"}), 200

# --- Chat Route (MVP) --- #

@agent_bp.route("/agents/<int:agent_id>/chat", methods=["POST"])
@login_required
def chat_with_agent(agent_id):
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first()
    if not agent:
        return jsonify({"message": "Agente não encontrado ou não autorizado"}), 404

    data = request.get_json()
    user_query = data.get("query")
    if not user_query:
        return jsonify({"message": "Consulta do usuário é obrigatória"}), 400

    # Basic RAG: Retrieve knowledge base content (simplified for MVP)
    knowledge_content = ""
    kbs = KnowledgeBase.query.filter_by(agent_id=agent_id).all()
    for kb in kbs:
        if kb.content:
            knowledge_content += kb.content + "\n\n" # Simple concatenation
        # Add file content retrieval later

    # Construct the prompt for the LLM
    system_prompt = agent.prompt
    context_prompt = f"Use a seguinte informação de base de conhecimento para responder à consulta do usuário:\n{knowledge_content}"
    full_prompt = f"{system_prompt}\n\n{context_prompt}\n\nConsulta do Usuário: {user_query}"

    try:
        # Initialize client within the route
        # This requires OPENAI_API_KEY env var to be set when this route is called
        client = OpenAI()
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or another suitable model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context_prompt}\n\nConsulta: {user_query}"} # Combine context and query for user role
            ]
        )
        llm_response = response.choices[0].message.content
        return jsonify({"response": llm_response}), 200

    except Exception as e:
        print(f"Erro ao chamar a API OpenAI: {e}") # Log the error
        # Check for specific API key error
        if "api key" in str(e).lower():
             return jsonify({"message": "Erro de configuração: Chave da API OpenAI não encontrada ou inválida."}), 500
        return jsonify({"message": "Erro ao processar a solicitação com o LLM"}), 500

