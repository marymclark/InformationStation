# Direct to all the forms

@app.route('/form/continuation')
def continuationForm():
    render_template('forms/continuation.html')

@app.route('/form/internship')
def internshipForm():
    render_template('forms/internship.html')

@app.route('/form/admission')
def admissionForm():
    render_template('forms/admission.html')