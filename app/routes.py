"""
routing for my app
"""

from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import LoginForm, LeaveForm
from app.models import StudentUser, FacultyUser, leaves
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

@app.route('/temp')
def temp():
	if not current_user.is_authenticated:
		return redirect(url_for('caution'))
	else:
		return session['user']

@app.route('/caution')
def caution():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution', name = 'Guest')
	else:
		return redirect(url_for('index'), name = session['user'])

@app.route('/apply_leave', methods = ['GET', 'POST'])
def apply_leave():
	form = LeaveForm()
	if form.validate_on_submit():
		newleave = leaves(
		student_username = session['user'],
		faculty_username = form.facultyusername.data,
		from_date = form.fromdate.data,
		to_date = form.todate.data,
		reason = form.reason.data,
		type_of_leave = form.typeofleave.data,
		leave_status = form.leavestatus.data)
		db.session.add(newleave)
		db.session.commit()
	return render_template('apply_leave.html', title = 'Apply Leave', form = form, name = session['user'])

@app.route('/view_leave')
def view_leave():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution')
	items = leaves.query.filter_by(student_username=session['user'])
	table = Results(items, border = True)
	return render_template('results.html', table = table)

@app.route('/student_dashboard', methods = ['GET', 'POST'])
def student_dashboard():
	if not current_user.is_authenticated:
		return render_template('caution.html', title='Caution')
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
		login_user(user)
		session['user'] = form.username.data
		varname = session['user']
		return redirect(url_for('student_dashboard'))
	return render_template('student_login.html', title = 'Sign In', form = form, name = varname)

@app.route('/faculty_login', methods = ['GET', 'POST'])
def faculty_login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = FacultyUser.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('faculty_login'))
		login_user(user)
		return redirect(url_for('faculty_dashboard'))
		
	return render_template('faculty_login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))