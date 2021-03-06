from application import app, db, login_manager, login_required
from flask import redirect, render_template, request, url_for
from flask_login import current_user
from application.chores.models import Chore
from application.instances.models import Instance
from application.groups.models import Group
from application.chores.forms import ChoreForm

@app.route("/chores/new/<int:group_id>")
@login_required
def chores_form(group_id):

    g = Group.query.get(group_id)
    if g.creator_id !=  current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()
        
    return render_template("chores/new.html", form=ChoreForm(), group_id=group_id)


@app.route("/chores/edit/<int:chore_id>/")
@login_required
def chores_edit_form(chore_id):
    c = Chore.query.get(chore_id)
    g = Group.query.get(c.group_id)

    if g.creator_id !=  current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()

    return render_template("chores/edit.html", chore = Chore.query.get(chore_id), form=ChoreForm())

@app.route("/chores/<int:chore_id>/", methods=["POST"])
@login_required
def chores_edit(chore_id):
    c = Chore.query.get(chore_id)
    g = Group.query.get(c.group_id)

    if g.creator_id !=  current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()

    form = ChoreForm(request.form)

    if not form.validate():
        return render_template("chores/edit.html", chore = c, form=form)
    c.name = form.name.data
    c.points = form.points.data
    db.session().commit()

    return redirect(url_for("groups_view", group_id=c.group_id))

@app.route("/chores/delete/<int:chore_id>/", methods=["POST"])
@login_required
def chores_delete(chore_id):

    c = Chore.query.get(chore_id)
    g = Group.query.get(c.group_id)

    if g.creator_id !=  current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()

    Instance.query.filter_by(chore_id = chore_id).delete()
    db.session.delete(c)
    db.session().commit()

    return redirect(url_for("groups_view", group_id=c.group_id))


@app.route("/chores/group/<int:group_id>", methods=["POST"])
@login_required
def chores_create(group_id):

    g = Group.query.get(group_id)
    if g.creator_id !=  current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()

    form = ChoreForm(request.form)

    if not form.validate():
        return render_template("chores/new.html", form=form, group_id = group_id)

    c = Chore(form.name.data, form.points.data, group_id)

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("groups_view", group_id=group_id))
