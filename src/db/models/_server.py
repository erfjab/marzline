from enum import StrEnum
from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy import (
    Integer,
    String,
    JSON,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.ext.hybrid import hybrid_property
from ..core import Base


class ServerType(StrEnum):
    MARZBAN = "marzban"
    MARZNESHIN = "marzneshin"


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    remark: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    enable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    type: Mapped[ServerType] = mapped_column(String(32), nullable=False)
    config: Mapped[Dict] = mapped_column(JSON, default=dict, nullable=False)
    access: Mapped[str] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=datetime.now, nullable=True
    )

    @property
    def kb_remark(self) -> str:
        """Get remark with status indicator"""
        return f"{'🟢' if self.enable else '🔴'} {self.remark}"

    @hybrid_property
    def is_available(self) -> bool:
        """Check if server is available for new agencies"""
        return self.enable and self.access

    def format(self) -> dict:
        return {
            "remark": self.remark,
            "enable": self.enable,
            "type": self.type,
            "config": "\n".join(f"{k}:{v}" for k, v in self.config.items()),
        }

    @classmethod
    def get_by_id(cls, db: Session, id: int) -> Optional["Server"]:
        """Get server by ID"""
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_remark(cls, db: Session, remark: str) -> Optional["Server"]:
        """Get server by Remark"""
        return db.query(cls).filter(cls.remark == remark).first()

    @classmethod
    def get_all(
        cls,
        db: Session,
        *,
        is_available: Optional[bool] = None,
        enable: Optional[bool] = None,
    ) -> List["Server"]:
        """Get servers with optional filters"""
        query = db.query(cls).order_by(cls.id)

        if is_available is not None:
            query = query.filter(cls.is_available == is_available)
        if enable is not None:
            query = query.filter(cls.enable == enable)

        return query.all()

    @classmethod
    def create(
        cls,
        db: Session,
        *,
        remark: str,
        type: ServerType,
        config: Dict,
        access: Optional[str] = None,
    ) -> "Server":
        """Create a new server"""
        server = cls(
            remark=remark,
            type=type,
            config=config,
            access=access,
        )
        db.add(server)
        db.flush()
        return server

    @classmethod
    def update(
        cls,
        db: Session,
        *,
        server_id: int,
        remark: Optional[str] = None,
        enable: Optional[bool] = None,
        config: Optional[Dict] = None,
        access: Optional[str] = None,
    ) -> Optional["Server"]:
        """Update server properties"""
        server = cls.get_by_id(db, server_id)
        if not server:
            return None

        if remark is not None:
            server.remark = remark
        if enable is not None:
            server.enable = enable
        if config is not None:
            server.config = config
        if access is not None:
            server.access = access

        return server

    @classmethod
    def remove(cls, db: Session, server_id: int) -> bool:
        server = cls.get_by_id(db, server_id)
        if not server:
            return True
        db.delete(server)
        db.flush()
        return True
