#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects

        objs_list = {}
        cls_name = cls if isinstance(cls, str) else cls.__name__
        for k, v, in FileStorage.__objects.items():
            if k.split('.')[0] == cls_name:
                objs_list[k] = v

        return objs_list

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.amenity import Amenity
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete obj from __objects if it’s inside - if obj
        is equal to None, the method should not do anything
        """
        if obj:
            obj_id = obj.to_dict()["id"]
            cls_name = obj.to_dict()["__class__"]
            obj_key = cls_name + "." + obj_id

            if obj_key in FileStorage.__objects:
                del FileStorage.__objects[obj_key]
                self.save()

    def close(self):
        """
        call reload() method for deserializing
        the JSON file to objects
        """
        self.reload()
