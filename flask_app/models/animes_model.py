from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model
from flask import flash


class Anime:
    db_name = "users_anime_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.quality = data["quality"]
        self.date_added= data["date_added"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @classmethod
    def add_anime(cls, data):
        query = """
        INSERT INTO animes
        (name, description, quality, date_added, user_id)
        VALUES (%(name)s, %(description)s, %(quality)s, %(date_added)s, %(user_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def get_all_animes_with_users(cls, data):
        query = """
        SELECT * FROM animes
        JOIN users
        ON animes.user_id = users.id
        """

        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        
        anime_obj_list = []

        for each_anime_dic in results:
            new_anime_obj = cls(each_anime_dic)
            new_user_dic = {
                "id": each_anime_dic["users.id"],
                "first_name": each_anime_dic["first_name"],
                "last_name": each_anime_dic["last_name"],
                "email": each_anime_dic["email"],
                "password": "",
                "created_at": each_anime_dic["users.created_at"],
                "updated_at": each_anime_dic["users.updated_at"]
            }
            new_user_obj = users_model.User(new_user_dic)
            new_anime_obj.user = new_user_obj
            anime_obj_list.append(new_anime_obj)

        return anime_obj_list


    @classmethod
    def get_all_animes_with_one_user(cls, data):
        query = """
        SELECT * FROM animes
        JOIN users
        ON animes.user_id = user_id
        Where users.id=%(id)s
        """

        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        
        anime_obj_list = []

        for each_anime_dic in results:
            new_anime_obj = cls(each_anime_dic)
            new_user_dic = {
                "id": each_anime_dic["users.id"],
                "first_name": each_anime_dic["first_name"],
                "last_name": each_anime_dic["last_name"],
                "email": each_anime_dic["email"],
                "password": "",
                "created_at": each_anime_dic["users.created_at"],
                "updated_at": each_anime_dic["users.updated_at"]
            }
            new_user_obj = users_model.User(new_user_dic)
            new_anime_obj.user = new_user_obj
            anime_obj_list.append(new_anime_obj)

        return anime_obj_list


    @classmethod
    def get_one_anime_with_user(cls, data):
        query = """
        SELECT * FROM animes
        JOIN users ON animes.user_id = users.id 
        WHERE animes.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        anime_dictionary = results[0]
        #new
        if not results:
            return None

        new_anime = cls(anime_dictionary)
        new_user_dic = {
            "id": anime_dictionary["users.id"],
            "first_name": anime_dictionary["first_name"],
            "last_name": anime_dictionary["last_name"],
            "email": anime_dictionary["email"],
            "password": "",
            "created_at": anime_dictionary["users.created_at"],
            "updated_at": anime_dictionary["users.updated_at"]
        }
        user_obj = users_model.User(new_user_dic)
        new_anime.user = user_obj

        return new_anime

    @classmethod
    def edit_anime(cls, data):
        query = """
        UPDATE animes
        SET
        name = %(name)s,
        description = %(description)s,
        quality = %(quality)s, 
        date_added = %(date_added)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_animes(cls, data):
        query = "DELETE FROM animes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def val_animes(form_data):
        is_valid = True

        # Validate name
        if len(form_data["name"]) < 3:
            is_valid = False
            flash("name min 3 characters")

        if len(form_data["description"]) < 8:
            is_valid = False
            flash("description min 8 characters")



        if len(form_data["quality"]) <4:
            is_valid = False
            flash("quality min 4 characters")

        # Validate reason
        if len(form_data["date_added"]) < 1:
            is_valid = False
            flash("date_added must be valid")

        return is_valid
