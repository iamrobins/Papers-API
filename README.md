# Papers API

### Features
- POST /papers: Creates a new sample paper from JSON input (validated by your Pydantic
models). Returns the created paper's ID.
- GET /papers/{paper_id}: Retrieves a sample paper by ID. Returns the JSON representation and cached the response in Redis.
- PUT /papers/{paper_id}: Updates an existing sample paper (partial updates supported).
- DELETE /papers/{paper_id}: Deletes a sample paper.

- POST /extract/pdf: Accepts a PDF file upload. Uses Gemini to extract information and convert it
to the sample paper JSON format.

- POST /extract/text: Accepts plain text input. Uses Gemini to extract information and convert it to
the sample paper JSON format.

- GET /tasks/{task_id}: Checks the status of a PDF extraction task.

### Additional Features
- JWT Authentication (Private Routes Protection)
- Rate Limiting (10req/m)
- Celery for Asynchronous tasks
- Search Functionality: Full-text search capabilities on the question and answer fields.
- Postman API Docs

## Test Data
- Test Data is available in /seed folder

## Example .env
```bash
MONGO_URI=mongodb://localhost:27017/papers?authSource=admin
JWT_SECRET=secret
OOGLE_VERTEX_AI_PROJECT="supple-nature-438705-m6"
GOOGLE_VERTEX_AI_LOCATION="europe-west2"
GOOGLE_APPLICATION_CREDENTIALS="/path/your-service-account-file.json"
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### Setup Instructions
- Download Docker https://www.docker.com
- Execute these cmds inside project root directory

```bash
- docker compose up
- pip install -r requirements.txt
- fastapi dev main.py
- celery -A worker worker --loglevel=info
```

### Note
- You need to register an account in order to use the API.
- Your bearer auth token will be valid for 1 day
- API Examples are available in Postman Collection