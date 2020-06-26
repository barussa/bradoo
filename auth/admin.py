from flask import Blueprint
from auth import login_required
 
admin = Blueprint("admin",__name__)
 
@admin.route("/admin")
@login_required
def painel():
    return "Tela de admin"
