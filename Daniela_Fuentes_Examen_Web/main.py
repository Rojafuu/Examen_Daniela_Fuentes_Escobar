# Importación de módulos necesarios para el funcionamiento de Flask y otras funcionalidades
from flask import Flask, request, render_template, redirect, url_for, session, flash

# Creación de la instancia principal de la aplicación Flask
app = Flask(__name__)

# Configuración de la clave secreta necesaria para manejar sesiones de usuario
app.config['SECRET_KEY'] = 'MI_CLAVE_SECRETA'  # Necesario para las sesiones

# Definición de un diccionario de usuarios predefinidos para simular un sistema de autenticación
USUARIOS = {
    "juan": "admin",  # Usuario 'juan' con la contraseña 'admin'
    "pepe": "user"  # Usuario 'pepe' con la contraseña 'user'
}


# Ruta principal de la aplicación, se activa cuando se hace una solicitud GET o POST a la raíz ('/')
@app.route('/', methods=['GET', 'POST'])
def home():
    # Si el método es POST (es decir, el formulario ha sido enviado)
    if request.method == 'POST':
        # Obtener el valor del campo 'ejercicio' del formulario
        ejercicio = request.form.get('ejercicio')

        # Redirigir al ejercicio correspondiente según el valor de 'ejercicio'
        if ejercicio == '1':
            return redirect(url_for('Ejercicio_1'))  # Redirige a la ruta de Ejercicio 1
        elif ejercicio == '2':
            return redirect(url_for('Ejercicio_2'))  # Redirige a la ruta de Ejercicio 2

    # Si el método es GET, simplemente renderiza la página de inicio
    return render_template('home.html')


# Ruta para el ejercicio 1, se activa cuando se hace una solicitud GET o POST a '/Ejercicio_1'
@app.route('/Ejercicio_1', methods=['GET', 'POST'])
def Ejercicio_1():
    # Si el método es POST (se envió el formulario)
    if request.method == 'POST':
        # Obtener los datos enviados en el formulario
        nombre = request.form.get('nombre')
        edad = request.form.get('edad')
        cantidad_tarros = request.form.get('cantidad_tarros')

        # Validación: Si algún campo está vacío, mostrar un mensaje de error
        if not nombre or not edad or not cantidad_tarros:
            flash("Todos los campos son requeridos.", "error")
            return render_template('Ejercicio_1.html')

        try:
            # Intentar convertir la edad y la cantidad de tarros a enteros
            edad = int(edad)
            cantidad_tarros = int(cantidad_tarros)
        except ValueError:
            # Si ocurre un error en la conversión (por ejemplo, se ingresa un texto en lugar de números)
            flash("Edad y cantidad de tarros deben ser números válidos.", "error")
            return render_template('Ejercicio_1.html')

        # Definición del precio por tarro
        precio_tarro = 9000

        # Calcular el costo total sin descuento (multiplicando cantidad de tarros por el precio de cada tarro)
        total_sin_descuento = cantidad_tarros * precio_tarro

        # Aplicar un descuento basado en la edad del usuario
        if 18 <= edad <= 30:
            descuento = 0.15  # 15% de descuento para usuarios entre 18 y 30 años
        elif edad > 30:
            descuento = 0.25  # 25% de descuento para usuarios mayores de 30 años
        else:
            descuento = 0.0  # No hay descuento para menores de 18 años

        # Calcular el total con descuento aplicado
        total_con_descuento = total_sin_descuento * (1 - descuento)

        # Calcular cuánto se ahorra el usuario con el descuento
        descuento_en_dinero = total_sin_descuento - total_con_descuento

        # Renderizar la página de Ejercicio_1 con los resultados del cálculo
        return render_template('Ejercicio_1.html', nombre=nombre, edad=edad,
                               cantidad_tarros=cantidad_tarros, total_sin_descuento=total_sin_descuento,
                               total_con_descuento=total_con_descuento, descuento_en_dinero=descuento_en_dinero)

    # Si el método es GET, simplemente renderiza la página de Ejercicio 1
    return render_template('Ejercicio_1.html')


# Ruta para el ejercicio 2, se activa cuando se hace una solicitud GET o POST a '/Ejercicio_2'
@app.route('/Ejercicio_2', methods=['GET', 'POST'])
def Ejercicio_2():
    # Verificar si el usuario ya está autenticado (si existe un 'username' en la sesión)
    if 'username' in session:
        return redirect(url_for('Ejercicio_2'))  # Si ya está logueado, redirige al mismo ejercicio

    # Inicialización del mensaje de bienvenida como None
    mensaje_bienvenida = None

    # Si el método es POST (se envió el formulario de login)
    if request.method == 'POST':
        # Obtener las credenciales enviadas en el formulario (usuario y contraseña)
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

        # Verificar si el usuario y la contraseña son correctos
        if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
            # Si las credenciales son correctas, iniciar sesión almacenando el nombre de usuario en la sesión
            session['username'] = usuario

            # Generar un mensaje de bienvenida dependiendo del tipo de usuario (administrador o usuario normal)
            if usuario == 'juan':
                mensaje_bienvenida = f'Bienvenido administrador {usuario}'
            elif usuario == 'pepe':
                mensaje_bienvenida = f'Bienvenido usuario {usuario}'
        else:
            # Si las credenciales son incorrectas, mostrar un mensaje de error
            flash("Usuario o contraseña incorrectos.", "error")

    # Renderizar la página de Ejercicio_2 con el mensaje de bienvenida si es que se ha logueado correctamente
    return render_template('Ejercicio_2.html', mensaje_bienvenida=mensaje_bienvenida)


# Ruta para cerrar sesión, se activa cuando se hace una solicitud a '/logout'
@app.route('/logout')
def logout():
    # Eliminar el 'username' de la sesión, cerrando efectivamente la sesión del usuario
    session.pop('username', None)

    # Mostrar un mensaje de éxito informando que la sesión ha sido cerrada
    flash("Has cerrado sesión correctamente.", "success")

    # Redirigir al formulario de login (Ejercicio_2)
    return redirect(url_for('Ejercicio_2'))


# Ejecutar la aplicación Flask en modo de desarrollo (debug=True permite reiniciar automáticamente la aplicación cuando se hace un cambio)
if __name__ == '__main__':
    app.run(debug=True)
