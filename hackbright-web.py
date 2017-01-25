from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)

# @app.route('/student')
# def find_student():
#     student = request.args.get('github', 'jhacks')
#     redirect('/student/%s' % student)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    project_and_grades = hackbright.get_projects_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           project_and_grades=project_and_grades)
    return html
    # return "%s is the GitHub account for %s %s" % (github, first, last)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student-add-form")
def student_add_form():
    """Show form for adding a student."""

    return render_template("student_add_form.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    first_name = request.form.get('first_name', 'Jane')
    last_name = request.form.get('last_name', 'Hacker')
    github = request.form.get('github', 'jhacks')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('student_add.html', github=github)

@app.route("/project/<project_title>")
def get_project_details(project_title):
    """Show title and maximum grade of a porject."""
    id_number, title, description, max_grade = hackbright.get_project_by_title(project_title)
    return render_template("project_details.html",
                            title = title,
                            description = description,
                            max_grade = max_grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
