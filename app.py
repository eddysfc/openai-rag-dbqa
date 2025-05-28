import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv, set_key
from openai import OpenAI

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def create_vector_store(name="new_vector_store"):
    vector_store = client.vector_stores.create(name=name)
    details = {
        "id": vector_store.id,
        "name": vector_store.name,
        "created_at": vector_store.created_at,
        "file_count": vector_store.file_counts.completed
    }
    print("Vector store created:", details)
    return details

VECTOR_STORE_ID = os.environ["VECTOR_STORE_ID"]
if not VECTOR_STORE_ID:
    print("No vector store id found, creating new")
    VECTOR_STORE_ID = create_vector_store()["id"]
    set_key(".env", "VECTOR_STORE_ID", VECTOR_STORE_ID)
else:
    print("Using vector store", VECTOR_STORE_ID)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return jsonify(success=False, error='No "pdf" file field in request.'), 400

    f = request.files["pdf"]
    if f.filename == "":
        return jsonify(success=False, error="Invalid file name."), 400

    local_path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
    try:
        f.save(local_path)
    except Exception as e:
        return jsonify(success=False, error=f"Could not save file: {e}"), 500

    try:
        file_response = client.files.create(file=open(local_path, "rb"), purpose="assistants")
        client.vector_stores.files.create(
            vector_store_id=VECTOR_STORE_ID,
            file_id=file_response.id
        )
        print(file_response.id)
    except Exception as e:
        return jsonify(success=False, error=f"OpenAI error: {e}"), 500

    return jsonify(success=True, filename=f.filename), 200

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question", "").strip()
    if not question:
        return jsonify(success=False, error="No question provided."), 400

    try:
        response = client.responses.create(
            input=question,
            model="gpt-4o-mini",
            tools=[{
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
            }]
        )

        answer = response.output[1].content[0].text
        return jsonify(success=True, answer=answer), 200

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)