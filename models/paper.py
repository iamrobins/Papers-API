from pydantic import BaseModel, Field, validator
from typing import List, Optional

# Define the question model
class QuestionModel(BaseModel):
    question: str
    answer: str
    type: str  # Allow any string value for flexibility
    question_slug: str
    reference_id: str
    hint: Optional[str] = None
    params: Optional[dict] = {}

    @validator('question_slug')
    def validate_slug(cls, v):
        if not v or " " in v:
            raise ValueError("Invalid slug format, no spaces allowed")
        return v

# Define the section model
class SectionModel(BaseModel):
    marks_per_question: int
    type: str  # Allow any string value for flexibility
    questions: List[QuestionModel]

    @validator('marks_per_question')
    def validate_marks(cls, v):
        if v <= 0:
            raise ValueError('Marks per question must be greater than 0')
        return v

# Define the main sample paper model
class SamplePaperModel(BaseModel):
    title: str
    type: str = Field(..., description="Type of the paper (e.g., 'previous_year')")  # Allow any string for flexibility
    time: int
    marks: int
    params: dict
    tags: List[str]
    chapters: List[str]
    sections: List[SectionModel]

    @validator('time')
    def validate_time(cls, v):
        if v <= 0:
            raise ValueError('Time must be greater than 0')
        return v

    @validator('marks')
    def validate_marks(cls, v):
        if v <= 0:
            raise ValueError('Total marks must be greater than 0')
        return v

    @validator('params')
    def validate_params(cls, v):
        required_keys = ['board', 'grade', 'subject']
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required parameter: {key}")
        return v

# Example JSON input that would pass validation
example_paper = {
    "title": "Sample Paper Title",
    "type": "previous_year",  # This is flexible now
    "time": 180,
    "marks": 100,
    "params": {
        "board": "CBSE",
        "grade": 10,
        "subject": "Maths"
    },
    "tags": [
        "algebra",
        "geometry"
    ],
    "chapters": [
        "Quadratic Equations",
        "Triangles"
    ],
    "sections": [
        {
            "marks_per_question": 5,
            "type": "default",  # This is flexible now
            "questions": [
                {
                    "question": "Solve the quadratic equation: x^2 + 5x + 6 = 0",
                    "answer": "The solutions are x = -2 and x = -3",
                    "type": "short",  # This is flexible now
                    "question_slug": "solve-quadratic-equation",
                    "reference_id": "QE001",
                    "hint": "Use the quadratic formula or factorization method",
                    "params": {}
                },
                {
                    "question": "In a right-angled triangle, if one angle is 30°, what is the other acute angle?",
                    "answer": "60°",
                    "type": "short",  # This is flexible now
                    "question_slug": "right-angle-triangle-angles",
                    "reference_id": "GT001",
                    "hint": "Remember that the sum of angles in a triangle is 180°",
                    "params": {}
                }
            ]
        }
    ]
}

# Validating the example paper using the Pydantic model
try:
    validated_paper = SamplePaperModel(**example_paper)
    print("Validation successful!")
except Exception as e:
    print(f"Validation error: {e}")
