# Prototipo navegable · aspecto Atlas

Recorrido visual de cómo se vería XMedical con el lenguaje del Atlas. No consulta el backend y no guarda datos. Los nombres clínicos de ejemplo son sintéticos.

## Abrir

Desde la carpeta `deck`:

```powershell
python -m http.server 8080 --directory deck
```

Luego abre `http://localhost:8080/prototipo/`.

También puedes abrir `deck/prototipo/index.html` con doble clic. Si el navegador bloquea las escenas o las fuentes, usa el servidor de arriba.

## Recorrer

En la portada se elige uno de los siete perfiles. Dentro, el menú lateral y las flechas cambian de pantalla. `G` abre el mapa de perfiles. `Esc` vuelve a la portada. `Home` también.

Atajo directo: `?perfil=medico` o el hash `#medico/consulta`.

Cada perfil clínico abre en su inicio con el hilo del día: cinco estaciones y la ocupación con iniciales. Recepción abre Agendar y Recibir; enfermería, Medir; medicina, Atender; especialidad, Derivar. El paciente solo ve su lugar. Administrador y superadministrador no llevan esa franja. En pantallas de menos de 860 px la escena grande se oculta y queda una estación abierta.

## Avatares

Suelta los archivos en `deck/prototipo/avatars/`.

Nombres: `superadmin`, `admin`, `recepcionista`, `enfermera`, `medico`, `especialista`, `paciente`, `fallback`.

SVG o PNG, fondo transparente, unos 256 px. Si existen los dos, se usa el SVG. Si no hay archivo, se muestran las iniciales.
