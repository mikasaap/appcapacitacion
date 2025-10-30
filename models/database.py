import sqlite3
from werkzeug.security import generate_password_hash
def get_db_connection():
    conn = sqlite3.connect('academia.db')
    print('Conectado a la base de datos:', 'academia.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS  estudiantes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL UNIQUE,
            fecha_nacimiento DATE NOT NULL
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            horas INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            curso_id INTEGER NOT NULL,
            estudiante_id INTEGER NOT NULL,
            FOREIGN KEY (curso_id) REFERENCES cursos (id),
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
        )
    ''')    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            celular TEXT NOT NULL
        )
    ''')
    cursor.execute('''INSERT INTO cursos (descripcion, horas) VALUES
        ('Curso de Python', 40),    
        ('Curso de Flask', 30),
        ('Curso de SQL', 25)    
    ''')
    cursor.execute('''Insert INTO estudiantes (nombre, apellidos, fecha_nacimiento) VALUES
        ('Juan', 'Pérez', '1995-05-15'),
        ('María', 'Gómez', '1998-08-22'),
        ('Luis', 'Martínez', '1997-12-30')
    ''')
    cursor.execute('''INSERT INTO inscripciones (fecha, curso_id, estudiante_id) VALUES
        ('2023-01-10', 1, 1),
        ('2023-02-15', 2, 2),
        ('2023-03-20', 3, 3)
    ''')    

    cursor.execute(''' SELECT * FROM usuarios WHERE username = ? ''', ('admin',))
    if not cursor.fetchone():
        hashed = generate_password_hash('admin742##')
        cursor.execute('''
            INSERT INTO usuarios (username, email, password, celular)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@admin.com', hashed, '71970783'))
    conn.commit()
    conn.close()