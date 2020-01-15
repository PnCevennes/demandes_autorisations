'''
    Variables utilisées par l'ensemble de l'application
'''
from flask_sqlalchemy import SQLAlchemy


"""
    Création de la base avec sqlalchemy
"""

db = SQLAlchemy()

"""
    Requetes utilisées par l'application
"""

SUB_Q = """
 SELECT a.id, a.num_dossier,
            date_part('YEAR'::text, a.d_ar_dossier_complet)::int AS annee,
            a.thematique,
            a.objet,
            a.type_demande,
            a.d_ar_refus,
            a.nature,
            COALESCE(a.d_reponse::text, a.lien_reponse::text, a.num_document_reponse::text) AS rep,
            a.avis_interne,
            p.nom_complet as nom_petitionnaire,
            instructeur, type_reponse
           FROM autorisations.suivi_autorisations a
           JOIN autorisations.v_petitionnaires p
           ON a.petitionnaire = p.id
"""

SUB_Q_SPLIT_MASSIFS = """
 SELECT a.id, a.num_dossier,
            regexp_split_to_table(a.massif::text, ','::text) AS massif,
            date_part('YEAR'::text, a.d_ar_dossier_complet)::int AS annee,
            a.thematique,
            a.objet,
            a.type_demande,
            a.d_ar_refus,
            a.nature,
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
    count(data.id) AS nb_demandes,
    count(data.id) - count(data.rep) AS nb_en_cours,
    count(data.rep) AS nb_reponse,
    count(data.d_ar_refus) AS nb_refus,
    count(data.avis_interne) FILTER (WHERE data.avis_interne::text = 'Favorable'::text) AS avis_int_favorable,
    count(data.avis_interne) FILTER (WHERE data.avis_interne::text = 'Préconisation'::text) AS avis_int_preconisation,
    count(data.avis_interne) FILTER (WHERE data.avis_interne::text = 'Défavorable'::text) AS avis_int_defavorable
   FROM data
   {};
"""

COLUMNS = {
    "massif": {"order": 1, "checked": True, "label": "Massif"},
    "thematique": {"order": 2, "checked": True, "label": "Thematique"},
    "objet": {"order": 3, "checked": True, "label": "Objet"},
    "nature": {"order": 4, "checked": False, "label": "Nature"},
    "type_demande": {"order": 5, "checked": True, "label": "Type de demande"},
    "annee": {"order": 6, "checked": True, "label": "Année"},
    "nom_petitionnaire": {"order": 7, "checked": False, "label": "Nom petitionnaire"},
    "instructeur": {"order": 8, "checked": False, "label": "Instructeur"},
    "num_dossier": {"order": 9, "checked": False, "label": "Num dossier"},
    "type_reponse": {"order": 10, "checked": False, "label": "Type de réponse"}
}

QUERY_CONST = """
    SELECT c.id, num_rapport,  p.nom_complet as auteur, referent,
        c.thematique, type_constatation, date_constatation,
        suites_donnees, nature_constatation,
        type_arbitage, d_rapport_manquement,
        d_mise_demeure, sat.num_dossier as num_autorisation, type_procedure,
        date_cloture, date_regularisation,
        c.nom_communes, c.massif, c.meta_create_date::date
    FROM autorisations.constatations c
    LEFT OUTER JOIN autorisations.v_petitionnaires p
    ON p.id = c.auteur
    LEFT OUTER JOIN autorisations.suivi_autorisations sat
    ON sat.id = c.id_autorisation
    ORDER BY c.id DESC
"""
