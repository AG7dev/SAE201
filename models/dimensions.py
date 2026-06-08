# ===== SAE 2.04 - Explorer les données de l'Assurance Maladie =====

# Import des bibliothèques ORM SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# Base déclarative pour toutes les entités du modèle
Base = declarative_base()

# ── Dimensions géographiques ────────────────────────────────────────────

class Region(Base):
    """
    Représente une région administrative.
    Contient plusieurs départements.
    """
    __tablename__ = "region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), nullable=False, unique=True)
    libelle = Column(String(100), nullable=False)

    # Relation 1-N avec Departement
    departements = relationship("Departement", backref="region")

    def __repr__(self):
        return f"{self.code} – {self.libelle}"


class Departement(Base):
    """
    Représente un département appartenant à une région.
    """
    __tablename__ = "departement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), nullable=False, unique=True)
    libelle = Column(String(100), nullable=False)

    # Clé étrangère vers Region
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)

    def __repr__(self):
        return f"{self.code} – {self.libelle}"


# ── Dimensions métier ────────────────────────────────────────────────

class ProfessionSante(Base):
    """Référence des professions de santé."""
    __tablename__ = "profession_sante"

    id = Column(Integer, primary_key=True, autoincrement=True)
    libelle = Column(String(200), nullable=False, unique=True)

    def __repr__(self):
        return self.libelle


class TrancheAge(Base):
    """Découpage par tranche d’âge."""
    __tablename__ = "tranche_age"

    id = Column(Integer, primary_key=True, autoincrement=True)
    libelle = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return self.libelle


class Sexe(Base):
    """Dimension sexe (H/F/Autre selon données)."""
    __tablename__ = "sexe"

    id = Column(Integer, primary_key=True, autoincrement=True)
    libelle = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.libelle


# ── Dimensions d’activité ──────────────────────────────────────────────

class TypeExercice(Base):
    """Type d’exercice (libéral, salarié, mixte...)."""
    __tablename__ = "type_exercice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    libelle = Column(String(200), nullable=False, unique=True)

    def __repr__(self):
        return self.libelle


class TypeSecteur(Base):
    """Secteur conventionnel (ex : secteur 1, 2...)."""
    __tablename__ = "type_secteur"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False, unique=True)
    libelle = Column(String(200), nullable=False)

    def __repr__(self):
        return f"{self.code} – {self.libelle}"


# ── Dimensions financières ──────────────────────────────────────────────

class TypeHonoraire(Base):
    """
    Hiérarchie des actes et honoraires (3 niveaux).
    Exemple : Actes > Consultations > Cabinet.
    """
    __tablename__ = "type_honoraire"

    id = Column(Integer, primary_key=True, autoincrement=True)
    niveau_1 = Column(String(80), nullable=False)
    niveau_2 = Column(String(80), nullable=True)
    niveau_3 = Column(String(80), nullable=True)

    # Unicité sur la combinaison hiérarchique
    __table_args__ = (UniqueConstraint("niveau_1", "niveau_2", "niveau_3"),)

    def __repr__(self):
        return " > ".join(filter(None, [self.niveau_1, self.niveau_2, self.niveau_3]))


class TypePrescription(Base):
    """Types de prescriptions médicales."""
    __tablename__ = "type_prescription"

    id = Column(Integer, primary_key=True, autoincrement=True)
    libelle = Column(String(200), nullable=False, unique=True)

    def __repr__(self):
        return self.libelle
    
class UserTable(Base):
    """Tables contenant les utilisateurs"""
    __tablename__ = "user_table"
    
    username = Column(String(32), primary_key=True)
    password = Column(String(64), nullable=False)
    date = Column(String(20), nullable=False)
    permissions = Column(String(16), default=None)
    
    def __repr__(self):
        return self.username
    
    