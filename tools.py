import flet as ft
import asyncio

def mostrar_usuario(usuario):
    return ft.Row(
        controls=[
            ft.Container(
                border=ft.border.all(1, "white54"),
                bgcolor="transparent",
                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                content=ft.Row(controls=[
                    ft.Icon(ft.icons.PERSON_ROUNDED),
                    ft.Text(usuario)
                ])
            )
        ]
    )

# input custom 
class UserInputField(ft.Row):
    def __init__(self, icon_name, suffix=False, password=False, placeholder=""):
        super().__init__()
        self.icon_name = icon_name  # Ícono mostrado en cada input
        self.suffix = suffix  # Booleano para añadir el subfijo @nauta
        self.password = password  # Booleano para si el campo es de contraseña
        self.placeholder = placeholder  # Placeholder del input
        self.value = ""  # Valor actual del input
        self.alignment = ft.MainAxisAlignment.CENTER
        
        # Campo de texto (separado para fácil acceso y manipulación)
        self.text_field = ft.TextField(
            border_color="transparent",
            bgcolor="transparent",
            width=210,
            text_size=14,
            content_padding=ft.Padding(0, 10, 0, 10),
            cursor_color="white",
            suffix_text="@nauta.com.cu" if self.suffix else "",
            suffix_style=ft.TextStyle(color="blue"),
            password=self.password,
            can_reveal_password=self.password,
            hint_text=self.placeholder,
            hint_style=ft.TextStyle(color="white54"),
            on_focus=self.on_focus,
            on_blur=self.on_blur,
            on_change=self.on_change
        )
        
        # Contenedor principal del campo de entrada
        self.container = ft.Container(
            width=270,
            height=50,
            border_radius=8,
            border=ft.border.all(1, "white54"),
            bgcolor="transparent",
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Ícono en el campo de entrada
                    ft.Icon(
                        name=self.icon_name,
                        size=22,
                        color="white70",
                    ),
                    # Campo de texto
                    self.text_field,
                ],
            ),
        )
        self.controls = [self.container]

    def on_change(self, e):
        self.value = e.data
    
    def on_focus(self, e):
        """Cambia el estilo cuando se enfoca el campo."""
        self.container.border = ft.border.all(2, "white")
        self.container.bgcolor = ft.colors.GREY_900 # Fondo ligeramente visible
        icon = self.container.content.controls[0]
        icon.color = "blue"  # Ícono más brillante
        self.update()

    def on_blur(self, e):
        """Restablece el estilo cuando se pierde el enfoque."""
        self.container.border = ft.border.all(1, "white54")
        self.container.bgcolor = "transparent"
        icon = self.container.content.controls[0]
        icon.color = "white70"  # Ícono más tenue
        self.update()

    def set_value(self, value):
        """Permite establecer un valor al campo de texto."""
        self.text_field.value = value
        self.text_field.update()
    
# funcion auiliar para crear dialogos y pantallas de carga
# page es la instancia de la pagina, carga es para crear una pantalla de carga, por defecto 'default', pero puede tener 'carga' y 'agregar_cuenta'
# 
def new_dialog(page, carga='', title_dialog=None, content_dialog=None, add=False):
    if carga == 'default' or carga=='':
        dialog = ft.AlertDialog(
            title=ft.Text(title_dialog),
            content=ft.Text(content_dialog),
            modal=True,
            actions=[ft.TextButton('Entendido', on_click=lambda e: page.close_dialog())]
        )
    
    elif carga == 'carga':
        dialog = ft.AlertDialog(
            bgcolor=ft.colors.TRANSPARENT,
            modal=True,
            content=ft.Container(content=ft.Column(controls=[ft.Container(
                content=ft.ProgressRing(),
                width=100,
                height=100,
                alignment=ft.alignment.center,
            ), ft.Text('Conectando...', text_align='center')], alignment='center', horizontal_alignment='center'), padding=ft.padding.all(20), alignment=ft.alignment.center)
        )
    
    elif carga == 'agregar_cuenta':
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title_dialog),
            content=ft.Container(content=ft.Column(height=150, controls=[
                UserInputField(
                    suffix='@nauta.com.cu',
                    password=False,
                    placeholder='usuario' ,
                    icon_name=ft.icons.PERSON_ROUNDED
                ),
                UserInputField(
                    password=True,
                    placeholder='contraseña',
                    icon_name=ft.icons.LOCK_OPEN_ROUNDED
                ), ], alignment='center', horizontal_alignment='center'
            ))
        )

    page.dialog = dialog
    dialog.open = True
    page.update()

# clase para el temporizador
class Cronometro(ft.Text):
    def __init__(self):
        super().__init__()
        self.seconds = 0
        self.size = 24
        self.weight = "bold"
        self.color = ft.colors.RED_900

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_cronometro)

    def will_unmount(self):
        self.running = False

    async def update_cronometro(self):
        while self.running:
            hours, remainder = divmod(self.seconds, 3600)
            mins, secs = divmod(remainder, 60)
            self.value = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds += 1

        

# ui detiempo programado para cuando pueda implementarlo
'''def crear_contenedor_tiempo_programado(self):
        """Crea el contenedor de tiempo programado ."""
        return ft.Container(
            width=320,
            height=160,
            bgcolor=ft.colors.GREEN_100,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Programado", size=14, color=ft.colors.GREEN_800),
                    # ft.Text("00:00:00", size=24, color=ft.colors.GREEN_900, weight='bold'),
                    self.temporizador
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )'''
