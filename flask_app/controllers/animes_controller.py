from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import animes_model, users_model

@app.route("/dashboard")
def all_trees():
    # if "user_id" not in session:
    #     return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("all_anime.html", 
        logged_user = users_model.User.get_userid(data),
        all_animes = animes_model.Anime.get_all_animes_with_users(data)) 
    
@app.route("/anime/new")
def new_anime():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template('add_anime.html', 
    logged_user = users_model.User.get_userid(data),
    all_animes = animes_model.Anime.get_all_animes_with_users(data))
    
    
@app.route("/anime/delete/<int:id>", methods=["POST"])
def delete_trees(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": id
    }
    animes_model.Anime.delete_animes(data)
    return redirect('/dashboard')
    
@app.route("/anime/add_to_db", methods=["POST"])
def add_anime_db():
    if "user_id" not in session:
        return redirect('/')
    if not animes_model.Anime.val_animes(request.form):
        return redirect('/anime/new')
    animes_model.Anime.add_anime(request.form)
    return redirect('/dashboard')
    
    
@app.route("/user/<int:id>")
def view_tree(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": id,
    }
    return render_template('view_anime.html',
    this_anime = animes_model.Anime.get_one_anime_with_user(data))
    


@app.route("/edit/<int:id>")
def edit_anime(id):
    print("entered edit_anime function")
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id,
    }
    return render_template("edit_anime.html",
    this_anime = animes_model.Anime.get_one_anime_with_user(data))
    
@app.route("/anime/edit/<int:id>", methods=["POST"])
def edit_anime_db(id):
    if "user_id" not in session:
        return redirect('/')
    if not animes_model.Anime.val_animes(request.form):
        return redirect(f'/edit/{id}')
    animes_model.Anime.edit_anime(request.form)
    return redirect('/dashboard')

@app.route("/show/<int:id>")
def show_anime(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": id,
    }
    return render_template('show_user_anime.html',
    this_animee = animes_model.Anime.get_one_anime_with_user(data))
    
@app.route("/details/<int:anime_id>")
def show_user_anime(anime_id):
    animes = animes_model.Anime.get_one_anime_with_user({"id": anime_id})

    return render_template('show_user_anime.html', animes=animes)

@app.route("/user/account")
def get_my_animes():
    if "user_id" not in session:
        return redirect('/')
    data={
        "id": session["user_id"]}
    
    all_animes=animes_model.Anime.get_all_animes_with_one_user(data)
    return render_template("view_anime.html", all_animes=all_animes)

