import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv, set_key
from openai import OpenAI

def create_app():

    # Load .env into environment
    load_dotenv()

    app = Flask(__name__)

    # Ensure upload directory exists
    app.config["UPLOAD_FOLDER"] = "uploads"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize OpenAI client
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from .env file.")
    client = OpenAI(api_key=openai_api_key)

    # Load or create vector store
    vector_store_id = os.getenv("VECTOR_STORE_ID") or create_vector_store(client)
    app.config["VECTOR_STORE_ID"] = vector_store_id

    # Register routes
    register_routes(app, client)
    return app

def create_vector_store(client, name="new_vector_store"):

    # Create a new OpenAI vector store and save its ID in .env
    vector_store = client.vector_stores.create(name=name)
    details = {
        "id": vector_store.id,
        "name": vector_store.name,
        "created_at": vector_store.created_at,
        "file_count": vector_store.file_counts.completed
    }
    print(f"Vector store created: {details}")
    set_key(".env", "VECTOR_STORE_ID", vector_store.id)

    # Export vector store ID
    return details["id"]

def register_routes(app, client):

    # Render the main interface
    @app.route("/")
    def index():
        return render_template("index.html")
    
    # Handle PDF uploads, save locally, then upload to OpenAI
    @app.route("/upload", methods=["POST"])
    def upload():

        # Validate upload
        if "pdf" not in request.files:
            return jsonify(success=False, error='No "pdf" file field in request.'), 400

        f = request.files["pdf"]
        if f.filename == "":
            return jsonify(success=False, error="Invalid file name."), 400

        # Save locally
        local_path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
        try:
            f.save(local_path)
        except Exception as e:
            return jsonify(success=False, error=f"Could not save file: {e}"), 500

        # Upload to OpenAI vector store
        try:
            file_response = client.files.create(file=open(local_path, "rb"), purpose="assistants")
            client.vector_stores.files.create(
                vector_store_id=app.config["VECTOR_STORE_ID"],
                file_id=file_response.id
            )
            print(file_response.id)
        except Exception as e:
            return jsonify(success=False, error=f"OpenAI error: {e}"), 500

        # Ok response
        return jsonify(success=True, filename=f.filename), 200

    # Handle question submission and RAG, send request to OpenAI API, return answer
    @app.route("/ask", methods=["POST"])
    def ask():
        question = request.form.get("question", "").strip()
        if not question:
            return jsonify(success=False, error="No question provided."), 400

        try:
            response = client.responses.create(
                input=question,
                model="gpt-4o-mini",    # Change model if wanted
                tools=[{
                    "type": "file_search",
                    "vector_store_ids": [app.config["VECTOR_STORE_ID"]],
                }]
            )
            
            # Return answer with ok response
            answer = response.output[1].content[0].text
            return jsonify(success=True, answer=answer), 200

        except Exception as e:
            return jsonify(success=False, error=str(e)), 500

if __name__ == "__main__":
    create_app().run(debug=True)    # Debug mode for development only