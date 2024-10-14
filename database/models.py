# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 14, 2024 17:29:55
# Database: sqlite:////tmp/tmp.I5XoOLjPDl/Menu_Service_1/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class MenuItemCategory(SAFRSBaseX, Base):
    """
    description: Represents a category for menu items (e.g., appetizer, main course, etc.).
    """
    __tablename__ = 'menu_item_categories'
    _s_collection_name = 'MenuItemCategory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    MenuItemList : Mapped[List["MenuItem"]] = relationship(back_populates="category")



class Restaurant(SAFRSBaseX, Base):
    """
    description: Represents a restaurant with an ID, name, and location.
    """
    __tablename__ = 'restaurants'
    _s_collection_name = 'Restaurant'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    RestaurantMenuList : Mapped[List["RestaurantMenu"]] = relationship(back_populates="restaurant")



class MenuItem(SAFRSBaseX, Base):
    """
    description: Represents a menu item with details such as name, price, description, and category.
    """
    __tablename__ = 'menu_items'
    _s_collection_name = 'MenuItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    category_id = Column(ForeignKey('menu_item_categories.id'), nullable=False)
    photo = Column(String)

    # parent relationships (access parent)
    category : Mapped["MenuItemCategory"] = relationship(back_populates=("MenuItemList"))

    # child relationships (access children)
    MenuLogList : Mapped[List["MenuLog"]] = relationship(back_populates="menu_item")
    RestaurantMenuList : Mapped[List["RestaurantMenu"]] = relationship(back_populates="menu_item")



class MenuLog(SAFRSBaseX, Base):
    """
    description: Logs changes to menu items, such as additions, updates, or deletions.
    """
    __tablename__ = 'menu_logs'
    _s_collection_name = 'MenuLog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    menu_item_id = Column(ForeignKey('menu_items.id'), nullable=False)
    change_description = Column(String, nullable=False)
    change_date = Column(DateTime)

    # parent relationships (access parent)
    menu_item : Mapped["MenuItem"] = relationship(back_populates=("MenuLogList"))

    # child relationships (access children)



class RestaurantMenu(SAFRSBaseX, Base):
    """
    description: Represents the restaurant's specific menu items.
    """
    __tablename__ = 'restaurant_menus'
    _s_collection_name = 'RestaurantMenu'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(ForeignKey('restaurants.id'), nullable=False)
    menu_item_id = Column(ForeignKey('menu_items.id'), nullable=False)

    # parent relationships (access parent)
    menu_item : Mapped["MenuItem"] = relationship(back_populates=("RestaurantMenuList"))
    restaurant : Mapped["Restaurant"] = relationship(back_populates=("RestaurantMenuList"))

    # child relationships (access children)
