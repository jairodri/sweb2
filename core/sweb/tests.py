from config.wsgi import *
from core.sweb.models import *
from core.user.models import User
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

IMPORT_FOLDER = 'C:/Users/jairodri/Util/Python/Projects/testpyodbc/export/'
DATABASE_SQLITE = 'C:\\Users\\jairodri\\Util\\Python\\Projects\\sweb2\\dbsweb.sqlite3'
USER_CREATION_ID = User.objects.get(username='system')

# Conexión para sqlite con 3 /// para indicar dirección absoluta
conn = 'sqlite:///' + DATABASE_SQLITE
print(conn)
engine = create_engine(conn, echo=True)


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
    # print(FormaDePago.objects.all())

    # Insertamos todos los datos del dataframe en la tabla
    dtFormasPago.to_sql('sirtbfpg', engine, if_exists='append', index=False)

    # Actualizamos campos de auditoría
    FormaDePago.objects.all().update(user_creation=USER_CREATION_ID)
    FormaDePago.objects.all().update(date_creation=datetime.now())

    # print(pd.read_sql_query('select * from sirtbfpg', engine))


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
    # print(TipoClienteRecambios.objects.all())

    # Insertamos todos los datos del dataframe en la tabla
    dttiposclienterecambios.to_sql('sirtbtcr', engine, if_exists='append', index=False)

    # Actualizamos campos de auditoría
    TipoClienteRecambios.objects.all().update(user_creation=USER_CREATION_ID)
    TipoClienteRecambios.objects.all().update(date_creation=datetime.now())

    # print(pd.read_sql_query('select * from sirtbtcr', engine))


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
    # print(DescuentoMO.objects.all())

    # Insertamos todos los datos del dataframe en la tabla
    dtDescuentosMo.to_sql('sirtbdmo', engine, if_exists='append', index=False)

    # Actualizamos campos de auditoría
    DescuentoMO.objects.all().update(user_creation=USER_CREATION_ID)
    DescuentoMO.objects.all().update(date_creation=datetime.now())

    print(pd.read_sql_query('select * from sirtbdmo', engine))


def bancosimport():
    # Banco
    dtbanco = pd.read_csv(IMPORT_FOLDER + 'bdbancos.csv', sep='|', dtype=str)
    # dtbanco['B_PREF_TEL'] = dtbanco['B_PREF_TEL'].astype(int)
    print(dtbanco)

    # Eliminamos las columnas que no necesitamos
    dtbanco.drop(['Unnamed: 0'], axis=1, inplace=True)

    # Renombramos las columnas con los nombres de las columnas en rarticul
    dtbanco.rename(columns={'B_COD_CSP': 'ban_codcsp',
                            'B_SUCURSAL': 'ban_sucursal',
                            'B_CUENTA': 'ban_cuenta',
                            'B_DGC': 'ban_dgc',
                            'B_DGC2': 'ban_dgc2',
                            'B_COD_BCOE': 'ban_codbcoe',
                            'B_RAZON': 'ban_rsocial',
                            'B_VIA_PUBL': 'ban_tipovia',
                            'B_NOMBREVP': 'ban_nomvia',
                            'B_NUM_VP': 'ban_numvia',
                            'B_CPOSTAL': 'ban_cpostal',
                            'B_MUNICIPI': 'ban_mncipio',
                            'B_PROVINCI': 'ban_provin',
                            'B_TELEX': 'ban_telex',
                            'B_PREF_TEL': 'ban_preftel',
                            'B_NUM_TELF': 'ban_telef',
                            'B_TELF_PER': 'ban_telper',
                            'B_EXT_TEL': 'ban_extelf',
                            'B_NOM_CONT': 'ban_contac'
                            },
                   inplace=True)

    # Borramos el contenido de la tabla antes de insertar
    Banco.objects.all().delete()
    # print(Banco.objects.all())
    #
    # Insertamos todos los datos del dataframe en la tabla
    dtbanco.to_sql('sirtbban', engine, if_exists='append', index=False)

    # Actualizamos campos de auditoría
    Banco.objects.all().update(user_creation=USER_CREATION_ID)
    Banco.objects.all().update(date_creation=datetime.now())

    print(pd.read_sql_query('select * from sirtbban', engine))


# formasdepagoimport()
# tiposclienterecambiosimport()
# descuentosmoimport()
bancosimport()
