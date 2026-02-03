from dataclasses import dataclass

@dataclass
class Album:
    id: int
    title: str
    artist_id:str
    durata:float

    def __str__(self):
        return f"id: {self.id}, title: {self.title}"

    def __repr__(self):
        return f"id: {self.id}, title: {self.title}"

    def __hash__(self):
        return hash(self.id)