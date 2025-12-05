from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db.base import Base
from ..db.session import get_db
from ..main import app
from ..models.app import Usuario
from ..models.dw import DimIndicador, DimMunicipio
from ..seed.run_all_seeds import run_all

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
SessionTesting = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine.execution_options(schema_translate_map={"dw": None}),
)


def override_get_db():
    db = SessionTesting()
    try:
        yield db
    finally:
        db.close()


def setup_module(_module):
    with engine.begin() as conn:
        conn = conn.execution_options(schema_translate_map={"dw": None})
        Base.metadata.create_all(bind=conn)
    app.dependency_overrides[get_db] = override_get_db
    run_all()


client = TestClient(app)


def test_seed_municipio_indicador_usuario():
    db = SessionTesting()
    try:
        mun = db.query(DimMunicipio).first()
        ind = db.query(DimIndicador).first()
        user = db.query(Usuario).first()
        assert mun is not None
        assert ind is not None
        assert user is not None
    finally:
        db.close()
