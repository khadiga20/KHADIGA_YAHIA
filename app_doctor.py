from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  


def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",  
        database="diga_clinic"
    )
    return conn


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/choose_role', methods=['POST'])
def choose_role():
    role = request.form['role']
    session['role'] = role
    if role == 'doctor':
        return redirect('/doctor_dashboard')
    elif role == 'patient':
        return redirect('/patient_dashboard')
    return redirect('/')


@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'role' in session and session['role'] == 'doctor':
        return render_template('doctor_dashboard.html')
    return redirect('/')


@app.route('/patient_dashboard')
def patient_dashboard():
    if 'role' in session and session['role'] == 'patient':
        return render_template('patient_dashboard.html')
    return redirect('/')


@app.route('/submit_doctor', methods=['GET', 'POST'])
def submit_doctor():
    if 'role' in session and session['role'] == 'doctor':
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            specialty_id = request.form['specialty_id']
            price = request.form['price']
            gender = request.form['gender']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO doctors (name, phone, email, specialty_id, price, gender)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, phone, email, specialty_id, price, gender))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/submit_doctor')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM specialties")
        specialties = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('submit_doctor.html', specialties=specialties)
    return redirect('/')

@app.route('/submit_patient', methods=['GET', 'POST'])
def submit_patient():
    if 'role' in session and session['role'] == 'patient':
        if request.method == 'POST':
            owner_name = request.form['owner_name']
            owner_phone = request.form['owner_phone']
            owner_email = request.form['owner_email']
            anim_name = request.form['anim_name']
            anim_type = request.form['anim_type']
            anim_age = request.form['anim_age']
            anim_problem = request.form['anim_problem']
            anim_gendar = request.form['anim_gendar']
            doctor_id = request.form['doctor_id']
            appointment_date = request.form['appointment_date']  
            appointment_time = request.form['appointment_time']  

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO animals (owner_name, owner_phone, owner_email, anim_name, anim_type, anim_age, anim_problem, anim_gendar, doctor_id, appointment_date, appointment_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (owner_name, owner_phone, owner_email, anim_name, anim_type, anim_age, anim_problem, anim_gendar, doctor_id, appointment_date, appointment_time))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/submit_patient')
        
        return render_template('submit_patient.html')
    return redirect('/')



@app.route('/submit_specialty', methods=['GET', 'POST'])
def submit_specialty():
    if 'role' in session and session['role'] == 'doctor':
        if request.method == 'POST':
            spe_name = request.form['spe_name']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO specialties (spe_name) VALUES (%s)", (spe_name,))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/submit_specialty')
        
        return render_template('submit_specialty.html')
    return redirect('/')


@app.route('/specialties_and_doctors')
def specialties_and_doctors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            specialties.spe_id AS specialty_id,
            specialties.spe_name AS specialty_name,
            doctors.doctor_id AS doctor_id,
            doctors.name AS doctor_name
        FROM 
            doctors
        JOIN 
            specialties
        ON 
            doctors.specialty_id = specialties.spe_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('specialties_and_doctors.html', results=results)
@app.route('/appointments')
def appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            animals.anim_name AS patient_name,
            animals.owner_name AS owner_name,
            animals.anim_problem AS problem,
            doctors.name AS doctor_name,
            animals.appointment_date AS appointment_date,
            animals.appointment_time AS appointment_time
        FROM 
            animals
        JOIN 
            doctors 
        ON 
            animals.doctor_id = doctors.doctor_id
    """
    cursor.execute(query)
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('appointments.html', appointments=appointments)
@app.route('/specialties')
def specialties():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
  
    query = "SELECT spe_id AS specialty_id, spe_name AS specialty_name FROM specialties"
    cursor.execute(query)
    specialties = cursor.fetchall()
    
   
    seen = set()
    unique_specialties = []
    for specialty in specialties:
        if specialty['specialty_name'] not in seen:
            unique_specialties.append(specialty)
            seen.add(specialty['specialty_name'])
    
    cursor.close()
    conn.close()
    
    
    return render_template('specialties.html', Specialty=unique_specialties)



if __name__ == '__main__':
    app.run(debug=True)
