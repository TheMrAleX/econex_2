import flet as ft

def main(page: ft.Page):
    page.title = "Lista de Usuarios"
    page.padding = 20
    page.scroll = "auto"

    # Ejemplo de diccionario con datos de usuarios
    users = [
        {"usuario": "JohnDoe", "email": "john.doe@example.com"},
        {"usuario": "JaneDoe", "email": "jane.doe@example.com"},
        {"usuario": "User123", "email": "user123@example.com"},
    ]

    # Contenedor principal
    main_container = ft.Column(
        controls=[],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )

    # Título
    main_container.controls.append(
        ft.Text(
            "Lista de Usuarios",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_800,
        )
    )

    # Agregar cada usuario como una fila
    for user in users:
        row = ft.Row(
            controls=[
                ft.Text(
                    user.get("usuario", "Desconocido"),
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                ),
                ft.Text(user.get("email", "Sin correo"), color=ft.colors.GREY),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )

        # Agregar un contenedor con diseño alrededor de cada fila
        user_card = ft.Container(
            content=row,
            padding=10,
            bgcolor=ft.colors.BLUE_GREY_50,
            border_radius=10,
            border=ft.border.all(1, ft.colors.BLUE_GREY_100),
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.BLUE_GREY_200),
        )

        main_container.controls.append(user_card)

    # Agregar todo al contenido de la página
    page.add(main_container)

# Ejecutar la app
ft.app(target=main)
