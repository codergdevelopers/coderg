from flask import Blueprint, render_template

from flask_qa.models import Projects
from flask_qa.extensions import db

from config.config import params

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html',)


@main.route("/about")
def about():
    return render_template("about.html", params=params)


@main.route("/contact")
def contact():
    return render_template("contact.html")


@main.route("/projects")
def display_projects():
    categories = set()
    projects = Projects.query.filter_by().all()

    # Getting all the available categories
    for project in projects:
        categories.add(project.category)

    return render_template("projects.html", categories=list(categories), projects=projects)


@main.route("/blog")
def blog():
    return render_template("blog.html")








# ORIGINAL FILES DISCARDED CONTENTS

# @main.route('/ask', methods=['GET', 'POST'])
# @login_required
# def ask():
#     if request.method == 'POST':
#         question = request.form['question']
#         expert = request.form['expert']
#
#         question = Question(
#             question=question,
#             expert_id=expert,
#             asked_by_id=current_user.id
#         )
#
#         db.session.add(question)
#         db.session.commit()
#
#         return redirect(url_for('main.index'))
#
#     experts = User.query.filter_by(expert=True).all()
#
#     context = {
#         'experts' : experts
#     }
#
#     return render_template('ask.html', **context)
#
# @main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
# @login_required
# def answer(question_id):
#     if not current_user.expert:
#         return redirect(url_for('main.index'))
#
#     question = Question.query.get_or_404(question_id)
#
#     if request.method == 'POST':
#         question.answer = request.form['answer']
#         db.session.commit()
#
#         return redirect(url_for('main.unanswered'))
#
#     context = {
#         'question' : question
#     }
#
#     return render_template('answer.html', **context)
#
# @main.route('/question/<int:question_id>')
# def question(question_id):
#     question = Question.query.get_or_404(question_id)
#
#     context = {
#         'question' : question
#     }
#
#     return render_template('question.html', **context)
#
# @main.route('/unanswered')
# @login_required
# def unanswered():
#     if not current_user.expert:
#         return redirect(url_for('main.index'))
#
#     unanswered_questions = Question.query\
#         .filter_by(expert_id=current_user.id)\
#         .filter(Question.answer == None)\
#         .all()
#
#     context = {
#         'unanswered_questions' : unanswered_questions
#     }
#
#     return render_template('unanswered.html', **context)
#
# @main.route('/users')
# @login_required
# def users():
#     if not current_user.admin:
#         return redirect(url_for('main.index'))
#
#     users = User.query.filter_by(admin=False).all()
#
#     context = {
#         'users' : users
#     }
#
#     return render_template('users.html', **context)
#
# @main.route('/promote/<int:user_id>')
# @login_required
# def promote(user_id):
#     if not current_user.admin:
#         return redirect(url_for('main.index'))
#
#     user = User.query.get_or_404(user_id)
#
#     user.expert = True
#     db.session.commit()
#
#     return redirect(url_for('main.users'))



@main.route("/addprojects")
def add_projects():

    proj = Projects(category="Python", title="Hey soldier prettify my folder", language='Python', purpose='Batch rename files in a given folder. Can ignore files', working_on="Using wildcards in ignore list", link=r'https://github.com/aqdasak/Batch-Rename', author='Aqdas Ahmad Khan')
    db.session.add(proj)
    db.session.commit()

    proj = Projects(category="Java", title="Starke", language='Java', purpose='Greeting message on startup', working_on="Logic based printing of characters", link=r'https://github.com/deepanshdubey/starke', author='Aqdas Ahmad Khan (+Deepansh Dubey)')
    db.session.add(proj)
    db.session.commit()

    proj = Projects(category="Java", title="MorseCode_Decoder", language='Java', purpose='Decoding the characters of Morse Code', working_on="Identifying user inputs", link=r'https://github.com/deepanshdubey/MorseCode_Decoder', author='Deepansh Dubey')
    db.session.add(proj)
    db.session.commit()

    proj = Projects(category="WEB - D", title="Coderg Frontend", language='HTML, CSS & JS', purpose='Building a website for our society', working_on="HTML, CSS & JS", link=r'https://github.com/deepanshdubey/Coderg', author='Deepansh Dubey')
    db.session.add(proj)
    db.session.commit()

    proj = Projects(category="WEB - D", title="Coderg Backend", language='Python (flask)',
                    purpose='Backend of this website', working_on="Blogs section",
                    link=r'https://github.com/codergdevelopers/coderg', author='Aqdas Ahmad Khan')
    db.session.add(proj)
    db.session.commit()

    proj = Projects(category="WEB - D", title="React.calc", language='Javascript', purpose='Basic four function calculator', working_on="ReactJS", link=r'https://github.com/deepanshdubey/react.calc.git', author='Deepansh Dubey')
    db.session.add(proj)
    db.session.commit()

    return "New post added"


