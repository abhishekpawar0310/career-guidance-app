from app import create_app, db
from app.models import Career

app = create_app()

CAREERS = [
    dict(name="Data Scientist", suited_level="both",
         description="Analyzes large datasets to uncover patterns and drive business decisions using statistics, programming and machine learning.",
         riasec={"R": 1, "I": 9, "A": 3, "S": 3, "E": 4, "C": 6},
         aptitude={"logical": 9, "verbal": 5, "numerical": 8}),
    dict(name="Software Engineer", suited_level="both",
         description="Designs, builds and maintains software applications and systems used by millions of people.",
         riasec={"R": 4, "I": 8, "A": 3, "S": 3, "E": 4, "C": 5},
         aptitude={"logical": 9, "verbal": 5, "numerical": 7}),
    dict(name="Doctor (MBBS)", suited_level="both",
         description="Diagnoses and treats illness, working directly with patients to improve health outcomes.",
         riasec={"R": 3, "I": 9, "A": 2, "S": 8, "E": 3, "C": 5},
         aptitude={"logical": 7, "verbal": 6, "numerical": 6}),
    dict(name="Mechanical Engineer", suited_level="both",
         description="Designs, builds and tests machines, engines and mechanical systems.",
         riasec={"R": 9, "I": 7, "A": 3, "S": 2, "E": 3, "C": 5},
         aptitude={"logical": 8, "verbal": 4, "numerical": 9}),
    dict(name="Civil Engineer", suited_level="both",
         description="Plans and oversees construction of infrastructure like buildings, roads and bridges.",
         riasec={"R": 8, "I": 6, "A": 3, "S": 3, "E": 4, "C": 6},
         aptitude={"logical": 7, "verbal": 4, "numerical": 8}),
    dict(name="Graphic Designer", suited_level="both",
         description="Creates visual content — branding, illustrations and layouts — that communicates ideas and emotions.",
         riasec={"R": 2, "I": 3, "A": 9, "S": 3, "E": 4, "C": 3},
         aptitude={"logical": 3, "verbal": 5, "numerical": 2}),
    dict(name="Content Writer / Journalist", suited_level="both",
         description="Researches and writes stories, articles or content that informs, entertains or persuades an audience.",
         riasec={"R": 1, "I": 5, "A": 8, "S": 5, "E": 5, "C": 3},
         aptitude={"logical": 4, "verbal": 9, "numerical": 2}),
    dict(name="Teacher / Educator", suited_level="both",
         description="Educates and mentors students, making complex subjects easier to understand.",
         riasec={"R": 2, "I": 5, "A": 4, "S": 9, "E": 4, "C": 6},
         aptitude={"logical": 5, "verbal": 8, "numerical": 4}),
    dict(name="Psychologist / Counselor", suited_level="both",
         description="Helps people understand and manage their thoughts, emotions and behavior.",
         riasec={"R": 1, "I": 7, "A": 4, "S": 9, "E": 3, "C": 4},
         aptitude={"logical": 5, "verbal": 8, "numerical": 3}),
    dict(name="Entrepreneur / Business Owner", suited_level="both",
         description="Builds and runs a business from the ground up, taking on risk to create something new.",
         riasec={"R": 4, "I": 5, "A": 5, "S": 4, "E": 9, "C": 5},
         aptitude={"logical": 6, "verbal": 6, "numerical": 6}),
    dict(name="Marketing Manager", suited_level="both",
         description="Plans campaigns and strategy to promote products, brands or services to the right audience.",
         riasec={"R": 2, "I": 4, "A": 7, "S": 5, "E": 9, "C": 4},
         aptitude={"logical": 5, "verbal": 8, "numerical": 4}),
    dict(name="Chartered Accountant", suited_level="both",
         description="Manages financial records, audits, tax planning and compliance for businesses and individuals.",
         riasec={"R": 2, "I": 6, "A": 1, "S": 3, "E": 5, "C": 10},
         aptitude={"logical": 8, "verbal": 5, "numerical": 9}),
    dict(name="Lawyer", suited_level="both",
         description="Advises and represents clients on legal matters, from contracts to courtroom cases.",
         riasec={"R": 1, "I": 7, "A": 4, "S": 6, "E": 8, "C": 6},
         aptitude={"logical": 8, "verbal": 9, "numerical": 3}),
    dict(name="Architect", suited_level="both",
         description="Designs buildings and spaces that are functional, safe and aesthetically striking.",
         riasec={"R": 6, "I": 6, "A": 9, "S": 3, "E": 4, "C": 5},
         aptitude={"logical": 7, "verbal": 4, "numerical": 7}),
    dict(name="Nurse / Healthcare Professional", suited_level="both",
         description="Provides direct patient care, working closely with doctors to support recovery and wellbeing.",
         riasec={"R": 5, "I": 5, "A": 2, "S": 9, "E": 2, "C": 6},
         aptitude={"logical": 5, "verbal": 6, "numerical": 5}),
    dict(name="Police / Defense Services", suited_level="both",
         description="Protects public safety and order through law enforcement, discipline and physical readiness.",
         riasec={"R": 8, "I": 4, "A": 1, "S": 6, "E": 6, "C": 6},
         aptitude={"logical": 6, "verbal": 5, "numerical": 5}),
    dict(name="Chef / Culinary Professional", suited_level="both",
         description="Creates and prepares food professionally, blending creativity, taste and technique.",
         riasec={"R": 7, "I": 3, "A": 8, "S": 4, "E": 5, "C": 4},
         aptitude={"logical": 3, "verbal": 3, "numerical": 3}),
    dict(name="Fashion Designer", suited_level="both",
         description="Designs clothing and accessories, combining creativity with an understanding of trends and fabric.",
         riasec={"R": 3, "I": 3, "A": 10, "S": 4, "E": 6, "C": 3},
         aptitude={"logical": 3, "verbal": 4, "numerical": 3}),
    dict(name="Bank / Finance Professional", suited_level="both",
         description="Manages banking operations, investments, loans and financial planning for clients or institutions.",
         riasec={"R": 2, "I": 5, "A": 2, "S": 4, "E": 6, "C": 9},
         aptitude={"logical": 7, "verbal": 5, "numerical": 8}),
    dict(name="Data / Business Analyst", suited_level="both",
         description="Interprets business data to find trends and recommend decisions that improve performance.",
         riasec={"R": 2, "I": 8, "A": 3, "S": 4, "E": 5, "C": 8},
         aptitude={"logical": 8, "verbal": 6, "numerical": 8}),
]

with app.app_context():
    created, updated = 0, 0

    for c in CAREERS:
        career = Career.query.filter_by(name=c["name"]).first()
        if career:
            career.description = c["description"]
            career.riasec_profile = c["riasec"]
            career.aptitude_profile = c["aptitude"]
            career.suited_level = c["suited_level"]
            updated += 1
        else:
            db.session.add(Career(
                name=c["name"],
                description=c["description"],
                riasec_profile=c["riasec"],
                aptitude_profile=c["aptitude"],
                suited_level=c["suited_level"],
            ))
            created += 1

    db.session.commit()
    print(f"Careers: {created} created, {updated} updated. Existing IDs preserved.")