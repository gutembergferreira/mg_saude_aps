from backend.app.db.session import SessionLocal
from backend.app.seed import seed_dados_demo, seed_indicadores, seed_municipios, seed_usuarios


def run_all():
    with SessionLocal() as db:
        seed_municipios.seed(db)
        seed_indicadores.seed(db)
        seed_usuarios.seed(db)
        seed_dados_demo.seed(db)


if __name__ == "__main__":
    run_all()
    print("Seeds executados com sucesso.")
