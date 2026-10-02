from app import create_app, db
from app.models import College, Course, CollegeCourse, Career

app = create_app()

COLLEGES = [
    dict(name="COEP Technological University, Pune",
         address="Wellesely Road, Shivajinagar, Pune - 411005, Maharashtra",
         contact="020-2550 7000",
         website="https://www.coeptech.ac.in"),
    dict(name="B.J. Government Medical College, Pune",
         address="J.P. Narayan Road, Near Pune Railway Station, Pune - 411001, Maharashtra",
         contact="020-2612 8000",
         website="https://www.bjgmcpune.org"),
    dict(name="Fergusson College (Deemed University), Pune",
         address="Fergusson College Road, Shivajinagar, Pune - 411004, Maharashtra",
         contact="020-2565 6236",
         website="https://www.fergusson.edu"),
    dict(name="Symbiosis Law School, Pune",
         address="Survey No. 227, Plot 11, Opp. Pune Airport, New Airport Road, Viman Nagar, Pune - 411014, Maharashtra",
         contact="020-6686 1100",
         website="https://www.symlaw.ac.in"),
    dict(name="Symbiosis Centre for Management Studies, Pune",
         address="Survey No. 231, near Lunkad Gold Coast, Clover Park, Viman Nagar, Pune - 411014, Maharashtra",
         contact="020-6621 0000",
         website="https://www.scmspune.ac.in"),
    dict(name="MIT Institute of Design, Pune",
         address="Rajbaug, Loni Kalbhor, Pune-Solapur Highway, Pune - 412201, Maharashtra",
         contact="+91 92098 00600",
         website="https://www.mitid.edu.in"),
    dict(name="Symbiosis Centre for Media & Communication, Pune",
         address="Symbiosis Campus, off Symbiosis Road, Viman Nagar, Pune - 411014, Maharashtra",
         contact="020-6621 0000",
         website="https://www.scmc.edu.in"),
    dict(name="Dr. D. Y. Patil Institute of Hotel Management & Catering Technology, Pune",
         address="Sr. No. 87/88, Tathawade, Tal. Mulshi, Pune - 411033, Maharashtra",
         contact="020-6791 9476",
         website="https://hmct.dypvp.edu.in"),
]

# Each course maps to exactly one Career (matches your Course.career_id design).
# Where one degree genuinely leads to several careers (e.g. BBA, B.Tech CSE),
# it appears as separate course rows so each can link to its own career.
COURSES = [
    dict(name="B.Tech Computer Science & Engineering",
         description="Core software engineering, systems and programming fundamentals.",
         career="Software Engineer", college="COEP Technological University, Pune",
         fees="approx Rs.6.25 Lakh (total, govt fee structure)",
         apply_link="https://www.coeptech.ac.in"),
    dict(name="B.Tech CSE (Data Science Track)",
         description="Computer science fundamentals with a specialization in data science and machine learning.",
         career="Data Scientist", college="COEP Technological University, Pune",
         fees="approx Rs.6.25 Lakh (total, govt fee structure)",
         apply_link="https://www.coeptech.ac.in"),
    dict(name="B.Tech CSE (Analytics Track)",
         description="Computer science fundamentals with a focus on data analytics and business intelligence.",
         career="Data / Business Analyst", college="COEP Technological University, Pune",
         fees="approx Rs.6.25 Lakh (total, govt fee structure)",
         apply_link="https://www.coeptech.ac.in"),
    dict(name="B.Tech Mechanical Engineering",
         description="Core mechanical design, thermodynamics and manufacturing systems.",
         career="Mechanical Engineer", college="COEP Technological University, Pune",
         fees="approx Rs.6.25 Lakh (total, govt fee structure)",
         apply_link="https://www.coeptech.ac.in"),
    dict(name="B.Tech Civil Engineering",
         description="Structural design, construction management and infrastructure planning.",
         career="Civil Engineer", college="COEP Technological University, Pune",
         fees="approx Rs.6.25 Lakh (total, govt fee structure)",
         apply_link="https://www.coeptech.ac.in"),
    dict(name="MBBS (Bachelor of Medicine & Bachelor of Surgery)",
         description="5.5-year medical degree covering pre-clinical, para-clinical and clinical training.",
         career="Doctor (MBBS)", college="B.J. Government Medical College, Pune",
         fees="approx Rs.5.5 Lakh (total, govt fee structure)",
         apply_link="https://www.bjgmcpune.org"),
    dict(name="B.A. Psychology",
         description="Undergraduate psychology covering human behavior, cognition and counseling foundations.",
         career="Psychologist / Counselor", college="Fergusson College (Deemed University), Pune",
         fees="approx Rs.90,000 (total, self-financed)",
         apply_link="https://www.fergusson.edu"),
    dict(name="B.A. LL.B. (Hons.)",
         description="5-year integrated law degree combining a general degree with a law qualification.",
         career="Lawyer", college="Symbiosis Law School, Pune",
         fees="approx Rs.24 Lakh (total, 5 years)",
         apply_link="https://www.symlaw.ac.in"),
    dict(name="BBA - Marketing Management",
         description="Business administration with a specialization in marketing and brand management.",
         career="Marketing Manager", college="Symbiosis Centre for Management Studies, Pune",
         fees="approx Rs.9.5 Lakh (total)",
         apply_link="https://www.scmspune.ac.in"),
    dict(name="BBA - Entrepreneurship",
         description="Business administration with a specialization in new venture creation and entrepreneurship.",
         career="Entrepreneur / Business Owner", college="Symbiosis Centre for Management Studies, Pune",
         fees="approx Rs.9.5 Lakh (total)",
         apply_link="https://www.scmspune.ac.in"),
    dict(name="BBA - Accounting & Finance",
         description="Business administration with a specialization in accounting, banking and finance.",
         career="Bank / Finance Professional", college="Symbiosis Centre for Management Studies, Pune",
         fees="approx Rs.9.5 Lakh (total)",
         apply_link="https://www.scmspune.ac.in"),
    dict(name="B.Des (Communication / Product Design)",
         description="Undergraduate design degree covering visual communication, branding and product design.",
         career="Graphic Designer", college="MIT Institute of Design, Pune",
         fees="approx Rs.18.75 Lakh (total)",
         apply_link="https://www.mitid.edu.in"),
    dict(name="B.Des Fashion Design",
         description="Undergraduate design degree focused on fashion design, textiles and trend forecasting.",
         career="Fashion Designer", college="MIT Institute of Design, Pune",
         fees="approx Rs.18.90 Lakh (total)",
         apply_link="https://www.mitid.edu.in"),
    dict(name="B.A. Mass Communication (Hons.)",
         description="Undergraduate journalism and mass communication degree covering print, digital and broadcast media.",
         career="Content Writer / Journalist", college="Symbiosis Centre for Media & Communication, Pune",
         fees="approx Rs.13.84 Lakh (total, 4 years)",
         apply_link="https://www.scmc.edu.in"),
    dict(name="BHMCT (Bachelor of Hotel Management & Catering Technology)",
         description="Undergraduate hospitality degree covering culinary arts, hotel operations and catering management.",
         career="Chef / Culinary Professional", college="Dr. D. Y. Patil Institute of Hotel Management & Catering Technology, Pune",
         fees="approx Rs.7.2 Lakh (total)",
         apply_link="https://hmct.dypvp.edu.in"),
]

with app.app_context():
    CollegeCourse.query.delete()
    Course.query.delete()
    College.query.delete()
    db.session.commit()

    college_objs = {}
    for c in COLLEGES:
        college = College(name=c["name"], address=c["address"], contact=c["contact"], website=c["website"])
        db.session.add(college)
        db.session.flush()
        college_objs[c["name"]] = college

    skipped = []
    added = 0
    for item in COURSES:
        career = Career.query.filter_by(name=item["career"]).first()
        if not career:
            skipped.append(item["career"])
            continue

        course = Course(name=item["name"], description=item["description"], career_id=career.id)
        db.session.add(course)
        db.session.flush()

        college = college_objs[item["college"]]
        db.session.add(CollegeCourse(
            college_id=college.id,
            course_id=course.id,
            fees=item["fees"],
            apply_link=item["apply_link"],
        ))
        added += 1

    db.session.commit()
    print(f"Seeded {len(COLLEGES)} colleges and {added} college-course offerings.")
    if skipped:
        print(f"Skipped (career not found — did you run seed_careers.py first?): {skipped}")