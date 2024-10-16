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
MONGO_URI="mongodb://localhost:27017/papers"
JWT_SECRET=secret
GOOGLE_APPLICATION_CREDENTIALS="supple-nature-438705-m6-dccafcea8974.json"
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Gemini Creds
```json
{
  "type": "service_account",
  "project_id": "supple-nature-438705-m6",
  "private_key_id": "dccafcea89744cbd77cd4c453d1b4a82651874bc",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDD1jaCeNmPsVAD\nPHSjE6zblsXH5cVQHk4xmzvGrltW1lwytMELiDBmOHp45PlOMT8vGlYBaWz9KC5p\nUJE1k101IijX/6r0Hnb0PpT73vkDXEztVkCIA0h96gvkqy9omN53N3RZ8KE1ch5W\nR/UR/cZEcIq93aWCaiXdzhLDtaOKkLPbPiNZhhU/twbkG3snmr3RQWLP63uvFSos\nvG1nG2Rdk90yUJPKYdFbvdjI+p2HCoOIrUpRl5NxEQxf0tZ6IDY7T+EGqKQXgMie\nSoFBrvVc+mzxDZbEkY2/K8KjDKxbvjrwGrlPTAay4dtLpy2SlBQFTfv10u6zMWD/\ncVNLhYIbAgMBAAECggEADj0b936L6vusYp/ZpyW+ErUyqicVoo6hhs/Pl9GDiJvL\nVlB4HLuJMVV36iRT0BCalHUova+JohpyzWtzM18EjuFt8M6BAoDYi0elk26R0mG6\noiL8TCdY9Pa4aKbdqpA61JYumn95aSZj+EgBFI7MBJveKpHb/9Bx8l+SU7J4MpHU\nP33SMUUfP/aRBbszPv4qmeQeWc1GdzyhppxzfmmPuO0KJmylH8dDJOqPmKuBT/SU\nft6n5F0JZmVG94UvLXnwuQ3qtR6YkDREJRySsItqHyz+XLFg76PezN29zOXxxo68\nOmQU7z5dK8TRN46DyKL8pw8iZUjCsOTAzkFUj0JoMQKBgQDmHjAO4tMZuvXS+GoS\n/PJjt4rSYe//788MGhJ7vnGv42cZHoXj9IBwhzg8cHhHm4ysH5s/aup39cUay+1a\nqjlGk1v9sLeCty52Q6RHb421PgIPI+qQ9d9f1N75qfqbHbn2IebJnMr6Tdd7zU5X\nYlfccf7I10FB7d6TReNag0CXcwKBgQDZ3PbHvUbp1qQ+6xcOU/M2ekWsvzwZq9+5\nN8hLAs+FLElKNDLwEWMTIlTog/eeUQmp4ZFUgN76GFo3Dhzj8xXvVYEJXwFRlBFn\nLduV5jer+B7pgNxyp0WvTKQ2sutZXjlqFXq6ffHnDHLQudXIbTm67kcCUIZk2fvW\nwAxKFyOwuQKBgCRu0x0IPHPubc0hF2o6MgYnoQr+Bol25kj8N8DvvgAi+Me5VWlp\n5IvsXLL0+5YawoLd3i6ENusXNkWv07xvBvJtkjrwJ53CctC2lOPafY0cbCcJgLHC\nu8LoaQUOLGcypaaaZ3e0I07N1Df9oVGkeFSml7gknGhbyMl4Xy6NaUSRAoGARiYd\n1+acJMMWE6RCwjxJvarVMHBK+8EZwluxxGVdSHYgCyKPnDkc+5Y8XLnRS0qwn+Cf\nmOP95+1bbwq+Rq+Iyo1vhQLwO8I/cEeVwshj+J1l5q21Tb2KdI1q+qnVmer69auA\n3veaolihx49uxKBWzFfYyWgAPgzqSBWCX4Df3xECgYEA3okHJtNx+++CG7vzqHRu\nd8I2j8sAhzUbtKRQuQoiVkieONRY8DdqrMM1XveA/BbPc/7QQXWlHVy0rd7fmDz1\nGscIgZVy0D8aeVSr+ZKfgb4ePaM17WewiIqQUpOS3G9A3WXwH/u7iTPbAuT5Qb5B\nl1OhlZ6wtAtQlhfY75laBw0=\n-----END PRIVATE KEY-----\n",
  "client_email": "papers-dev@supple-nature-438705-m6.iam.gserviceaccount.com",
  "client_id": "107123678672923975410",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/papers-dev%40supple-nature-438705-m6.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

### Setup Instructions
- Download Docker https://www.docker.com
- Inside the project open terminal and execute "docker compose up"
- pip install -r requirements.txt
- fastapi dev main.py

### Note
- You need to register an account in order to use the API.
- Your bearer auth token will be valid for 1 day
- API Examples are available in Postman Collection