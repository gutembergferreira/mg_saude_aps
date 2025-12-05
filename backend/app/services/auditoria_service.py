from datetime import datetime
from typing import Optional

from fastapi import Request
from sqlalchemy.orm import Session

from ..models.app import AuditoriaAcesso, Usuario


def log_audit_access(
    db: Session,
    request: Request,
    user: Optional[Usuario],
    descricao: str,
    sucesso: bool = True,
) -> None:
    perfil_nome = user.perfil.nome if user and user.perfil else None
    registro = AuditoriaAcesso(
        usuario_id=user.id if user else None,
        perfil_nome=perfil_nome,
        endpoint=request.url.path,
        metodo_http=request.method,
        timestamp=datetime.utcnow(),
        ip_cliente=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        descricao=descricao,
        sucesso=sucesso,
    )
    db.add(registro)
    db.commit()
