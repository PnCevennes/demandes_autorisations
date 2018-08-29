
from flask_sqlalchemy import SQLAlchemy

from config import config

"""
Création de la base avec sqlalchemy
"""

db = SQLAlchemy()

SUB_Q = """
 SELECT a.id, a.num_dossier,
            regexp_split_to_table(a.massif::text, ','::text) AS massif,
            date_part('YEAR'::text, a.d_ar_dossier_complet)::int AS annee,
            a.thematique,
            a.objet,
            a.type_demande,
            a.d_ar_refus,
            COALESCE(a.d_reponse::text, a.lien_reponse::text, a.num_document_reponse::text) AS rep,
            a.avis_interne, 
            p.nom_complet as nom_petitionnaire,
            instructeur, type_reponse
           FROM autorisations.suivi_autorisations a
           JOIN autorisations.v_petitionnaires p
           ON a.petitionnaire = p.id
"""

QUERY = """
 WITH data AS (
         {}
        )
 SELECT row_number() OVER () AS unique_id,
    {}
    count(*) AS nb_demandes,
    count(*) - count(data.rep) AS nb_en_cours,
    count(data.rep) AS nb_reponse,
    count(data.d_ar_refus) AS nb_refus,
    count(data.avis_interne) FILTER (WHERE data.avis_interne::text = 'Favorable'::text) AS avis_int_favorable,
    count(data.avis_interne) FILTER (WHERE data.avis_interne::text = 'Préconisation'::text) AS avis_int_preconisation,
    count(data.avis_interne) FILTER (WHERE data.avis_interne::text = 'Défavorable'::text) AS avis_int_defavorable
   FROM data
   {};
"""

COLUMNS = {
    "massif": {"checked": True, "label": "Massif"}, 
    "thematique": {"checked": True, "label": "Thematique"},
    "objet": {"checked": True, "label": "Objet"},
    "type_demande": {"checked": True, "label": "Type de demande"},
    "annee": {"checked": True, "label": "Année"},
    "nom_petitionnaire": {"checked": False, "label": "Nom petitionnaire"},
    "instructeur": {"checked": False, "label": "Instructeur"},
    "num_dossier": {"checked": False, "label": "Num dossier"},
    "type_reponse": {"checked": False, "label": "Type de réponse"}
    
}

QUERY_CONST = """
    SELECT massif, p.nom_complet, referent, num_rapport, nature_constatation, 
        suites_donnees, date_cloture, regularisation, date_regularisation, 
        code_insee, nom_communes
    FROM autorisations.constatations c
    LEFT OUTER JOIN autorisations.v_petitionnaires p
    ON p.id = c.auteur
"""


QUERY_DATE_AT = """
    SELECT massif, p.nom_complet, referent, num_rapport, nature_constatation, 
        suites_donnees, date_cloture, regularisation, date_regularisation, 
        code_insee, nom_communes
    FROM autorisations.constatations c
    LEFT OUTER JOIN autorisations.v_petitionnaires p
    ON p.id = c.auteur
"""
