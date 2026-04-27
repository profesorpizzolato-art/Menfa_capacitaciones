from database_manager import Session, inicializar_sistema
from models import Usuario

def crear_primer_admin():
    inicializar_sistema()
    session = Session()

    # EL CORREO OFICIAL DE MENFA
    email_admin = "menfacapacitaciones@gmail.com" 
    password_admin = "Menfa2026" # Podés poner la que quieras aquí

    existe = session.query(Usuario).filter_by(email=email_admin).first()

    if not existe:
        nuevo_admin = Usuario(
            nombre="Administración MENFA",
            email=email_admin,
            password=password_admin,
            rol="admin"
        )
        session.add(nuevo_admin)
        session.commit()
        print(f"✅ CRM Ligado a: {email_admin}")
    else:
        # Si ya existía con otro nombre, lo actualizamos
        existe.email = email_admin
        session.commit()
        print("⚠️ Usuario actualizado con el correo oficial.")

    session.close()

if __name__ == "__main__":
    crear_primer_admin()
