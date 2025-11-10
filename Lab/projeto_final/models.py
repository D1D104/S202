from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Comment:
    user_id: str
    texto: str
    ts: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {"user_id": self.user_id, "texto": self.texto, "ts": self.ts}

@dataclass
class Post:
    _id: Optional[str] 
    author_id: str
    titulo: str
    corpo: str
    tags: List[str]
    ts: datetime = field(default_factory=datetime.utcnow)
    comentarios: List[Comment] = field(default_factory=list)

    def to_dict(self):
        return {
            **({"_id": self._id} if self._id else {}),
            "author_id": self.author_id,
            "titulo": self.titulo,
            "corpo": self.corpo,
            "tags": self.tags,
            "ts": self.ts,
            "comentarios": [c.to_dict() for c in self.comentarios]
        }

@dataclass
class UserMeta:
    _id: str
    nome: str
    perfil: Optional[str] = None

    def to_dict(self):
        return {"_id": self._id, "nome": self.nome, "perfil": self.perfil}
