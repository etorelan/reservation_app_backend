import os
import random
import django
import json
# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netflix_clone_backend.settings")
django.setup()

from django.db import transaction
from django.contrib.auth.models import User
from base.models import *  # Replace 'your_app' with your actual Django app name


def populate_database():
    # # Load data from the countries-states-cities-database repository
    db_file = "./hotel_names.json"  # Replace with the actual path to the 'countries.json' file

    # Assuming you have Django models for Country and City, update the following code accordingly
    # with open(db_file, 'r', encoding='utf-8') as file:
    #     with transaction.atomic():
    #         countries_data = json.load(file)

    #         # Iterate over the countries data and create Country objects
    #         for entry in countries_data:
    #             if len(entry["cities"]) >= 9:
    #                 try:
    #                     country = Country.objects.get(name=entry["name"])
    #                     random_cities = random.sample(entry["cities"], k=9)
    #                     for city in random_cities:
    #                         try:
    #                             City.objects.create(name=city["name"], country=country)
    #                         except:
    #                             pass

    #                 except Country.DoesNotExist:
    #                     country = Country.objects.create(name=entry["name"])
    #                     random_cities = random.sample(entry["cities"], k=9)

    #                     for city in random_cities:
    #                         City.objects.create(name=city["name"], country=country)

    #                 print(f"Added cities for {entry['name']}")
    # d = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Neque vitae tempus quam pellentesque nec nam aliquam sem et. In fermentum et sollicitudin ac orci phasellus. Nisi lacus sed viverra tellus. Aliquam vestibulum morbi blandit cursus risus. Gravida arcu ac tortor dignissim convallis aenean et tortor at. Arcu non sodales neque sodales. Odio tempor orci dapibus ultrices in iaculis nunc. Placerat in egestas erat imperdiet sed euismod nisi porta lorem. Scelerisque eu ultrices vitae auctor eu augue ut. Odio aenean sed adipiscing diam donec adipiscing tristique. Netus et malesuada fames ac turpis. Euismod quis viverra nibh cras pulvinar mattis. Ante in nibh mauris cursus mattis. Nisl nisi scelerisque eu ultrices vitae auctor. At in tellus integer feugiat scelerisque varius. Sollicitudin tempor id eu nisl nunc mi. Mauris nunc congue nisi vitae suscipit tellus mauris a. Adipiscing elit pellentesque habitant morbi tristique senectus. Dictum varius duis at consectetur lorem donec massa sapien faucibus. Urna duis convallis convallis tellus id interdum velit laoreet. Amet cursus sit amet dictum sit. Viverra mauris in aliquam sem fringilla. Duis at tellus at urna condimentum mattis pellentesque. Mattis molestie a iaculis at erat pellentesque adipiscing commodo elit. Aliquam malesuada bibendum arcu vitae elementum. Eget velit aliquet sagittis id. Integer eget aliquet nibh praesent tristique magna sit amet. Et malesuada fames ac turpis egestas integer eget aliquet. Ut faucibus pulvinar elementum integer enim neque volutpat. Id faucibus nisl tincidunt eget. Porttitor leo a diam sollicitudin tempor id eu. Leo in vitae turpis massa sed elementum tempus. Sed sed risus pretium quam. Facilisis magna etiam tempor orci eu lobortis elementum. Elit scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus. Mi proin sed libero enim sed faucibus turpis in eu. Lacus sed turpis tincidunt id aliquet risus feugiat. Faucibus vitae aliquet nec ullamcorper sit. At volutpat diam ut venenatis tellus in metus vulputate eu. Quam pellentesque nec nam aliquam sem. Erat imperdiet sed euismod nisi. Commodo ullamcorper a lacus vestibulum sed arcu non. Tellus orci ac auctor augue mauris augue neque gravida. Ut placerat orci nulla pellentesque. Pulvinar etiam non quam lacus suspendisse faucibus interdum posuere lorem. Tincidunt vitae semper quis lectus. Tristique nulla aliquet enim tortor. Rhoncus urna neque viverra justo nec ultrices dui. Egestas pretium aenean pharetra magna ac placerat vestibulum. Tempor orci eu lobortis elementum. Felis donec et odio pellentesque diam volutpat commodo. Neque vitae tempus quam pellentesque nec nam aliquam sem. Tristique senectus et netus et malesuada fames ac turpis egestas. Sit amet aliquam id diam maecenas ultricies mi eget mauris. Augue lacus viverra vitae congue eu consequat ac. Augue ut lectus arcu bibendum at. Condimentum vitae sapien pellentesque habitant. Ut diam quam nulla porttitor massa id neque aliquam vestibulum. Nunc congue nisi vitae suscipit tellus mauris a. Eu consequat ac felis donec et odio pellentesque diam. Eget nunc lobortis mattis aliquam faucibus purus in. Nisi porta lorem mollis aliquam ut porttitor. Massa tincidunt nunc pulvinar sapien et ligula. Sem nulla pharetra diam sit amet nisl suscipit adipiscing. Proin sed libero enim sed faucibus turpis in eu. In hac habitasse platea dictumst. Sed velit dignissim sodales ut. Suscipit tellus mauris a diam."

    with open(db_file, 'r', encoding='utf-8') as file:
        words_data = json.load(file)

        with transaction.atomic():
            for _ in range(7):
                email = random.choice(words_data) + "@email.com"
                
                id = random.randint(387, 569)
                country = Country.objects.get(id=id)
                f_name = random.choice(words_data)
                l_name = random.choice(words_data)
                phone = "999 999 999"

                g = Guest(email=email, country=country, first_name=f_name, last_name=l_name, phone=phone)
                g.full_clean()
                g.save()


    print("Database population complete!")


if __name__ == "__main__":
    # populate_database()
    pass dont
