

Configuración del Entorno y UI Base

Definimos el lienzo donde trabajaremos y los parámetros visuales para que la app se vea profesional.

```python
def main(page: ft.Page):
    page.title = "Registro de Estudiantes - TAP"
    page.bgcolor = "#FDFBE3" # Color crema de fondo
    page.padding = 30
    
    # Configuración de ventana para versiones 0.80.5+
    page.window.width = 500
    page.window.height = 800

```

 Se configura el título, el color de fondo y el tamaño de la ventana. Usamos la nueva jerarquía `page.window` para evitar errores de compatibilidad.

---

Motores de Validación y Limpieza

Aquí definimos la "inteligencia" detrás del formulario: cómo saber si un dato es correcto y cómo limpiar los errores visuales cuando el usuario interactúa.

```python
    def es_email_valido(email):
        # Validación mediante Expresión Regular
        return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

    def validar_escribiendo(e):
        if e.control.value:
            e.control.border_color = "black"
            e.control.border_width = 1
            if hasattr(e.control, "helper_text"):
                e.control.helper_text = ""
        page.update()

```

 `es_email_valido` asegura que el correo tenga un formato real. `validar_escribiendo` es un evento dinámico que quita el color rojo del borde en cuanto el usuario empieza a escribir en un campo que estaba mal.

---

## 📋Estructura del Formulario (Controles)

Definimos los componentes visuales. Es crítico notar que en esta versión de Flet, los eventos se asignan por separado para evitar errores de tipo.

```python
    # Campos de Texto
    txt_nombre = ft.TextField(label="Nombre Completo", border_color="black")
    txt_nombre.on_change = validar_escribiendo

    # Menús desplegables (Dropdowns)
    dd_carrera = ft.Dropdown(
        label="Carrera",
        options=[ft.dropdown.Option("Ingeniería en Sistemas"), ...]
    )
    dd_carrera.on_change = validar_escribiendo

    # Selección de Género (RadioGroup)
    genero_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Masculino", label="Masculino"),
            ft.Radio(value="Femenino", label="Femenino"),
        ])
    )

```

 Combinamos `TextField` para texto libre, `Dropdown` para opciones cerradas (carrera/semestre) y `RadioGroup` para la selección única de género.

---

Lógica de Envío y Feedback Final

Es donde se decide si los datos se aceptan o se rechazan, y se muestra el resumen final en una ventana modal.

```python
    def enviar_click(e):
        # Auditoría de campos
        campos = [txt_nombre, txt_control, txt_email, dd_carrera, dd_semestre]
        errores = 0
        
        for campo in campos:
            if not campo.value:
                campo.border_color = "red"
                errores += 1
        
        if errores == 0 and genero_group.value:
            # Si todo está OK, mostramos el AlertDialog
            dlg_modal.content = ft.Text(f"Estudiante: {txt_nombre.value}...")
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            # ... (limpieza de formulario)

```

El botón activa una verificación por bucle. Si hay errores, se marcan en rojo. Si todo es exitoso, se construye el contenido del `AlertDialog` (Ventana Modal) y se despliega usando `page.overlay`.

---

