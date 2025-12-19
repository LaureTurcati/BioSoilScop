import json
from dataclasses import dataclass, field
from typing import Self, List, Union, Optional

from log import LOG

@dataclass
class Session:
    nom_session: str
    nom_session_file: str
    choix: str
    status: str
    date_debut: Optional[str] = None
    date_fin: Optional[str] = None
    time_slots: List[str] = field(default_factory=list)

    @staticmethod
    def from_config(filepath: str) -> Self | None:
        try:
            with open(filepath, "r") as f:
                dataSession = json.load(f)
                nom_session = dataSession.get("nom_session")
                nom_session_file = dataSession.get("nom_session").replace(" ", "_")
                choix = dataSession.get("choix")
                status = dataSession.get("status")

                if choix == "plage":
                    date_debut = dataSession.get("date_debut")
                    date_fin = dataSession.get("date_fin")
                    time_slots = dataSession.get("time_slots")

                    session = Session(nom_session, nom_session_file, choix, status, date_debut, date_fin, time_slots)

                elif choix == "continue":
                    session = Session(nom_session, nom_session_file, choix, status)

                log_message_session = {
                    "message": "Paramètres de session chargés et initialisés",
                    "details": f"nom_session: {nom_session}, choix: {choix}, nom_session_file: {nom_session_file}"
                }
                LOG.info(log_message_session)
                return session
        except Exception as e:
            print(f"Erreur avec {filepath} :", e)

            log_message_error_session = {
                "message": f"Erreur avec {filepath}",
                "details": str(e)
            }
            LOG.error(log_message_error_session)
            return None