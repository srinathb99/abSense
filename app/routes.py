"""
routing for my app
"""

from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import LoginForm, LeaveForm
from app.models import StudentUser, FacultyUser, leaves, advisor
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.table_results import Results

session = {}

@app.route('/')
@app.route('/index')
def index():
	varname = 'Guest'
	if current_user.is_authenticated and session.get('user'):
		varname = session['user']
	return render_template('index.html', title='Home', name = varname)

@app.route('/caution')
def caution():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution', name = 'Guest')
	else:
		return redirect(url_for('index'), name = session['user'])

@app.route('/apply_leave', methods = ['GET', 'POST'])
def apply_leave():
	form = LeaveForm()
	fname = advisor.query.filter_by(student_username=session['user']).first().faculty_username
	if form.validate_on_submit():
		newleave = leaves(
		student_username = session['user'],
		faculty_username = fname,
		from_date = form.fromdate.data,
		to_date = form.todate.data,
		reason = form.reason.data,
		type_of_leave = form.typeofleave.data,
		leave_status = form.leavestatus.data)
		db.session.add(newleave)
		db.session.commit()
		flash('Your leave application was submitted succesfully.')
		return redirect(url_for('student_dashboard'))
	return render_template('apply_leave.html', title = 'Apply Leave', form = form, studentname = session['user'], facultyname = fname, name = session['user'])

@app.route('/view_leave')
def view_leave():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution')
	elif session['type'] == 'faculty':
		return render_template('caution.html', title='Caution')
	items = leaves.query.filter_by(student_username=session['user'])
	table = Results(items, border = True)
	return render_template('results.html', table = table, name = session['user'])

@app.route('/view_leave_faculty')
def view_leave_faculty():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution')
	elif session['type'] == 'student':
		return render_template('caution.html', title='Caution')
	items = leaves.query.filter_by(faculty_username=session['user'])
	table = Results(items, border = True)
	return render_template('results_faculty.html', table = table, name = session['user'])

@app.route('/student_dashboard', methods = ['GET', 'POST'])
def student_dashboard():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution', name = 'Guest')
	elif session['type'] == 'faculty':
		return render_template('caution.html', title='Caution', name = session['user'])
	else:
		return render_template('student_dash.html', title='Student Dashboard', name = session['user'])

@app.route('/student_login', methods = ['GET', 'POST'])
def student_login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	varname = 'Guest'
	
	if form.validate_on_submit():
		user = StudentUser.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('student_login'))
		flash('You were succesfully logged in.')
		login_user(user)
		session['user'] = form.username.data
		session['type'] = 'student'
		varname = session['user']
		return redirect(url_for('student_dashboard'))
	return render_template('student_login.html', title = 'Sign In', form = form, name = varname)

@app.route('/faculty_login', methods = ['GET', 'POST'])
def faculty_login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	varname = 'Guest'
	if form.validate_on_submit():
		user = FacultyUser.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('faculty_login'))
		flash('You were succesfully logged in.')
		login_user(user)
		session['user'] = form.username.data
		session['type'] = 'faculty'
		varname = session['user']
		return redirect(url_for('faculty_dashboard'))
	return render_template('faculty_login.html', title = 'Sign In', form = form, name = varname)

@app.route('/faculty_dashboard', methods = ['GET', 'POST'])
def faculty_dashboard():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution', name = 'Guest')
	elif session['type'] == 'student':
		return render_template('caution.html', title='Caution', name = session['user'])
	else:
		return render_template('faculty_dash.html', title='Faculty Dashboard', name = session['user'])

@app.route('/logout')
def logout():
	logout_user()
	flash('You were logged out succesfully.')
	return redirect(url_for('index'))