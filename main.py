import flet as ft
from tools import UserInputField, new_dialog, Cronometro, mostrar_usuario
from econnect import Nauta
from manager import iniciar_sesion_json, cererar_sesion_json, cargar_valor_online, save_online_or_offline, ultimo_usuario_en_iniciar_sesion, load_users
# clase nauta para la persistencia

nauta = Nauta()

# clase principal de la app
class EconexApp:
    def __init__(self, page: ft.Page):
        self.page = page # instancia de page de flet
        self.control_login = 'offline' # variable de control
        self.page_appbar = ft.AppBar(title=ft.Text('Econex'), bgcolor=ft.colors.SURFACE_VARIANT) # appbar de la app
        self.page_bottom_appbar = self.create_navigation_bar() # navigation bar de la app
        self.user_input = UserInputField(ft.icons.PERSON_ROUNDED, True, placeholder='usuario') # input de usuario
        self.password_input = UserInputField(ft.icons.LOCK_OPEN_ROUNDED, password=True, placeholder='contraseña') # input de password

        self.datos_nauta = ('assets/datos.econex')
        
        self.init_page() # funcion que inicia las configuraciones iniciales de la app

        # verifica si la sesión no se cerró para comenzar a cargarla
        online = cargar_valor_online()
        if online['online'] == 'no':
            print('no')
        elif online['online'] == 'si':
            self.cargar_ui_de_sesion(nauta.reanude_login(self.datos_nauta))

        user = ultimo_usuario_en_iniciar_sesion()
        if user != False:
            user['username'] = user['username'].split('@nauta.com.cu')[0]
            self.user_input.set_value(user['username'])
            self.password_input.set_value(user['password'])


    # carga ui si detecta que la sesión no se cerró
    def cargar_ui_de_sesion(self, tiempo):
        self.page.views.clear() # limpiamos las vistas
        loged_view = self.construir_vista_principal(tiempo) # cargamos la vista pasando el tiempo disponible
        self.page.views.append(loged_view) # agregamos la vista a la lista de vistas
        self.page.close_dialog() # cerramos el dialogo de carga
        self.page.update()

    def init_page(self):
        # configuraciones iniciales de la página
        self.page.title = 'Econex'
        self.page.horizontal_alignment = 'center'
        self.page.vertical_alignment = 'center'
        self.page.bgcolor = '#333'
        self.main_page_change(0)

    def create_navigation_bar(self):
        # crea una barra de navegación
        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.WIFI_ROUNDED, label='Inicio'),
                ft.NavigationBarDestination(icon=ft.icons.ACCOUNT_BOX_OUTLINED, label='Cuentas')
            ], on_change=lambda e: self.main_page_change(e.control.selected_index)
        )
    
    def index_zero(self):
        # página principal
        return [
            self.page_appbar,

            ft.Divider(color=ft.colors.TRANSPARENT),
            ft.Image(src='etecsa.png'),  # Imagen de ETECSA
            ft.Text('Iniciar sesión', size=28),

            ft.Divider(color=ft.colors.TRANSPARENT),
            self.user_input,

            ft.Divider(color=ft.colors.TRANSPARENT),
            self.password_input,

            ft.Divider(color=ft.colors.TRANSPARENT),
            ft.OutlinedButton(
                text='Conectarme',
                on_click=self.iniciar_sesion,
                height=42,
                icon=ft.icons.LOGIN_ROUNDED
            ), 
            self.page_bottom_appbar,
        ]
    
    def iniciar_sesion(self, e):
        # inicio de sesion asincrono
        self.control_login = 'loading'
        self.show_loading_dialog()
        import threading
        threads = []
        t = threading.Thread(target=self.login)
        threads.append(t)
        t.start()

    def login(self):
        # funcion que inicia sesion

        
        # bloque de código para iniciar sesion sin verificar
        '''self.page.views.clear() # limpiamos las vistas
        loged_view = self.construir_vista_principal('00:00:00') # cargamos la vista pasando el tiempo disponible
        self.page.views.append(loged_view) # agregamos la vista a la lista de vistas
        self.page.close_dialog() # cerramos el dialogo de carga
        self.page.update() # actualizamos la app
        return True'''



        # logica que hara el iniciode sesión
        try:
            if nauta.test_net(): # intentamos verificar si al conexión está en buen estado
                # tomamos el usuario y contraseña de los inputs correspondientes
                usuario = self.user_input.value
                password = self.password_input.value

                # si el usuario no termina en @nauta.com.cu se lo agregamos
                if usuario.endswith('@nauta.com.cu'):
                    pass

                else:
                    usuario = usuario+'@nauta.com.cu'

                # inicio de sesion con usuario y contraseña se guardará True o False dependiendo
                inicio = nauta.login_net(usuario, password)
                if inicio==True: # si el inicio es True ya iniciamos sesión y cambiamos de vista
                    nauta.save_data(self.datos_nauta)
                    save_online_or_offline('si')
                    iniciar_sesion_json(usuario, password) 
                    tiempo_disponible = nauta.get_time() # guardamos el tiempo disponible para mostrarlo
                    self.page.views.clear() # limpiamos las vistas
                    loged_view = self.construir_vista_principal(tiempo_disponible) # cargamos la vista pasando el tiempo disponible
                    self.page.views.append(loged_view) # agregamos la vista a la lista de vistas
                    self.page.close_dialog() # cerramos el dialogo de carga
                    self.page.update() # actualizamos la app
                
                # si el inicio de sesion no es efectivo mostramos el error
                else:
                    self.page.close_dialog() # cerramos dialogo de carga y mostramos error
                    new_dialog(self.page, title_dialog='Error', content_dialog=inicio, carga='default')
                    self.control_login = 'offline'
                    
            # si la verificación de la red no es efectiva mostramos el error
            else:
                new_dialog(self.page, title_dialog='Error', content_dialog='Error al conectar con el Portal Nauta revise su conexón.', carga='default')

        # si hay alguna excepcion la pasamos a depuración
        except Exception as e:
            print(e)
        
    def show_loading_dialog(self):
        # muestra un dialogo de carga
        new_dialog(self.page, carga='carga')

    def dialogo_error(self, title, content):
        # muestra los dialogos de error, toma titulo y contenido
        new_dialog(self.page, title_dialog=title, content_dialog=content)

    def main_page_change(self, index):
        # muestra contenido segun el indice de navegacion
        content = []
        if index == 0 or 1:
            content = self.index_zero()
        elif index == 'APARTADO DE CUENTAS HAY QUE ARREGLARLO':
            content = []
            users = load_users()
            if len(users) > 0:
                for user in users:
                    usuario = user['username']
                    content.append(mostrar_usuario(usuario))
            else:
                content = [self.page_appbar, self.create_navigation_bar()]

            print(content)

        home = ft.View(
            '/',
            content,
            horizontal_alignment='center'
        )

        self.page.views.clear()
        self.page.views.append(home)
        self.page.update()

    #----------------------------------------------------
    # ALL SOBRE LA VISTA DE LOGEADO
    #----------------------------------------------------


    def cerrar_sesion(self, e):
        # cierre de sesión asíncrono
        self.show_loading_dialog()
        import threading
        threads = []
        t = threading.Thread(target=self.close)
        threads.append(t)
        t.start()

    def gui_close(self, e=None):
        save_online_or_offline('no')
        self.page.views.clear() # limpiamos las vistas
        self.main_page_change(0)# cargamos la vista pasando el tiempo disponible
        

    def close(self):

        try:
            r = nauta.logout()
            print(r)
            if r == True:
                self.gui_close()
        except:
            r = nauta.logout_back(self.datos_nauta)
            if r == True:
                self.gui_close()
            else:
                self.page.close_dialog()
                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text('Imposible cerrar sesión'),
                    content=ft.Text('No hemos podido cerrar la conexión de ninguna manera, hazlo manualmente apagando el Nauta y toca la opción de olvidar para que la app no se atasque.'),
                    actions=[
                        ft.TextButton('cancelar', on_click=lambda e: self.page.close(dialog)),
                        ft.TextButton('olvidar', on_click=self.gui_close)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                self.page.open(dialog)
                self.page.update()

    # la vista de logeado se divide en contenedores, cada función crea su correspondiente
    def crear_contenedor_tiempo_disponible(self, tiempo_disponible):
        """Crea el contenedor de tiempo disponible con el tiempo proporcionado."""
        return ft.Container(
            width=160,
            height=160,
            bgcolor=ft.colors.BLUE_GREY_100,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Disponible", size=14, color=ft.colors.BLUE_GREY_800),
                    ft.Text(
                        tiempo_disponible,
                        size=24,
                        weight="bold",
                        color=ft.colors.BLUE_GREY_900,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def crear_contenedor_tiempo_consumido(self):
        """Crea el contenedor de tiempo consumido con un cronómetro."""
        return ft.Container(
            width=160,
            height=160,
            bgcolor=ft.colors.RED_100,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Consumido", size=14, color=ft.colors.RED_800),
                    Cronometro(),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def construir_vista_principal(self, tiempo_disponible_var):
        """Construye la vista principal."""
        tiempo_disponible = self.crear_contenedor_tiempo_disponible(tiempo_disponible_var)
        tiempo_consumido = self.crear_contenedor_tiempo_consumido()

        return ft.View(
            "/loged",
            controls=[
                ft.AppBar(
                    title=ft.Text("Econex", size=20),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        tiempo_disponible,
                        tiempo_consumido,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(color=ft.colors.TRANSPARENT),
                ft.OutlinedButton('Desconectarme', height=42, icon=ft.icons.LOGOUT_OUTLINED, on_click=self.cerrar_sesion),
                ft.Divider()
                # self.crear_contenedor_tiempo_programado()
            ],horizontal_alignment='center'
        )

def main(page: ft.Page):
    app = EconexApp(page)

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')