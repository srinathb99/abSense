from flask_table import Table, Col
 
class Results(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed', 'table-hover']
    id = Col('ID')
    student_username = Col('Student')
    faculty_username = Col('Faculty', show=False)
    from_date = Col('From')
    to_date = Col('To')
    reason = Col('Reason')
    type_of_leave = Col('Type of Leave')
    leave_status = Col('Leave Status')