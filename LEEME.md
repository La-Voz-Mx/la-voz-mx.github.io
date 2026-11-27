# Cómo subir y bajar notas · La Voz del Bajío

El sitio se edita con **Pages CMS**, un panel gratuito que funciona en el navegador (también en celular).
Se entra con la cuenta de GitHub, se llena un formulario y se guarda. Uno o dos minutos después el cambio ya está en el sitio.
No hay que tocar código.

---

## Día a día

### Subir una nota
1. Entra a **app.pagescms.org** y abre el sitio de La Voz del Bajío.
2. En el menú de la izquierda elige **📰 Noticias**.
3. Pulsa el botón para **agregar una entrada** (Add entry).
4. Llena el formulario: titular, fecha, categoría, resumen, foto y texto.
   - En el texto, deja **una línea en blanco entre párrafos**.
   - Para un subtítulo, empieza la línea con `## `.
   - Si es la nota más importante del día, activa **Nota principal de la portada** (y desactívala en la anterior).
   - Si es una nota real, desactiva **Es contenido de muestra**.
5. Pulsa **Guardar** (Save). Listo.

### Bajar una nota
- **Para quitarla sin perderla:** ábrela, activa **Ocultar del sitio** y guarda. Para volver a mostrarla, desactívalo.
- **Para borrarla para siempre:** en la lista de Noticias usa el botón de borrar (Delete) de esa nota.

### Subir una columna (La Opinión)
1. Si la persona es nueva, primero agrégala en **👤 La Opinión · Columnistas** (nombre, cargo, retrato y orden en la fila).
2. En **✍️ La Opinión · Columnas** agrega una entrada y elige a la persona en **Columnista**.
3. Llena el título, la frase destacada y el texto. En **Fragmento a subrayar** copia unas palabras exactas del texto: se subrayan en verde.
4. Guarda. La columna aparece en «Todos» y en el filtro de esa persona.

Para bajar una columna o a un columnista, se usa igual **Ocultar del sitio** o el botón de borrar.

### Subir una sátira (La Fe de Erratas)
1. En **✏️ La Fe de Erratas** agrega una entrada y elige el **Tipo de pieza**.
2. Llena solo los campos de ese tipo (cada campo dice para qué tipo sirve):
   - **Errata:** Donde dice / Debe decir / palabras a resaltar. Activa **Errata del día** en una sola.
   - **Meme:** foto + texto de la banda.
   - **Titular imposible:** título + foto.
   - **Erratas de la semana:** agrega cada errata en la lista.
3. Guarda. Todas las piezas llevan la etiqueta «Sátira» automáticamente.

### Fotos
Se suben directo desde el campo **Foto** o **Retrato**. Se guardan en la carpeta `img/`.
Usa fotos horizontales de al menos 1400 px de ancho y que pesen menos de 1 MB.

### Compartir en redes
Cada publicación tiene su propio enlace, con el botón **Copiar enlace** en la página:
- Nota: `…/#nota-titular-de-la-nota`
- Columna: `…/#columna-titulo-de-la-columna`
- Columnas de una persona: `…/#opinion-nombre-apellido`
- Sátira: `…/#satira-titulo`

### Ajustes
En **⚙️ Ajustes del sitio** se cambian los enlaces de Facebook e Instagram y el aviso de «versión de prueba».
Cuando ya no quede contenido de muestra, borra el aviso.

---

## Configuración (una sola vez)

1. **Subir esta carpeta a GitHub**, en la organización La-Voz-Mx, en un repositorio llamado `la-voz-mx.github.io`.
2. En ese repositorio: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
   Desde entonces, cada cambio guardado publica el sitio en `https://la-voz-mx.github.io`.
3. Entra a **app.pagescms.org**, inicia sesión con GitHub e **instala la app de Pages CMS** en la organización La-Voz-Mx, dándole acceso a ese repositorio.
4. Para que otra persona del equipo pueda editar, dale acceso al repositorio en GitHub. Después podrá entrar al panel con su propia cuenta.

---

## Para quien mantiene el sitio

| Archivo | Qué es |
|---|---|
| `contenido/` | Una ficha `.json` por nota, columna, columnista y sátira. Es lo que edita el panel. |
| `.pages.yml` | Define los formularios del panel. |
| `herramientas/construir.py` | Junta las fichas en `contenido.js`. GitHub lo ejecuta en cada cambio. |
| `.github/workflows/publicar.yml` | Publica el sitio en GitHub Pages. |
| `contenido.js` | Se genera automáticamente. No lo edites a mano. |
| `index.html` | Diseño y funcionamiento del sitio. |
| `img/`, `logos/` | Fotografías y logotipos originales. |

Para probar en tu computadora: `python3 herramientas/construir.py` y abre `index.html`.
Si una ficha tiene un error, el sitio la salta y el registro de GitHub Actions dice cuál fue.
