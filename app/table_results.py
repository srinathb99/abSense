from flask_table import Table, Col
 
class Results(Table):
    id = Col('ID', show=False)
    student_username = Col('Student')
    faculty_username = Col('Faculty', show=False)
    from_date = Col('From')
    to_date = Col('To')
    reason = Col('Reason')
    type_of_leave = Col('Type of Leave')
    leave_status = Col('Leave Status')