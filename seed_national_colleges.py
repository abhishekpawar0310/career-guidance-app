from app import create_app, db
from app.models import College, Course, CollegeCourse, Career

app = create_app()

NEW_COLLEGES = [
    dict(name="IIT Bombay, Mumbai",
         address="Powai, Mumbai, Maharashtra - 400076",
         contact="022-2572 2545", website="https://www.iitb.ac.in"),
    dict(name="IIT Madras (Online Degree Programme)",
         address="IIT Madras Campus, Chennai, Tamil Nadu - 600036 (fully online programme)",
         contact="044-2257 8367", website="https://study.iitm.ac.in/ds/"),
    dict(name="All India Institute of Medical Sciences (AIIMS), New Delhi",
         address="Ansari Nagar, New Delhi - 110029",
         contact="011-2658 8500", website="https://www.aiims.edu"),
    dict(name="National Law School of India University (NLSIU), Bangalore",
         address="Nagarabhavi, Bengaluru, Karnataka - 560242",
         contact="080-2316 0532", website="https://www.nls.ac.in"),
    dict(name="National Institute of Design (NID), Ahmedabad",
         address="Paldi, Ahmedabad, Gujarat - 380007",
         contact="079-2662 3692", website="https://www.nid.edu"),
    dict(name="National Institute of Fashion Technology (NIFT), New Delhi",
         address="Hauz Khas, New Delhi - 110016",
         contact="011-2696 5080", website="https://www.nift.ac.in"),
    dict(name="Institute of Hotel Management, Catering & Nutrition (IHM Pusa), New Delhi",
         address="Library Avenue, Pusa, New Delhi - 110012",
         contact="011-2584 5203", website="https://www.ihmpusa.net"),
    dict(name="School of Planning and Architecture (SPA), New Delhi",
         address="4, Block-B, Indraprastha Estate, New Delhi - 110002",
         contact="011-2337 0480", website="https://www.spa.ac.in"),
    dict(name="Regional Institute of Education (NCERT), Mysuru",
         address="Manasagangothri, Mysuru, Karnataka - 570006",
         contact="0821-251 4095", website="https://riemysore.ac.in"),
    dict(name="Institute of Chartered Accountants of India (ICAI)",
         address="ICAI Bhawan, Indraprastha Marg, New Delhi - 110002",
         contact="011-3011 0511", website="https://www.icai.org"),
    dict(name="National Defence Academy (NDA), Khadakwasla",
         address="Khadakwasla, Pune, Maharashtra - 411023",
         contact="020-2431 2622", website="https://www.nda.nic.in"),
]

# Careers that ALREADY have a course (from seed_colleges.py) — just add a
# second, national college as another offering of that same course.
NEW_OFFERINGS_FOR_EXISTING_COURSES = [
    ("Software Engineer", "IIT Bombay, Mumbai",
     "approx Rs.8.59 Lakh (total, 4 years)", "https://www.iitb.ac.in"),
    ("Mechanical Engineer", "IIT Bombay, Mumbai",
     "approx Rs.8.59 Lakh (total, 4 years)", "https://www.iitb.ac.in"),
    ("Data Scientist", "IIT Madras (Online Degree Programme)",
     "approx Rs.4 Lakh (total, online programme)", "https://study.iitm.ac.in/ds/"),
    ("Doctor (MBBS)", "All India Institute of Medical Sciences (AIIMS), New Delhi",
     "approx Rs.6,000 (total, heavily subsidized govt fee)", "https://www.aiims.edu"),
    ("Lawyer", "National Law School of India University (NLSIU), Bangalore",
     "approx Rs.15 Lakh (total tuition, 5 years)", "https://www.nls.ac.in"),
    ("Graphic Designer", "National Institute of Design (NID), Ahmedabad",
     "approx Rs.16.8 Lakh (total, 4 years)", "https://www.nid.edu"),
    ("Fashion Designer", "National Institute of Fashion Technology (NIFT), New Delhi",
     "approx Rs.12 Lakh (total, 4 years)", "https://www.nift.ac.in"),
    ("Chef / Culinary Professional", "Institute of Hotel Management, Catering & Nutrition (IHM Pusa), New Delhi",
     "approx Rs.4.47 Lakh (total, 3 years)", "https://www.ihmpusa.net"),
]

# Careers that had NO course/college mapping until now — brand-new Course rows.
NEW_COURSES = [
    dict(name="B.Sc. (Hons.) Nursing",
         description="Undergraduate nursing degree covering clinical practice, patient care and health sciences.",
         career="Nurse / Healthcare Professional",
         college="All India Institute of Medical Sciences (AIIMS), New Delhi",
         fees="approx Rs.5,000 (total, heavily subsidized govt fee)",
         apply_link="https://www.aiims.edu"),
    dict(name="B.Arch (Bachelor of Architecture)",
         description="5-year architecture degree covering building design, structural planning and urban design.",
         career="Architect",
         college="School of Planning and Architecture (SPA), New Delhi",
         fees="approx Rs.4.9 Lakh (total, govt fee structure, 5 years)",
         apply_link="https://www.spa.ac.in"),
    dict(name="BA B.Ed. / BSc B.Ed. (Integrated)",
         description="4-year integrated teacher-training degree combining a general degree with a Bachelor of Education.",
         career="Teacher / Educator",
         college="Regional Institute of Education (NCERT), Mysuru",
         fees="approx Rs.20,000 (total, govt fee, 4 years)",
         apply_link="https://riemysore.ac.in"),
    dict(name="CA Foundation, Intermediate & Final",
         description="India's official Chartered Accountancy qualification, completed in three stages alongside practical articleship training.",
         career="Chartered Accountant",
         college="Institute of Chartered Accountants of India (ICAI)",
         fees="approx Rs.85,000 - 1 Lakh (total ICAI fees across all 3 levels, excludes optional coaching)",
         apply_link="https://www.icai.org"),
    dict(name="National Defence Academy (Army / Navy / Air Force Wing)",
         description="3-year tri-service training programme for direct-entry officers in the Indian Armed Forces, followed by service-specific academy training.",
         career="Police / Defense Services",
         college="National Defence Academy (NDA), Khadakwasla",
         fees="Fully government-funded - no tuition fee; cadets receive a stipend during training",
         apply_link="https://www.nda.nic.in"),
]

with app.app_context():
    # 1. Add new colleges (skip any that somehow already exist)
    college_objs = {c.name: c for c in College.query.all()}
    for c in NEW_COLLEGES:
        if c["name"] in college_objs:
            continue
        college = College(name=c["name"], address=c["address"], contact=c["contact"], website=c["website"])
        db.session.add(college)
        db.session.flush()
        college_objs[c["name"]] = college

    added_offerings = 0
    added_courses = 0
    skipped = []

    # 2. Add a second (national) college offering to careers that already have a course
    for career_name, college_name, fees, apply_link in NEW_OFFERINGS_FOR_EXISTING_COURSES:
        career = Career.query.filter_by(name=career_name).first()
        if not career:
            skipped.append(f"{career_name} (career not found)")
            continue
        course = Course.query.filter_by(career_id=career.id).first()
        if not course:
            skipped.append(f"{career_name} (no existing course to attach to)")
            continue
        college = college_objs.get(college_name)

        already_linked = CollegeCourse.query.filter_by(college_id=college.id, course_id=course.id).first()
        if already_linked:
            continue

        db.session.add(CollegeCourse(college_id=college.id, course_id=course.id, fees=fees, apply_link=apply_link))
        added_offerings += 1

    # 3. Brand-new courses for the 5 careers that had no mapping at all
    for item in NEW_COURSES:
        career = Career.query.filter_by(name=item["career"]).first()
        if not career:
            skipped.append(f"{item['career']} (career not found)")
            continue

        course = Course(name=item["name"], description=item["description"], career_id=career.id)
        db.session.add(course)
        db.session.flush()
        added_courses += 1

        college = college_objs.get(item["college"])
        db.session.add(CollegeCourse(
            college_id=college.id, course_id=course.id,
            fees=item["fees"], apply_link=item["apply_link"],
        ))
        added_offerings += 1

    db.session.commit()
    print(f"Colleges added: {len(NEW_COLLEGES)}")
    print(f"New college-course offerings added: {added_offerings}")
    print(f"Brand-new courses added (previously uncovered careers): {added_courses}")
    if skipped:
        print(f"Skipped: {skipped}")