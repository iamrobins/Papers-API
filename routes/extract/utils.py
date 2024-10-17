import json, os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from google.oauth2 import service_account
load_dotenv()

# Load credentials from environment variable
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_VERTEX_AI_PROJECT = os.getenv("GOOGLE_VERTEX_AI_PROJECT")
GOOGLE_VERTEX_AI_LOCATION = os.getenv("GOOGLE_VERTEX_AI_LOCATION")

# Load credentials object
credentials = service_account.Credentials.from_service_account_file(credentials_path)


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
    "response_mime_type": "application/json"
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

def generate_sample_paper(file_type, file_data):
    print("Initializing Vertex AI...")
    vertexai.init(project=GOOGLE_VERTEX_AI_PROJECT, location=GOOGLE_VERTEX_AI_LOCATION, credentials=credentials)
    
    document1 = Part.from_data(
        mime_type=file_type,
        data=file_data)
    text1 = """Extract information and convert it to the sample paper JSON format. If possible then must try to provide answer and hit as well. Covering all questions from the document is highest priority you can give small hits if necessary to cover up all the questions in response. Lastly Don\'t forget to give credits to the owner of document."""
    textsi_1 = """You are a PDF and Text extractor that extracts the data and returns in the Sample Paper JSON Structure below.

    {
    \"title\": \"Sample Paper Title\",
    \"type\": \"previous_year\",
    \"time\": 180,
    \"marks\": 100,
    \"params\": {
    \"board\": \"CBSE\",
    \"grade\": 10,
    \"subject\": \"Maths\"
    },
    \"tags\": [
    \"algebra\",
    \"geometry\"
    ],
    \"chapters\": [
    \"Quadratic Equations\",\"Triangles\"
    ],
    \"sections\": [
    {
    \"marks_per_question\": 5,
    \"type\": \"default\",
    \"questions\": [
    {
    \"question\": \"Solve the quadratic equation: x^2 + 5x + 6 = 0\",
    \"answer\": \"The solutions are x = -2 and x = -3\",
    \"type\": \"short\",
    \"question_slug\": \"solve-quadratic-equation\",
    \"reference_id\": \"QE001\",
    \"hint\": \"Use the quadratic formula or factorization method\",
    \"params\": {}
    },
    {
    \"question\": \"In a right-angled triangle, if one angle is 30°, what is the other acute angle?\",
    \"answer\": \"60°\",
    \"type\": \"short\",
    \"question_slug\": \"right-angle-triangle-angles\",
    \"reference_id\": \"GT001\",
    \"hint\": \"Remember that the sum of angles in a triangle is 180°\",
    \"params\": {}
    },
    \"credits\": \"CBSE India\"
    ]
    }
    ]
    }"""

    model = GenerativeModel(
        "gemini-1.5-flash-002",
        system_instruction=[textsi_1]
    )

    response = model.generate_content(
        [document1, text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    response_json = json.loads(response.candidates[0].content.parts[0].text)
    print(response_json)
    return response_json

