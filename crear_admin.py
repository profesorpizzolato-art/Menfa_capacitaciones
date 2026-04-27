from database_manager import Session, inicializar_sistema
from models import Usuario

def crear_primer_admin():
    # 1. Nos aseguramos de que las tablas existan
    inicializar_sistema()
    session = Session()

    # 2. Datos de tu usuario (Podés cambiarlos si querés)
    email_admin = "admin@menfa.com.ar"
    password_admin = "admin123" # Luego la podés cambiar desde la base

    # 3. Verificamos si ya existe para no duplicar
    existe = session.query(Usuario).filter_by(email=email_admin).first()

    if not existe:
        nuevo_admin = Usuario(
            nombre="Fabricio Pizzolato",
            email=email_admin,
            password=password_admin,
            rol="admin"
        )
        session.add(nuevo_admin)
        session.commit()
        print(f"✅ Usuario {nuevo_admin.nombre} creado con éxito.")
        print(f"📧 Email: {email_admin}")
        print(f"🔑 Pass: {password_admin}")
    else:
        print("⚠️ El usuario administrador ya existe.")

    session.close()

if __name__ == "__main__":
    crear_primer_admin()
