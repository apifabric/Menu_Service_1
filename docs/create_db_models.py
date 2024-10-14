import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Define the base class for declarative class definitions
Base = declarative_base()

# Define our tables/models

class Restaurant(Base):
    """
    description: Represents a restaurant with an ID, name, and location.
    """
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)


class MenuItemCategory(Base):
    """
    description: Represents a category for menu items (e.g., appetizer, main course, etc.).
    """
    __tablename__ = 'menu_item_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False)


class MenuItem(Base):
    """
    description: Represents a menu item with details such as name, price, description, and category.
    """
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey('menu_item_categories.id'), nullable=False)
    photo = Column(String, nullable=True)  # URL or filepath to the menu item photo


class RestaurantMenu(Base):
    """
    description: Represents the restaurant's specific menu items.
    """
    __tablename__ = 'restaurant_menus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)


class MenuLog(Base):
    """
    description: Logs changes to menu items, such as additions, updates, or deletions.
    """
    __tablename__ = 'menu_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    change_description = Column(String, nullable=False)
    change_date = Column(DateTime, default=datetime.datetime.now)


# Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data insertion
# Insert categories
categories = [
    MenuItemCategory(category_name='Appetizer'),
    MenuItemCategory(category_name='Main Course'),
    MenuItemCategory(category_name='Dessert'),
    MenuItemCategory(category_name='Beverage'),
    MenuItemCategory(category_name='Vegan')
]
session.add_all(categories)
session.commit()

# Insert restaurants
restaurants = [
    Restaurant(name='The Gourmet Kitchen', location='123 Flavor Town'),
    Restaurant(name='Vegan Delights', location='456 Plant St'),
    Restaurant(name='Ocean Fresh', location='789 Sea Lane')
]
session.add_all(restaurants)
session.commit()

# Insert menu items
menu_items = [
    MenuItem(name='Bruschetta', price=6.99, description='Grilled bread topped with diced tomatoes and basil.', category_id=1, photo='bruschetta.jpg'),
    MenuItem(name='Margarita Pizza', price=10.99, description='Classic pizza with fresh tomatoes, mozzarella, and basil.', category_id=2, photo='margarita_pizza.jpg'),
    MenuItem(name='Chocolate Cake', price=4.99, description='Rich chocolate cake with fudge icing.', category_id=3, photo='chocolate_cake.jpg'),
    MenuItem(name='Fresh Lemonade', price=2.50, description='Refreshing lemonade made with real lemons.', category_id=4, photo='lemonade.jpg'),
    MenuItem(name='Quinoa Salad', price=8.99, description='Healthy quinoa salad with fresh vegetables.', category_id=5, photo='quinoa_salad.jpg')
]
session.add_all(menu_items)
session.commit()

# Insert relationships in RestaurantMenu
restaurant_menus = [
    RestaurantMenu(restaurant_id=1, menu_item_id=1),
    RestaurantMenu(restaurant_id=1, menu_item_id=3),
    RestaurantMenu(restaurant_id=2, menu_item_id=5),
    RestaurantMenu(restaurant_id=3, menu_item_id=2),
    RestaurantMenu(restaurant_id=3, menu_item_id=4)
]
session.add_all(restaurant_menus)
session.commit()

# Insert menu logs
menu_logs = [
    MenuLog(menu_item_id=1, change_description='Added Bruschetta to the menu.'),
    MenuLog(menu_item_id=2, change_description='Margarita Pizza price updated.'),
    MenuLog(menu_item_id=3, change_description='Chocolate Cake description updated.'),
    MenuLog(menu_item_id=4, change_description='Fresh Lemonade added to beverages.'),
    MenuLog(menu_item_id=5, change_description='Quinoa Salad marked as vegan.')
]
session.add_all(menu_logs)
session.commit()

# Close session
session.close()
