'''
    Route permettant la visualisation des bilans concernant
    les autorisations et les rapports de constatations
'''

from flask import (
    render_template,
    Blueprint, request
)
from sqlalchemy import text

from app.env import db, SUB_Q, SUB_Q_SPLIT_MASSIFS, QUERY, COLUMNS, QUERY_CONST


route = Blueprint('autorisations', __name__)


@route.route('/', methods=['GET', 'POST'])
def get_stat_autorisations():
    '''
        Route bilan des autorisations
    '''
    subquery = SUB_Q
    subquery_massifs = SUB_Q_SPLIT_MASSIFS

    filters = []

    if "date-min" in request.form:
        if request.form['date-min']:
            filters.append(
                "a.d_ar_dossier_complet >= '" + request.form["date-min"] + "'"
            )

    if "date-max" in request.form:
        if request.form['date-max']:
            filters.append(
                "a.d_ar_dossier_complet <= '" + request.form["date-max"] + "'"
            )

    if filters:
        subquery = subquery + " WHERE " + " AND ".join(filters)
        subquery_massifs = subquery_massifs  + " WHERE " + " AND ".join(filters)

    (
        selected_columns, sql_select, sql_group_by
    ) = process_columns(request.form.getlist('columns'))

    # Statistiques
    sql_c = text(QUERY.format(subquery, "", ""))
    result_c = db.engine.execute(sql_c)

    # Tableau des résulats
    # Si la colonne massifs est spécifiée alors changement de sous requête
    if ("massif" in request.form.getlist('columns')):
        subquery = subquery_massifs
    sql_a = text(QUERY.format(subquery, sql_select, sql_group_by))
    result_a = db.engine.execute(sql_a)
    return render_template(
        'stat_autorisation.html',
        data_query_count=result_c,
        data_query_agg=result_a,
        form=request.form,
        columns=selected_columns
    )


@route.route('constatations', methods=['GET', 'POST'])
def get_constatations():
    '''
        Liste des rapports de constatations
    '''
    sql_c = text(QUERY_CONST)
    result_c = db.engine.execute(sql_c)

    return render_template(
        'constatations.html',
        data=result_c,
        columns=result_c.keys()
    )


def process_columns(form_columns):
    '''
        Traitement des colonnes demandées par l'utilisateur
    '''
    selected_columns = COLUMNS
    print(form_columns)
    if not form_columns:
        form_columns = [
            k for k in selected_columns if selected_columns[k]['checked']
        ]

    for col in selected_columns:
        if col in form_columns:
            selected_columns[col]['checked'] = True
        else:
            selected_columns[col]['checked'] = False

    check_col = [k for k in selected_columns if selected_columns[k]['checked']]
    if check_col:
        sql_select = ",".join(check_col) + ","
        sql_group_by = "GROUP BY " + sql_select[:-1]
    else:
        sql_select = ""
        sql_group_by = ""
    print(selected_columns, sql_select, sql_group_by)
    return (selected_columns, sql_select, sql_group_by)
