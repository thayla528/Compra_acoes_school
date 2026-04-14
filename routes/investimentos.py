
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.banco import conectar

investimentos_bp = Blueprint('investimentos', __name__)

@investimentos_bp.route("/simulador", methods=["GET", "POST"])
def simulador():
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        tipo = request.form.get('tipo')
        valor = float(request.form.get('valor_investido', 0))
        taxa = float(request.form.get('taxa', 0))
        tempo = int(request.form.get('tempo', 0))

        lucro = valor * ((taxa / 100) / 12) * tempo

        cursor.execute("""
            INSERT INTO investimentos (usuario, tipo, valor_investido, taxa, tempo, lucro)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session['usuario'], tipo, valor, taxa, tempo, lucro))

        conn.commit()

    cursor.execute("SELECT * FROM investimentos WHERE usuario = ?", (session['usuario'],))
    dados = cursor.fetchall()
    conn.close()

    return render_template("simulador.html", investimentos=dados)