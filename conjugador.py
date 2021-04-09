import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('conjugador', __name__, url_prefix='/conjugador')

@bp.route('/settings', methods=('GET', 'POST'))
def settings():
    liste_des_temps = ['Présent',
                          'Passé composé',
                          'Imparfait',
                          'Plus-que-parfait',
                          'Passé simple',
                          'Passé antérieur',
                          'Futur simple',
                          'Futur antérieur',
                          'Conditionnel présent',
                          'Conditionnel passé',
                          'sub_Présent',
                          'sub_Passé',
                          'sub_Imparfait']
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    else:
        username = session.get('username')
    db = get_db()
    temps_cochés=db.execute(f'SELECT * FROM temps WHERE username="{username}"').fetchone()
    print(temps_cochés[1::])
    liste_temps = list(temps_cochés[1::]) #[['presente',True], ['preterito',True]]

    if request.method == 'POST':
        for i in range(len(liste_des_temps)):
            #temps[1] = request.form[temps[0]]
            if liste_des_temps[i] in request.form:
                liste_temps[i]=1
            else:
                liste_temps[i]=0

        liste_temps_sql =[]
        for i in range(len(liste_temps)):
            liste_temps_sql.append(f"{liste_temps[i]}")
        print(", ".join(liste_temps_sql))
        username = session.get('username')
        db.execute(f"""UPDATE temps SET présent={liste_temps_sql[0]},
            'passé-composé'={liste_temps_sql[1]},
            imparfait={liste_temps_sql[2]},
            'plus-que-parfait'={liste_temps_sql[3]},
            'passé-simple'={liste_temps_sql[4]},
            'passé-antérieur'={liste_temps_sql[5]},
            'futur-simple'={liste_temps_sql[6]},
            'futur-antérieur'={liste_temps_sql[7]},
            'conditionnel-présent'={liste_temps_sql[8]},
            'conditionnel-passé'={liste_temps_sql[9]},
            'sub_présent'={liste_temps_sql[10]},
            'sub_passé'={liste_temps_sql[11]},
            'sub_imparfait'={liste_temps_sql[12]}
            WHERE username = '{username}'""")
        db.commit()
        return redirect(url_for('conjugador.quizz'))

    return render_template('conjugador/settings.html',liste_temps = liste_temps, len = len(liste_temps), ldt = liste_des_temps)

@bp.route('/', methods=('GET', 'POST'))
def quizz():

    return render_template('conjugador/quizz.html')