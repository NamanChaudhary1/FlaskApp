from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = []

class Student:
    def __init__(self, name, roll_no, marks):
        self._name = name
        self._roll_no = roll_no
        self._marks = marks

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise ValueError("Name must be a string")

    @property
    def roll_no(self):
        return self._roll_no

    @roll_no.setter
    def roll_no(self, value):
        if isinstance(value, int):
            self._roll_no = value
        else:
            raise ValueError("Roll number must be an integer")

    @property
    def marks(self):
        return self._marks

    @marks.setter
    def marks(self, value):
        if isinstance(value, (int, float)) and 0 <= value <= 100:
            self._marks = value
        else:
            raise ValueError("Marks must be a number between 0 and 100")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        marks = request.form['marks']
        
        # Convert roll_no and marks to their appropriate types
        try:
            roll_no = int(roll_no)
            marks = float(marks)
        except ValueError:
            return "Invalid input", 400
        
        students.append(Student(name, roll_no, marks))
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/students')
def display_students():
    return render_template('display_students.html', students=students)

@app.route('/search', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        
        # Convert roll_no to integer
        try:
            roll_no = int(roll_no)
        except ValueError:
            return "Invalid roll number", 400
        
        student = next((s for s in students if s.roll_no == roll_no), None)
        return render_template('search_student.html', student=student)
    return render_template('search_student.html', student=None)

@app.route('/update/<int:roll_no>', methods=['GET', 'POST'])
def update_student(roll_no):
    student = next((s for s in students if s.roll_no == roll_no), None)
    if request.method == 'POST':
        if student:
            name = request.form['name']
            marks = request.form['marks']
            
            # Convert marks to float
            try:
                marks = float(marks)
            except ValueError:
                return "Invalid marks", 400
            
            student.name = name
            student.marks = marks
            return redirect(url_for('display_students'))
    return render_template('update_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
