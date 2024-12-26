CREATE TABLE specialties (
    spe_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    spe_name VARCHAR(100) NOT NULL
);


CREATE TABLE doctors (
    doctor_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    specialty_id INT NOT NULL,
    price INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    FOREIGN KEY (specialty_id) REFERENCES specialties(spe_id) 
);


CREATE TABLE animals (
    anim_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(50) NOT NULL,
    owner_phone VARCHAR(50) UNIQUE,
    owner_email VARCHAR(255) NOT NULL,
    anim_name VARCHAR(30),
    anim_type VARCHAR(30),
    anim_age INT NOT NULL,
    anim_problem VARCHAR(255),
    anim_gender VARCHAR(50),
    doctor_id INT NOT NULL,
    appointment_date DATE,
    appointment_time TIME,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) 
    );
    insert into doctors (doctor_id,),
    values();

