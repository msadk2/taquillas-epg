# EPG Taquillas

Genera automáticamente un XMLTV con solo estas 14 taquillas:

- Taquilla Acción
- Taquilla Animación
- Taquilla Aventura
- Taquilla Ciencia Ficción
- Taquilla Cine España
- Taquilla Comedia
- Taquilla Documental
- Taquilla Drama
- Taquilla Fantasía
- Taquilla Histórica
- Taquilla Romance
- Taquilla Suspense
- Taquilla Terror
- Taquilla Western

La fuente es el `xmltv.php` de XUI. El workflow de GitHub Actions se ejecuta cada hora y actualiza:

`public/epg.xml`

## Secrets necesarios

En GitHub:

`Settings > Secrets and variables > Actions > New repository secret`

Crear:

- `XUI_BASE_URL` → `https://flexgo.xyz:443`
- `XUI_USERNAME` → tu usuario
- `XUI_PASSWORD` → tu contraseña

No escribas usuario ni contraseña directamente en los archivos del repositorio.

## Primera ejecución

Ve a:

`Actions > Actualizar EPG Taquillas > Run workflow`

Al terminar, debe aparecer `public/epg.xml`.

## URL del EPG

Si el repositorio es público, la URL será:

`https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/public/epg.xml`

Sustituye `TU_USUARIO` y `TU_REPOSITORIO`.

## Frecuencia

Actualmente se ejecuta una vez por hora:

`7 * * * *`

Puedes cambiar el cron del archivo:

`.github/workflows/update-epg.yml`
