from django.test import TestCase
from config.wsgi import *
from core.sweb.models import *
import pandas as pd
from sqlalchemy import create_engine

IMPORT_FOLDER = 'C:/Users/jairodri/Util/Python/Projects/testpyodbc/export/'
DATABASE_SQLITE = 'C:\\Users\\jairodri\\Util\\Python\\Projects\\sweb2\\dbsweb.sqlite3'


def formasdepagoimport():
    # Formas de Pago - tabla 007
    dtFormasPago = pd.read_csv(IMPORT_FOLDER + 'rtablas007.csv', sep='|', dtype=str)
    dtFormasPago['t_elemn'] = dtFormasPago['t_elemn'].astype(int)
    dtFormasPago['t_elemn2'] = dtFormasPago['t_elemn2'].astype(int)
    # print(dtFormasPago)

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

    print(pd.read_sql_query('select * from sirtbfpg', engine))


def tiposclienterecambiosimport():
    #  Tipos Cliente Recambios- tabla 003
    dttiposclienterecambios = pd.read_csv(IMPORT_FOLDER + 'rtablas003.csv', sep='|', dtype=str)
    # print(dttiposclienterecambios)

    # Eliminamos las columnas que no necesitamos
    dttiposclienterecambios.drop(['Unnamed: 0'], axis=1, inplace=True)

    # Renombramos las columnas
    dttiposclienterecambios.rename(columns={'t_clavec': 'tcr_codigo',
                                            't_elemc': 'tcr_descrip',
                                            't_elemc2': 'tcr_datocon'},
                                   inplace=True)

    # Borramos el contenido de la tabla antes de insertar
    TipoClienteRecambios.objects.all().delete()
    print(TipoClienteRecambios.objects.all())

    # Conexión para sqlite con 3 /// para indicar dirección absoluta
    conn = 'sqlite:///' + DATABASE_SQLITE
    print(conn)
    engine = create_engine(conn, echo=True)

    # Insertamos todos los datos del dataframe en la tabla
    dttiposclienterecambios.to_sql('sirtbtcr', engine, if_exists='append', index=False)

    print(pd.read_sql_query('select * from sirtbtcr', engine))


def descuentosmoimport():
    # Descuentos MO - tabla 002
    dtDescuentosMo = pd.read_csv(IMPORT_FOLDER + 'rtablas002.csv', sep='|', dtype=str)
    dtDescuentosMo['t_elemn'] = dtDescuentosMo['t_elemn'].astype(float)
    print(dtDescuentosMo)

    # Eliminamos las columnas que no necesitamos
    dtDescuentosMo.drop(['Unnamed: 0'], axis=1, inplace=True)

    # Renombramos las columnas con los nombres de las columnas en rarticul
    dtDescuentosMo.rename(columns={'t_clavec': 'dmo_codigo',
                                   't_elemc': 'dmo_descrip',
                                   't_elemn': 'dmo_descuento'},
                          inplace=True)

    # Borramos el contenido de la tabla antes de insertar
    DescuentoMO.objects.all().delete()
    print(DescuentoMO.objects.all())

    # Conexión para sqlite con 3 /// para indicar dirección absoluta
    conn = 'sqlite:///' + DATABASE_SQLITE
    print(conn)
    engine = create_engine(conn, echo=True)

    # Insertamos todos los datos del dataframe en la tabla
    dtDescuentosMo.to_sql('sirtbdmo', engine, if_exists='append', index=False)

    print(pd.read_sql_query('select * from sirtbdmo', engine))

# formasdepagoimport()
# tiposclienterecambiosimport()
descuentosmoimport()


