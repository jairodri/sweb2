from django.test import TestCase
from config.wsgi import *
from core.sweb.models import *
import pandas as pd
from sqlalchemy import create_engine

IMPORT_FOLDER = 'C:/Users/jairodri/Util/Python/Projects/testpyodbc/export/'
DATABASE_SQLITE = 'C:\\Users\\jairodri\\Util\\Python\\Projects\\sweb2\\dbsweb.sqlite3'

# Formas de Pago - tabla 007
dtFormasPago = pd.read_csv(IMPORT_FOLDER + 'rtablas007.csv', sep='|', dtype=str)
dtFormasPago['t_elemn'] = dtFormasPago['t_elemn'].astype(int)
dtFormasPago['t_elemn2'] = dtFormasPago['t_elemn2'].astype(int)
print(dtFormasPago)

# Eliminamos las columnas que no necesitamos
dtFormasPago.drop(['Unnamed: 0'], axis=1, inplace=True)

# Renombramos las columnas con los nombres de las columnas en rarticul
dtFormasPago.rename(columns={'t_clavec': 'fpg_codigo',
                             't_elemc': 'fpg_descrip',
                             't_elemn': 'fpg_diasvto',
                             't_elemn2': 'fpg_recibos'},
                    inplace=True)

# Borramos el contenido de la tabla antes de insertar
FormaDePago.objects.all().delete()
print(FormaDePago.objects.all())

# Conexión para sqlite con 3 /// para indicar dirección absoluta
conn = 'sqlite:///' + DATABASE_SQLITE
print(conn)
engine = create_engine(conn, echo=True)

# Insertamos todos los datos del dataframe en la tabla
dtFormasPago.to_sql('sirtbfpg', engine, if_exists='append', index=False)

print(pd.read_sql_query('select * from sirtbfpg',engine))
