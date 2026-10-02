import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Career
from app.models import Course

RIASEC_KEYS = ['R', 'I', 'A', 'S', 'E', 'C']
APTITUDE_KEYS = ['logical', 'verbal', 'numerical']


def _vector(score_dict, keys):
    return np.array([score_dict.get(k, 0) for k in keys]).reshape(1, -1)


def _safe_cosine(vec_a, vec_b):
    sim = cosine_similarity(vec_a, vec_b)[0][0]
    return 0.0 if np.isnan(sim) else float(sim)


def recommend_careers(riasec_scores, aptitude_scores, level, top_n=5):
    """
    Ranks careers by fit using cosine similarity between the student's
    RIASEC + aptitude profile and each career's profile, then blends
    interest similarity (70%) with aptitude similarity (30%).
    """
    careers = Career.query.filter(
        (Career.suited_level == level) | (Career.suited_level == 'both')
    ).all()

    if not careers:
        return []

    student_riasec = _vector(riasec_scores, RIASEC_KEYS)
    student_apt = _vector(aptitude_scores, APTITUDE_KEYS)

    results = []
    for career in careers:
        career_riasec = _vector(career.riasec_profile or {}, RIASEC_KEYS)
        career_apt = _vector(career.aptitude_profile or {}, APTITUDE_KEYS)

        riasec_sim = _safe_cosine(student_riasec, career_riasec)
        apt_sim = _safe_cosine(student_apt, career_apt)

        final_score = (0.7 * riasec_sim) + (0.3 * apt_sim)

        results.append({
            'career_id': career.id,
            'name': career.name,
            'description': career.description,
            'match_percent': round(final_score * 100, 1),
        })

    results.sort(key=lambda x: x['match_percent'], reverse=True)
    return results[:top_n]
def get_courses_for_career(career_id):
    """Returns every course tied to a career, each with its college offerings."""
    courses = Course.query.filter_by(career_id=career_id).all()
    result = []
    for course in courses:
        offerings = []
        for cc in course.offerings:
            offerings.append({
                'college_name': cc.college.name,
                'address': cc.college.address,
                'contact': cc.college.contact,
                'fees': cc.fees,
                'apply_link': cc.apply_link or cc.college.website,
            })
        result.append({
            'course_name': course.name,
            'course_description': course.description,
            'offerings': offerings,
        })
    return result