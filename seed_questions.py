from app import create_app, db
from app.models import Question, Option

app = create_app()

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

    seed_riasec('12th', RIASEC_12TH)
    seed_aptitude('12th', APTITUDE_12TH, start_order=100)

    db.session.commit()
    print("Seeded successfully!")
    print("12th:", Question.query.filter_by(level='12th').count(), "questions")