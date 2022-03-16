#encargado de ver todo con la base de datos
from flask_app.config.mysqlconnection import connectToMySQL
import re #importamos expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash 

class User:

    def __init__(self, data):
        self.id= data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('registro').query_db(query, data)
        return result

    @staticmethod
    def valida_usuario(user):
        es_valido = True

        #validar que mi nombre sea mayor a 2 caracteres
        if len(user['first_name']) <3:
            flash("Nombre debe de tener al menos 3 caracteres", "register")
            es_valido = False

        #Vlidar que m apellido sea mayor a 2 caracterres
        if len(user['last_name']) < 3:
            flash("Apellido debe de tener al menos 3 caracteres", "register")

        if not EMAIL_REGEX.match(user['email']):
            flash('E-mail inválido')
            es_valido = False
        if len (user['password']) < 6:
            flash('contraseça debe tener al menos 6 caracteres', "register")
            es_valido = False
        if user['password'] != user['confirm']:
            flash('Contraseñas no coinciden')

        #Consulta si ya existe ese correo
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL('registro').query_db(query, user)
        if len(results) >= 1:
            flash('Email registrado previamente')
            es_valido = False
        
        return es_valido

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('registro').query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('registro').query_db(query, data)

        if len(result) < 1:
            return False
        else:
            usr = result[0]
            user =cls(usr)
            return user