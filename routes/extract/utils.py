import json
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
load_dotenv()

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
    with open('seed/physics.json', 'r') as file:
        data = json.load(file)
        return data
    vertexai.init(project="supple-nature-438705-m6", location="europe-west2")
    
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
    print("PDF", response_json)
    return response_json


# def generate_sample_paper_from_text(document_text):
#     vertexai.init(project="supple-nature-438705-m6", location="europe-west2")
    
    
#     text1 = f"""Extract information and convert it to the sample paper JSON format. If possible then must try to provide answer and hit as well. Covering all questions from the document is highest priority you can give small hits if necessary to cover up all the questions in response. Lastly Don\'t forget to give credits to the owner of document. {document_text}"""
#     textsi_1 = """You are a PDF and Text extractor that extracts the data and returns in the Sample Paper JSON Structure below.

#     {
#     \"title\": \"Sample Paper Title\",
#     \"type\": \"previous_year\",
#     \"time\": 180,
#     \"marks\": 100,
#     \"params\": {
#     \"board\": \"CBSE\",
#     \"grade\": 10,
#     \"subject\": \"Maths\"
#     },
#     \"tags\": [
#     \"algebra\",
#     \"geometry\"
#     ],
#     \"chapters\": [
#     \"Quadratic Equations\",\"Triangles\"
#     ],
#     \"sections\": [
#     {
#     \"marks_per_question\": 5,
#     \"type\": \"default\",
#     \"questions\": [
#     {
#     \"question\": \"Solve the quadratic equation: x^2 + 5x + 6 = 0\",
#     \"answer\": \"The solutions are x = -2 and x = -3\",
#     \"type\": \"short\",
#     \"question_slug\": \"solve-quadratic-equation\",
#     \"reference_id\": \"QE001\",
#     \"hint\": \"Use the quadratic formula or factorization method\",
#     \"params\": {}
#     },
#     {
#     \"question\": \"In a right-angled triangle, if one angle is 30°, what is the other acute angle?\",
#     \"answer\": \"60°\",
#     \"type\": \"short\",
#     \"question_slug\": \"right-angle-triangle-angles\",
#     \"reference_id\": \"GT001\",
#     \"hint\": \"Remember that the sum of angles in a triangle is 180°\",
#     \"params\": {}
#     },
#     \"credits\": \"CBSE India\"
#     ]
#     }
#     ]
#     }"""
    

#     model = GenerativeModel(
#         "gemini-1.5-flash-002",
#         system_instruction=[textsi_1]
#     )

#     response = model.generate_content(
#         [text1],
#         generation_config=generation_config,
#         safety_settings=safety_settings,
#         stream=False
#     )
    
#     response_json = json.loads(response.candidates[0].content.parts[0].text)
#     print("TEXT", response_json)
    
#     return response_json




# def generate_sample_paper_from_pdf(pdf_data):
#     return {
#     "title": "Physics (Theory)",
#     "type": "previous_year",
#     "time": 180,
#     "marks": 70,
#     "params": {
#         "board": "CBSE",
#         "grade": 12,
#         "subject": "Physics"
#     },
#     "tags": [
#         "Electrostatics",
#         "Current Electricity",
#         "Magnetism",
#         "Electromagnetic Induction",
#         "Optics",
#         "Dual Nature of Matter",
#         "Atoms and Nuclei",
#         "Semiconductor Electronics",
#         "Communication Systems"
#     ],
#     "chapters": [
#         "Electrostatics",
#         "Current Electricity",
#         "Magnetism",
#         "Electromagnetic Induction",
#         "Optics",
#         "Dual Nature of Matter",
#         "Atoms and Nuclei",
#         "Semiconductor Electronics",
#         "Communication Systems"
#     ],
#     "sections": [
#         {
#             "marks_per_question": 1,
#             "type": "mcq",
#             "questions": [
#                 {
#                     "question": "A point charge situated at a distance 'r' from a short electric dipole on its axis, experiences a force F. If the distance of the charge is '2r', the force on the charge will be :",
#                     "answer": "F/8",
#                     "type": "mcq",
#                     "question_slug": "electric-dipole-force",
#                     "reference_id": "QE001",
#                     "hint": "The force due to an electric dipole is inversely proportional to the cube of the distance.",
#                     "params": {}
#                 },
#                 {
#                     "question": "For a metallic conductor, the correct representation of variation of resistance R with temperature T is :",
#                     "answer": "(b)",
#                     "type": "mcq",
#                     "question_slug": "resistance-temperature-variation",
#                     "reference_id": "CE001",
#                     "hint": "The resistance of a metallic conductor increases linearly with temperature.",
#                     "params": {}
#                 },
#                 {
#                     "question": "The potential difference across a cell in an open circuit is 8 V. It falls to 4 V when a current of 4 A is drawn from it. The internal resistance of the cell is :",
#                     "answer": "1 Ω",
#                     "type": "mcq",
#                     "question_slug": "internal-resistance-cell",
#                     "reference_id": "CE002",
#                     "hint": "Use the formula V = E - Ir, where V is the potential difference, E is the emf, I is the current, and r is the internal resistance.",
#                     "params": {}
#                 },
#                 {
#                     "question": "A steady current flows through a metallic wire whose area of cross-section (A) increases continuously from one end of the wire to the other. The magnitude of drift velocity (va) of the free electrons as a function of 'A' can be shown by :",
#                     "answer": "(b)",
#                     "type": "mcq",
#                     "question_slug": "drift-velocity-variation",
#                     "reference_id": "CE003",
#                     "hint": "The drift velocity is inversely proportional to the area of cross-section.",
#                     "params": {}
#                 },
#                 {
#                     "question": "A diamagnetic substance is brought near the north or south pole of a bar magnet. It will be :",
#                     "answer": "(a)",
#                     "type": "mcq",
#                     "question_slug": "diamagnetic-substance-behavior",
#                     "reference_id": "M001",
#                     "hint": "Diamagnetic substances are repelled by both poles of a magnet.",
#                     "params": {}
#                 },
#                 {
#                     "question": "A circular coil of radius 8.0 cm and 40 turns is rotated about its vertical diameter with an angular speed of 25π rad s⁻¹ in a uniform horizontal magnetic field of magnitude 3.0 × 10⁻² T. The maximum emf induced in the coil is :",
#                     "answer": "0.19 V",
#                     "type": "mcq",
#                     "question_slug": "induced-emf-coil",
#                     "reference_id": "EMI001",
#                     "hint": "Use the formula ε = NBAω, where ε is the induced emf, N is the number of turns, B is the magnetic field, A is the area, and ω is the angular speed.",
#                     "params": {}
#                 },
#                 {
#                     "question": "Figure shows a rectangular conductor PSRQ in which movable arm PQ has a resistance 'r' and resistance of PSRQ is negligible. The magnitude of emf induced when PQ is moved with a velocity 'v' does not depend on :",
#                     "answer": "(c)",
#                     "type": "mcq",
#                     "question_slug": "induced-emf-conductor",
#                     "reference_id": "EMI002",
#                     "hint": "The induced emf is independent of the resistance of the conductor.",
#                     "params": {}
#                 },
#                 {
#                     "question": "In the process of charging of a capacitor, the current produced between the plates of the capacitor is :",
#                     "answer": "(c)",
#                     "type": "mcq",
#                     "question_slug": "capacitor-charging-current",
#                     "reference_id": "CE004",
#                     "hint": "The displacement current is given by I = ε₀(dΦE/dt), where ΦE is the electric flux.",
#                     "params": {}
#                 },
#                 {
#                     "question": "For a concave mirror of focal length 'f', the minimum distance between the object and its real image is :",
#                     "answer": "4f",
#                     "type": "mcq",
#                     "question_slug": "concave-mirror-object-image-distance",
#                     "reference_id": "O001",
#                     "hint": "The minimum distance occurs when the object is at the centre of curvature.",
#                     "params": {}
#                 },
#                 {
#                     "question": "The radius of the nth orbit in Bohr model of hydrogen atom is proportional to :",
#                     "answer": "n²",
#                     "type": "mcq",
#                     "question_slug": "bohr-model-radius",
#                     "reference_id": "AN001",
#                     "hint": "The radius of the nth orbit is given by r = n²a₀, where a₀ is the Bohr radius.",
#                     "params": {}
#                 },
#                 {
#                     "question": "Hydrogen atom initially in the ground state, absorbs a photon which excites it to n = 5 level. The wavelength of the photon is :",
#                     "answer": "975 nm",
#                     "type": "mcq",
#                     "question_slug": "hydrogen-atom-photon-wavelength",
#                     "reference_id": "AN002",
#                     "hint": "Use the formula 1/λ = R(1/n₁² - 1/n₂²), where R is the Rydberg constant, n₁ is the initial energy level, and n₂ is the final energy level.",
#                     "params": {}
#                 },
#                 {
#                     "question": "The mass density of a nucleus of mass number A is :",
#                     "answer": "(d)",
#                     "type": "mcq",
#                     "question_slug": "nuclear-mass-density",
#                     "reference_id": "AN003",
#                     "hint": "The mass density of a nucleus is approximately constant.",
#                     "params": {}
#                 },
#                 {
#                     "question": "An ac source of voltage is connected in series with a p-n junction diode and a load resistor. The correct option for output voltage across load resistance will be :",
#                     "answer": "(b)",
#                     "type": "mcq",
#                     "question_slug": "p-n-diode-output-voltage",
#                     "reference_id": "SE001",
#                     "hint": "A p-n junction diode conducts only in the forward bias.",
#                     "params": {}
#                 },
#                 {
#                     "question": "When an intrinsic semiconductor is doped with a small amount of trivalent impurity, then :",
#                     "answer": "(b)",
#                     "type": "mcq",
#                     "question_slug": "semiconductor-doping",
#                     "reference_id": "SE002",
#                     "hint": "A trivalent impurity creates p-type semiconductor.",
#                     "params": {}
#                 },
#                 {
#                     "question": "In the energy-band diagram of n-type Si, the gap between the bottom of the conduction band Ec and the donor energy level Ed is of the order of :",
#                     "answer": "(d)",
#                     "type": "mcq",
#                     "question_slug": "energy-band-gap-n-type-si",
#                     "reference_id": "SE003",
#                     "hint": "The energy gap is very small in n-type Si.",
#                     "params": {}
#                 }
#             ],
#             "credits": "CBSE India"
#         }
#     ]
# }