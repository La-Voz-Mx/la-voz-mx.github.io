#!/usr/bin/env python3
"""
Construye contenido.js a partir de la carpeta contenido/.

Cada nota, columna, columnista y sátira es un archivo .json que el equipo
edita desde Pages CMS (app.pagescms.org). GitHub ejecuta este script en
cada cambio (ver .github/workflows/publicar.yml) y publica el sitio.

Para probarlo en tu computadora:  python3 herramientas/construir.py
"""
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENIDO = os.path.join(RAIZ, "contenido")
SALIDA = os.path.join(RAIZ, "contenido.js")
avisos = []


def slug_de(texto):
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t or "sin-titulo"


def leer(carpeta):
    """Devuelve [(slug, datos)] de cada .json de la carpeta."""
    ruta = os.path.join(CONTENIDO, carpeta)
    if not os.path.isdir(ruta):
        return []
    items = []
    for nombre in sorted(os.listdir(ruta)):
        if not nombre.endswith(".json"):
            continue
        try:
            with open(os.path.join(ruta, nombre), encoding="utf-8") as f:
                datos = json.load(f)
        except Exception as e:  # un archivo dañado no debe tumbar el sitio
            avisos.append(f"Se omitió {carpeta}/{nombre}: no es JSON válido ({e})")
            continue
        if not isinstance(datos, dict):
            continue
        if datos.get("ocultar"):
            continue
        items.append((slug_de(os.path.splitext(nombre)[0]), datos))
    return items


def fecha(v):
    v = str(v or "")
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", v)
    return m.group(0) if m else ""


def ruta_media(v):
    """Pages CMS guarda '/img/foto.jpg'; el sitio usa rutas relativas 'img/foto.jpg'."""
    v = str(v or "").strip()
    return v.lstrip("/") if v and not v.startswith(("http://", "https://")) else v


def cuerpo(texto):
    """Texto con párrafos separados por línea en blanco; '## ' marca un subtítulo."""
    if isinstance(texto, list):
        return texto
    bloques = []
    for parte in re.split(r"\n\s*\n", str(texto or "").replace("\r\n", "\n")):
        parte = parte.strip()
        if not parte:
            continue
        if parte.startswith("## "):
            bloques.append({"h": parte[3:].strip()})
        else:
            bloques.append(re.sub(r"\s*\n\s*", " ", parte))
    return bloques


def limpiar(d, claves):
    return {k: d[k] for k in claves if k in d and d[k] not in (None, "", [])}


def requerido(tipo, slug, d, campos):
    faltan = [c for c in campos if not d.get(c)]
    if faltan:
        avisos.append(f"Se omitió {tipo} '{slug}': falta {', '.join(faltan)}")
        return False
    return True


def main():
    config = {}
    p = os.path.join(CONTENIDO, "config.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            config = json.load(f)

    noticias = []
    for slug, d in leer("noticias"):
        if not requerido("la nota", slug, d, ["titulo", "fecha"]):
            continue
        n = limpiar(d, ["muestra", "principal", "categoria", "ciudad", "titulo", "resumen", "pie", "firma"])
        n.update(slug=slug, fecha=fecha(d.get("fecha")), foto=ruta_media(d.get("foto")), cuerpo=cuerpo(d.get("cuerpo")))
        noticias.append(n)

    columnistas = []
    for slug, d in leer("columnistas"):
        if not requerido("el columnista", slug, d, ["nombre"]):
            continue
        a = limpiar(d, ["muestra", "nombre", "cargo"])
        a.update(slug=slug, retrato=ruta_media(d.get("retrato")), orden=d.get("orden") or 999)
        columnistas.append(a)
    columnistas.sort(key=lambda a: (a["orden"], a["nombre"]))
    validos = {a["slug"] for a in columnistas}

    columnas = []
    for slug, d in leer("columnas"):
        if not requerido("la columna", slug, d, ["titulo", "fecha", "autor"]):
            continue
        autor = slug_de(os.path.splitext(os.path.basename(str(d.get("autor"))))[0])
        if autor not in validos:
            avisos.append(f"La columna '{slug}' apunta a un columnista que no existe o está oculto ({d.get('autor')})")
        c = limpiar(d, ["muestra", "titulo", "cita", "clave"])
        c.update(slug=slug, autor=autor, fecha=fecha(d.get("fecha")), cuerpo=cuerpo(d.get("cuerpo")))
        columnas.append(c)

    erratas = []
    for slug, d in leer("erratas"):
        if not requerido("la sátira", slug, d, ["titulo", "fecha", "tipo"]):
            continue
        e = limpiar(d, ["muestra", "tipo", "destacada", "titulo", "dondeDice", "debeDecir", "resaltar", "nota", "texto"])
        e.update(slug=slug, fecha=fecha(d.get("fecha")))
        if d.get("foto"):
            e["foto"] = ruta_media(d["foto"])
        if d.get("lista"):
            e["lista"] = [limpiar(x, ["dondeDice", "debeDecir"]) for x in d["lista"] if isinstance(x, dict)]
        erratas.append(e)

    for lista in (noticias, columnas, erratas):
        lista.sort(key=lambda x: x["fecha"], reverse=True)

    datos = {"config": config, "noticias": noticias, "columnistas": columnistas, "columnas": columnas, "erratas": erratas}
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write("/* ARCHIVO GENERADO AUTOMÁTICAMENTE: no lo edites a mano.\n")
        f.write("   El contenido se edita en la carpeta contenido/ (o desde Pages CMS)\n")
        f.write("   y este archivo se vuelve a crear con: python3 herramientas/construir.py */\n")
        f.write("window.LVB = ")
        json.dump(datos, f, ensure_ascii=False, indent=1)
        f.write(";\n")

    print(f"contenido.js listo: {len(noticias)} notas, {len(columnistas)} columnistas, "
          f"{len(columnas)} columnas, {len(erratas)} sátiras")
    for a in avisos:
        print("AVISO:", a)


if __name__ == "__main__":
    sys.exit(main())
