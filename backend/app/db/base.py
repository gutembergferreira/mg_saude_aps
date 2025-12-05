from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Importa os modelos para registro no metadata do SQLAlchemy/Alembic
from ..models import dw  # noqa: F401,E402
from ..models import planejamento  # noqa: F401,E402
from ..models import app as app_models  # noqa: F401,E402
