

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
 establece las reglas de cómo se comportará la aplicación en el sistema operativo.

page.theme_mode: Forzamos el modo claro para que los colores crema y negro no varíen si el usuario tiene su Windows en "Modo Oscuro".

page.window: En Flet 0.80.5, el manejo de la ventana se movió a este sub-objeto. Controlar el width y height evita que el diseño se "rompa" si el usuario estira la ventana de más.

page.padding: Un margen de 30px asegura que los controles no toquen los bordes físicos de la ventana, dando "aire" al diseño (espaciado visual).



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
 La RegEx (re.match):

Python
r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
Este jeroglífico verifica tres partes: (1) Nombre de usuario, (2) el símbolo @, (3) el dominio y el punto. Sin esto, alguien podría registrarse como "hola", lo cual no es un email.

validar_escribiendo: Este es un Evento Dinámico. Al asignarlo a on_change, Flet ejecuta esta función cada vez que el usuario presiona una tecla.

Lógica: Si el campo tiene al menos un carácter (if e.control.value), el borde vuelve a negro. Esto le dice al usuario: "Gracias, ya vi que estás corrigiendo el error".

<img width="590" height="741" alt="image" src="https://github.com/user-attachments/assets/d47ac7b2-cceb-4fd8-b306-de49d0db135f" />

<img width="582" height="720" alt="image" src="https://github.com/user-attachments/assets/f0c0e3ac-b23e-4247-863b-f205ad2c0c97" />

---

Estructura del Formulario (Controles)

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
<img width="580" height="827" alt="image" src="https://github.com/user-attachments/assets/237973bc-a0a5-403d-986c-688b30995ff1" />


 Combinamos `TextField` para texto libre, `Dropdown` para opciones cerradas (carrera/semestre) y `RadioGroup` para la selección única de género.
 ft.TextField: Es una entrada de texto libre. Usamos label para que el nombre del campo flote arriba cuando el usuario escribe.

ft.Dropdown: Es un control de Selección Cerrada. Esto es fundamental en ingeniería para normalizar datos; evita que alguien escriba "Sistemas", otro "ISC" y otro "Ing. Sistemas". Todos deben elegir la misma opción de la lista.

ft.RadioGroup: A diferencia del Dropdown, el RadioGroup es para opciones de Baja Densidad (pocas opciones). Al ponerlas en un ft.Row, logramos que el formulario no sea tan largo verticalmente.

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
Es un proceso secuencial de 3 pasos:

Iteración de Verificación:
Usamos un ciclo for campo in campos: para no escribir 5 veces el mismo if. Si un campo está vacío, incrementamos la variable errores. Es un "filtro de seguridad".

Manejo del page.overlay:
En Flet 0.80.5, el AlertDialog no vive "dentro" de la página, sino en una capa superior llamada Overlay. Si no lo agregas a page.overlay, el modal nunca aparecerá aunque le des open = True.

Reseteo de Estado:
Una vez que el registro es exitoso, es una buena práctica de UX (Experiencia de Usuario) limpiar todo. Usamos campo.value = "" para vaciar el formulario y que quede listo para el siguiente estudiante.
<img width="547" height="785" alt="image" src="https://github.com/user-attachments/assets/d5ef61b0-2e8b-4e4a-b432-309b256a29a0" />


---
La arquitectura del software sigue un modelo de Programación Orientada a Eventos, donde la interfaz permanece a la escucha de las acciones del usuario, validando la integridad de los datos en dos niveles: preventivo (mientras escribe) y restrictivo (al intentar enviar).

