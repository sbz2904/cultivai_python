#from config.firebase_config import db
from bson import ObjectId

from config.mongo_config import db

def create_user(data):
    try:
        #user_ref = db.collection('usuarios').add(data)
        user_ref = db.usuarios.insert_one(data)
        #return {'id': user_ref[1].id}
        return {'id': str(user_ref.inserted_id)}
    except Exception as e:
        return {'error': str(e)}

def get_all_users():
    try:
        users = []
        for doc in db.usuarios.find():
            doc['_id'] = str(doc['_id'])  # Convertir ObjectId a string
            users.append(doc)
        return users  # Ahora todos los _id son cadenas
    except Exception as e:
        return {'error': str(e)}
    

def get_user_by_id(user_id):
    try:
        user = db.usuarios.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])  # Convertir ObjectId a string
            user['sembrios'] = user.get('sembrios', [])  # Asegurar consistencia en nombre de clave
            return user
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}

def update_user_sembrios(user_id, sembrios_ids):
    try:
        result = db.usuarios.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'sembrios': sembrios_ids}}  # Cambiado a "sembrios" sin tilde
        )
        if result.matched_count > 0:
            return {'message': 'Sembrios actualizados correctamente'}
        return {'error': 'Usuario no encontrado'}
    except Exception as e:
        return {'error': str(e)}
