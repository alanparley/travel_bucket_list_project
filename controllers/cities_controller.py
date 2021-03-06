from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.city import City
import repositories.country_repository as country_repository
import repositories.city_repository as city_repository

cities_blueprint = Blueprint("cities", __name__)

@cities_blueprint.route("/cities")
def cities():
    cities = city_repository.select_all()
    return render_template("cities/index.html", all_cities = cities)

@cities_blueprint.route("/cities/new", methods=['GET'])
def new_city():
    cities = city_repository.select_all()
    countries = country_repository.select_all()
    return render_template("cities/new.html", all_cities = cities, all_countries = countries)


@cities_blueprint.route('/cities', methods=['POST'])
def create_city():
    city_name = request.form['city_name']
    # visited = request.form['visited']
    country_id = request.form['country_id']
    country = country_repository.select(country_id)
    city = City(city_name, country)
    city_repository.save(city)
    return redirect('/countries')

@cities_blueprint.route("/cities/<id>/newtocountry", methods=['GET'])
def new_city_to_country(id):
    country = country_repository.select(id)
    return render_template('cities/newtocountry.html', country = country)

@cities_blueprint.route('/cities/new_to_country', methods=['POST'])
def add_city_to_country():
    city_name = request.form['city_name']
    country_id = request.form['country']

    country = country_repository.select(country_id)

    city = City(city_name, country)

    city_repository.save(city)
    return redirect('/countries')


@cities_blueprint.route("/countries/<id>", methods=['GET'])
def show_city(id):
    city = city_repository.select(id)
    return render_template('countries/index.html', city = city)


@cities_blueprint.route("/cities/<id>/edit", methods=['GET'])
def edit_city(id):
    city = city_repository.select(id)
    countries = country_repository.select_all()
    return render_template('cities/edit.html', city = city, all_countries = countries)

@cities_blueprint.route("/cities/<id>", methods=['POST'])
def update_city(id):
    city = city_repository.select(id)
    country = country_repository.select_all()
    visited = request.form['visited']
    city = City(city.city_name, country, visited, id)
    city_repository.update(city)
    return redirect('/countries')

@cities_blueprint.route("/cities/<id>/delete", methods=['POST'])
def delete_city(id):
    city_repository.delete(id)
    return redirect('/countries')

