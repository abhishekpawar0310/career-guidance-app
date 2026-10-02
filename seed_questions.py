from app import create_app, db
from app.models import Question, Option

app = create_app()

RIASEC_10TH = [
    ("R", "I enjoy fixing or building things with my hands (bikes, gadgets, furniture, etc.)"),
    ("R", "I like outdoor activities such as sports, gardening, or working with machines/tools."),
    ("R", "I would rather work with real objects and tools than sit and write reports all day."),
    ("I", "I like figuring out how things work and solving puzzles or problems."),
    ("I", "I enjoy science experiments and asking 'why' questions about the world around me."),
    ("I", "I like researching a topic in depth rather than just skimming the basics."),
    ("A", "I enjoy drawing, writing stories, making music, or other creative activities."),
    ("A", "I like coming up with original ideas rather than following a fixed method."),
    ("A", "I enjoy expressing my feelings through art, design, or performance."),
    ("S", "I like helping classmates understand something they're struggling with."),
    ("S", "I enjoy volunteering or working in team activities that help other people."),
    ("S", "I feel good when I can listen to someone's problems and support them."),
    ("E", "I like taking the lead in group projects and organizing what everyone should do."),
    ("E", "I enjoy convincing others or presenting my ideas confidently."),
    ("E", "I would enjoy starting my own small business or selling something."),
    ("C", "I like keeping things organized — notes, schedules, files — in a neat structured way."),
    ("C", "I'm comfortable working with numbers, spreadsheets, or detailed records."),
    ("C", "I prefer having clear step-by-step instructions rather than figuring things out on my own."),
]

APTITUDE_10TH = [
    ("logical", "Look at the pattern: 2, 4, 8, 16, ?. What comes next?",
     [("20", False), ("24", False), ("32", True), ("18", False)]),
    ("logical", "If today is Wednesday, what day will it be after 10 days?",
     [("Friday", False), ("Saturday", True), ("Sunday", False), ("Monday", False)]),
    ("verbal", "Choose the word that means almost the same as 'ABUNDANT'.",
     [("Scarce", False), ("Plentiful", True), ("Empty", False), ("Broken", False)]),
    ("verbal", "Choose the word that does NOT belong with the others.",
     [("Apple", False), ("Banana", False), ("Carrot", True), ("Mango", False)]),
    ("numerical", "A shirt costs Rs.800 after a 20% discount. What was its original price?",
     [("Rs.900", False), ("Rs.960", False), ("Rs.1000", True), ("Rs.1200", False)]),
    ("numerical", "What is 15% of 200?",
     [("20", False), ("25", False), ("30", True), ("35", False)]),
]

RIASEC_12TH = [
    ("R", "I'd enjoy a hands-on job (engineering workshops, labs, fieldwork) more than a desk-only job."),
    ("R", "I like working with tools, machinery, or technical equipment to build or repair things."),
    ("R", "I would choose a practical, hands-on training program over a purely theoretical one."),
    ("I", "I enjoy analyzing data, diagnosing problems, or doing in-depth research on a topic."),
    ("I", "I like understanding the 'why' and 'how' behind scientific or technical concepts."),
    ("I", "I would enjoy a career that involves continuous learning, experimentation, and analysis."),
    ("A", "I would enjoy a career where I get to design, write, or create original content."),
    ("A", "I like thinking outside the box and coming up with unconventional solutions."),
    ("A", "Self-expression through art, media, writing or design excites me more than routine work."),
    ("S", "I would enjoy a career centered on teaching, counseling, healthcare or community work."),
    ("S", "Helping others grow, learn, or resolve personal issues is something I find fulfilling."),
    ("S", "I prefer working directly with people over working alone with data or machines."),
    ("E", "I would enjoy leading a team, managing a project, or running my own venture."),
    ("E", "I like negotiating, pitching ideas, or persuading people to see my point of view."),
    ("E", "Taking calculated risks to achieve ambitious goals excites me."),
    ("C", "I would enjoy a career involving structured processes: accounting, data management, admin."),
    ("C", "I like maintaining accuracy, order and following established procedures."),
    ("C", "I prefer a predictable, well-organized work routine over a constantly changing one."),
]

APTITUDE_12TH = [
    ("logical", "Complete the series: 3, 6, 12, 24, ?",
     [("30", False), ("36", False), ("48", True), ("40", False)]),
    ("logical", "If 5 machines make 5 items in 5 minutes, how long for 100 machines to make 100 items?",
     [("100 minutes", False), ("50 minutes", False), ("5 minutes", True), ("20 minutes", False)]),
    ("logical", "All roses are flowers. Some flowers fade quickly. Which conclusion is valid?",
     [("All roses fade quickly", False), ("Some roses fade quickly", False),
      ("No roses fade quickly", False), ("Cannot be determined from the given information", True)]),
    ("verbal", "Choose the word most OPPOSITE in meaning to 'RETICENT'.",
     [("Silent", False), ("Shy", False), ("Outspoken", True), ("Careful", False)]),
    ("verbal", "Complete the analogy: Doctor is to Hospital as Teacher is to ____.",
     [("Book", False), ("School", True), ("Student", False), ("Chalk", False)]),
    ("verbal", "Choose the correctly spelled word.",
     [("Recieve", False), ("Receive", True), ("Receeve", False), ("Receve", False)]),
    ("numerical", "A train travels 300 km in 5 hours. What is its average speed?",
     [("50 km/h", False), ("60 km/h", True), ("70 km/h", False), ("80 km/h", False)]),
    ("numerical", "If x + 5 = 12, what is the value of 3x?",
     [("18", False), ("21", True), ("24", False), ("15", False)]),
    ("numerical", "A sum of Rs.5000 becomes Rs.5500 in one year at simple interest. What is the rate?",
     [("8%", False), ("10%", True), ("12%", False), ("15%", False)]),
]


def seed_riasec(level, items):
    for order, (letter, text) in enumerate(items):
        q = Question(level=level, text=text, category='interest', order=order)
        db.session.add(q)
        db.session.flush()
        db.session.add(Option(question_id=q.id, text="Yes, this sounds like me", trait_scores={letter: 1}))
        db.session.add(Option(question_id=q.id, text="Not really", trait_scores={}))


def seed_aptitude(level, items, start_order):
    for i, (skill, text, options) in enumerate(items):
        q = Question(level=level, text=text, category='aptitude', order=start_order + i)
        db.session.add(q)
        db.session.flush()
        for opt_text, is_correct in options:
            trait = {skill: 1} if is_correct else {}
            db.session.add(Option(question_id=q.id, text=opt_text, trait_scores=trait))


with app.app_context():
    Option.query.delete()
    Question.query.delete()
    db.session.commit()

    seed_riasec('10th', RIASEC_10TH)
    seed_aptitude('10th', APTITUDE_10TH, start_order=100)
    seed_riasec('12th', RIASEC_12TH)
    seed_aptitude('12th', APTITUDE_12TH, start_order=100)

    db.session.commit()
    print("Seeded successfully!")
    print("10th:", Question.query.filter_by(level='10th').count(), "questions")
    print("12th:", Question.query.filter_by(level='12th').count(), "questions")