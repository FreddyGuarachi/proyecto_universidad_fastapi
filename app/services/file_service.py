import os
import uuid
from fastapi import UploadFile, HTTPException, status

UPLOAD_ALUMNOS_IMAGES = "uploads/alumnos/images"


async def save_image(file: UploadFile, alumno_id: int):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Formato no aceptado",
        )

    contenido = await file.read()

    nombre_unico = f"{uuid.uuid4()}_{file.filename}"

    ruta_carpeta = f"{UPLOAD_ALUMNOS_IMAGES}/alumno_{alumno_id}"

    os.makedirs(ruta_carpeta, exist_ok=True)

    ruta_imagen = f"{ruta_carpeta}/{nombre_unico}"

    with open(ruta_imagen, "wb") as f:
        f.write(contenido)

    return ruta_imagen
