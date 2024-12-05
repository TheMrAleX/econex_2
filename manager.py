import json
import os

RUTA = 'assets/cuentas.json'

if os.path.exists(RUTA):
    pass
else:
    with open(RUTA, 'wb') as archivo:
        archivo.write(archivo, RUTA)

# CRUD
def load_users():
    try:
        with open(RUTA, 'r') as file:
            return json.load(file)
        
    except:
        return []


def save_users(users):
    with open(RUTA, 'w') as file:
        json.dump(users, file, indent=4)

def create_user(username, password):
    users = load_users()
    # verificar que el usuario exista
    for user in users:
        if user['username'] == username:
            return False

    user_id = len(users) + 1

    users.append({'id': user_id, 'username': username, 'password': password, 'last': 'no'})
    save_users(users)
    return True # usuario guardado con éxito

def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
        return None
    
def ultimo_en_iniciar(usuario):
    users = load_users()

    for user in users:
        if user['username'] == usuario:
            user['last'] = 'si'
        else:
            user['last'] = 'no'
    save_users(users)

def colocar_no_en_online_usuario(usuario):
    
    users = load_users()
    
    for user in users:
        user['online'] = 'no'
    save_users(users)

def colocar_si_en_online_usuario(usuario):
    users = load_users()
    for user in users:
        if user['username'] == usuario:
            user['online'] = 'si'
    save_users(users)


def detectar_online():
    users = load_users()
    for user in users:
        if user['online'] == 'si':
            return True
        else:
            return False
        
def detectar_usuario_guardado():
    users = load_users()
    for user in users:
        if user['last'] == 'si':
            return user
    
    return False

def ultimo_usuario_en_iniciar_sesion():
    users = load_users()

    for user in users:
        if user['last'] == 'si':
            return user
    
    return False
        
def iniciar_sesion_json(usuario, password):
    ultimo_en_iniciar(usuario)
    create_user(usuario, password)
    colocar_si_en_online_usuario(usuario)

def cererar_sesion_json(usuario):
    colocar_no_en_online_usuario(usuario)


# para revisar si esta online

RUTA_ONLINE = 'assets/online.json'

if os.path.exists(RUTA_ONLINE):
    pass
else:
    with open(RUTA_ONLINE, 'wb') as archivo:
        archivo.write(archivo)

def cargar_valor_online():
    try:
        with open(RUTA_ONLINE, 'r') as file:
            return json.load(file)
        
    except:
        return []
    
def save_online_or_offline(online='no'):
    data = {'online': online}
    with open(RUTA_ONLINE, 'w') as file:
        json.dump(data, file, indent=4)
