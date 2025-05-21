Crear ambiente
python -m venv env

Activar ambiente
.\env\Scripts\activate

Instalar los requerimientos (Ejecutar este)
Si no estas en linux o derivados quita esta linea y cuando termines vuelve a ponerla uvloop==0.20.0
pip install -r .\requirements\prod.txt
alembic upgrade head

Agregar FastApi (Ignorar esto)
pip install fastapi
Crear main.py

Correr proyecto con uvicorn 
uvicorn main:app --reload

Correr proyecto con fastapi
fastapi dev main.py

# crear migracion
alembic revision --autogenerate -m "comment"
# aplicar migracion 
alembic upgrade head
