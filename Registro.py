import flet as ft
import re

def main(page: ft.Page):
    # ---------------- CONFIGURACIÓN ----------------
    page.title = "Registro de Estudiantes - TAP"
    page.bgcolor = "#FDFBE3"
    page.padding = 30
    page.window.width = 500
    page.window.height = 800

    # ---------------- FUNCIONES ----------------
    def es_email_valido(email):
        return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

    def cerrar_modal(e):
        dlg_modal.open = False
        page.update()

    def validar_escribiendo(e):
        # Si el usuario empieza a escribir/seleccionar, limpiamos el error visual
        if e.control.value:
            e.control.border_color = "black"
            e.control.border_width = 1
            if hasattr(e.control, "helper_text"):
                e.control.helper_text = ""
        page.update()

    # ---------------- CONTROLES ----------------
    txt_nombre = ft.TextField(label="Nombre Completo", border_color="black", bgcolor="white")
    txt_nombre.on_change = validar_escribiendo

    txt_control = ft.TextField(label="Número de Control", border_color="black", bgcolor="white")
    txt_control.on_change = validar_escribiendo

    txt_email = ft.TextField(label="Correo Electrónico", border_color="black", bgcolor="white")
    txt_email.on_change = validar_escribiendo

    dd_carrera = ft.Dropdown(
        label="Carrera",
        bgcolor="white",
        options=[
            ft.dropdown.Option("Ingeniería en Sistemas"),
            ft.dropdown.Option("Ingeniería Civil"),
            ft.dropdown.Option("Ingeniería Industrial"),
        ]
    )
    dd_carrera.on_change = validar_escribiendo

    dd_semestre = ft.Dropdown(
        label="Semestre",
        bgcolor="white",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 13)]
    )
    dd_semestre.on_change = validar_escribiendo

    # RadioGroup mejorado
    genero_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Masculino", label="Masculino"),
            ft.Radio(value="Femenino", label="Femenino"),
            ft.Radio(value="Otro", label="Otro"),
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    txt_error_msg = ft.Text("", color="red", weight="bold")

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmación de Registro"),
        actions=[
            ft.TextButton(content=ft.Text("Cerrar"), on_click=cerrar_modal),
        ],
    )

    def enviar_click(e):
        campos = [txt_nombre, txt_control, txt_email, dd_carrera, dd_semestre]
        errores = 0
        
        # 1. Validar campos vacíos
        for campo in campos:
            if not campo.value:
                campo.border_color = "red"
                campo.border_width = 2
                errores += 1
            else:
                campo.border_color = "green"
                campo.border_width = 1

        # 2. Validar Email (solo si no está vacío)
        if txt_email.value and not es_email_valido(txt_email.value):
            txt_email.border_color = "red"
            txt_email.helper_text = "Formato de correo inválido"
            errores += 1

        # 3. Validar Género
        if not genero_group.value:
            errores += 1
            txt_error_msg.value = "Error: Debes seleccionar un género y llenar todos los campos."
        else:
            if errores == 0:
                txt_error_msg.value = "" # Limpiar mensaje si todo está ok

        # Lógica de Resultado
        if errores == 0:
            # ÉXITO: Mostrar Modal
            dlg_modal.content = ft.Text(
                f"Estudiante: {txt_nombre.value}\n"
                f"No. Control: {txt_control.value}\n"
                f"Email: {txt_email.value}\n"
                f"Carrera: {dd_carrera.value}\n"
                f"Semestre: {dd_semestre.value}º\n"
                f"Género: {genero_group.value}"
            )
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            
            # Limpiar Formulario
            for campo in campos:
                campo.value = ""
                campo.border_color = "black"
            genero_group.value = None
            txt_error_msg.value = ""
        else:
            # FALLO: Feedback visual
            if not txt_error_msg.value:
                txt_error_msg.value = "Revisa los campos marcados en rojo."
        
        page.update()

    btn_enviar = ft.FilledButton(
        content=ft.Text("REGISTRAR ESTUDIANTE", color="white", weight="bold"),
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLACK),
        on_click=enviar_click,
        height=50,
        width=400
    )

    # ---------------- UI ----------------
    page.add(
        ft.Column([
            ft.Text("REGISTRO DE ASPIRANTES", size=25, weight="bold", color="black"),
            txt_nombre,
            txt_control,
            txt_email,
            ft.Row([dd_carrera, dd_semestre], spacing=10),
            ft.Text("Género:", weight="bold"),
            genero_group,
            txt_error_msg, # Mensaje de error dinámico
            ft.Divider(height=10, color="transparent"),
            btn_enviar
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )

if __name__ == "__main__":
    ft.run(main)