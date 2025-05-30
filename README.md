# OpenAI RAG DBQA
A minimal Flask web app for document-based question answering (DBQA) over uploaded PDFs, using retrieval-augmented generation (RAG) powered by OpenAI's Responses and GPT-4o-mini. Automate information search by uploading your PDF documents, asking questions about their content, and receiving natural language responses from an LLM.

## Features
- **PDF Upload**: Drag and drop or select PDF files to upload them to an OpenAI vector store.
- **Contextualized Question Answering**: Submit questions and receive responses from the LLM based on information found in your submitted files.
- **OpenAI Platform Integration**: Uses the Responses, GPT-4o-mini, and Vector Store APIs.
- **Modern UI**: Built with Tailwind CSS.

## Technologies Used
This app was built using:
- **OpenAI Python SDK** to communicate with the OpenAI API for file uploads, vector store management, and LLM querying.
- **Flask** as a lightweight backend framework to support routing and API endpoints.
- **Tailwind CSS** for responsive, modern UI styling.

## Setup Instructions
### 1. Clone the Repository
```
git clone https://github.com/eddysfc/openai-rag-dbqa.git
cd openai-rag-dbqa
```

### 2. Install Python Dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. (Optional) Install Node.js Dependencies
>This is only needed if you want to rebuild the Tailwind CSS.
```
npm ci
```

### 4. Create `.env` File
Inside, add the following:
```
OPENAI_API_KEY=
VECTOR_STORE_ID=
```
Get your API key from OpenAI and save in `OPENAI_API_KEY`.

Leave `VECTOR_STORE_ID`, it will be created on the first run and saved to `.env`.

### 5. Run the App
```
flask run
```
or
```
python app.py
```
On your browser, visit the IP address shown in the Python terminal (default `http://localhost:5000`).

(Optional) If you made changes to the Tailwind CSS styling, open a new terminal and run
```
npm run dev
```
to rebuild and view your changes.

## How to Use
1. Drag and drop or select a PDF to upload.
2. Click the upload button and be patient while the file is processed. Check the upload status for success.
3. Type your question into the text box and submit.
4. Wait a bit while the LLM thinks. Once it's done, your contextualized answer will appear below!

## Notes
- This project is for prototyping purposes only.
- All uploaded files are saved to the `uploads/` directory, as well as saved in your OpenAI vector store.
- The first time you run the app, a new vector store will be created if none is present. The ID will be stored in your `.env` file.

## License
This project is open-source and available for modification and improvement by the community.
