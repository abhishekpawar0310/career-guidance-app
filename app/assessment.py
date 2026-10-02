from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app import db
from app.models import Question, Option, AssessmentResult
from app.recommender import recommend_careers, get_courses_for_career
from app.pdf_report import generate_report_pdf

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment')


@assessment_bp.route('/take', methods=['GET', 'POST'])
@login_required
def take():
    if not current_user.education_level:
        flash('Please complete your profile before taking the assessment.', 'danger')
        return redirect(url_for('dashboard.home'))

    level = current_user.education_level

    if request.method == 'POST':
        questions = Question.query.filter_by(level=level).all()

        riasec_totals = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
        riasec_counts = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
        aptitude_totals = {"logical": 0, "verbal": 0, "numerical": 0}
        aptitude_counts = {"logical": 0, "verbal": 0, "numerical": 0}

        for q in questions:
            selected_id = request.form.get(f'q{q.id}')
            if not selected_id:
                continue

            option = Option.query.get(int(selected_id))
            if not option:
                continue

            # figure out which trait/skill this question measures
            target_key = None
            for opt in q.options:
                if opt.trait_scores:
                    target_key = list(opt.trait_scores.keys())[0]
                    break
            if not target_key:
                continue

            score = option.trait_scores.get(target_key, 0)

            if q.category == 'interest':
                riasec_totals[target_key] += score
                riasec_counts[target_key] += 1
            else:
                aptitude_totals[target_key] += score
                aptitude_counts[target_key] += 1

        riasec_percent = {
            k: round((riasec_totals[k] / riasec_counts[k]) * 100, 1) if riasec_counts[k] else 0
            for k in riasec_totals
        }
        aptitude_percent = {
            k: round((aptitude_totals[k] / aptitude_counts[k]) * 100, 1) if aptitude_counts[k] else 0
            for k in aptitude_totals
        }

        recommended = recommend_careers(riasec_percent, aptitude_percent, level, top_n=5)

        result = AssessmentResult(
            user_id=current_user.id,
            level=level,
            riasec_scores=riasec_percent,
            aptitude_scores=aptitude_percent,
            recommended_careers=recommended
        )
        db.session.add(result)
        db.session.commit()

        return redirect(url_for('assessment.result', result_id=result.id))

    questions = Question.query.filter_by(level=level).order_by(Question.category, Question.order).all()
    return render_template('assessment.html', questions=questions, level=level)


@assessment_bp.route('/result/<int:result_id>')
@login_required
def result(result_id):
    result = AssessmentResult.query.get_or_404(result_id)
    if result.user_id != current_user.id:
        flash("You don't have access to that result.", "danger")
        return redirect(url_for('dashboard.home'))

    career_courses = {}
    for career in result.recommended_careers:
        career_courses[career['career_id']] = get_courses_for_career(career['career_id'])

    return render_template('result_raw.html', result=result, career_courses=career_courses)


@assessment_bp.route('/result/<int:result_id>/download')
@login_required
def download_result(result_id):
    result = AssessmentResult.query.get_or_404(result_id)
    if result.user_id != current_user.id:
        flash("You don't have access to that result.", "danger")
        return redirect(url_for('dashboard.home'))

    career_courses = {}
    for career in result.recommended_careers:
        career_courses[career['career_id']] = get_courses_for_career(career['career_id'])

    buffer = generate_report_pdf(current_user, result, career_courses)
    filename = f"CareerCompass_Report_{result.created_at.strftime('%Y%m%d')}.pdf"
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)