from config.wsgi import *
from core.sweb.models import *
from core.user.models import User
import pandas as pd
import numpy as np
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


def clientesimport():
    # Cliente
    dtcliente = pd.read_csv(IMPORT_FOLDER + 'rprovcli.csv', sep='|', dtype=str)
    # print(dtcliente)

    dttipocli = pd.read_sql_query('select id as tcr_id, tcr_codigo as P_TIPOCL from sirtbtcr', engine)
    # print(dttipocli)
    # Hacemos el merge para poder obtener el id
    dtcli2 = pd.merge(dtcliente, dttipocli, how='left', on='P_TIPOCL')
    # print(dtcli2)
    # dtcli2.to_csv(IMPORT_FOLDER+'dtcli2.csv', index=False)

    dtbanco = pd.read_sql_query('select id as ban_id, ban_codcsp, ban_sucursal from sirtbban', engine)
    # Hacemos el merge para poder obtener el id
    dtcli3 = pd.merge(dtcli2, dtbanco, how='left', left_on=['P_COD_BAN', 'P_SUCUR'], right_on=['ban_codcsp', 'ban_sucursal'])
    # dtcli3.to_csv(IMPORT_FOLDER+'dtcli3.csv', index=False)

    dtfpago = pd.read_sql_query('select id as fpg_id, fpg_codigo as P_FORM_PAG from sirtbfpg', engine)
    # Hacemos el merge para poder obtener el id
    dtcli4 = pd.merge(dtcli3, dtfpago, how='left', on='P_FORM_PAG')
    # dtcli4.to_csv(IMPORT_FOLDER+'dtcli4.csv', index=False)

    dtdtomo = pd.read_sql_query('select id as dmo_id, dmo_codigo as P_C_DTOMO from sirtbdmo', engine)
    # Hacemos el merge para poder obtener el id
    dtcli5 = pd.merge(dtcli4, dtdtomo, how='left', on='P_C_DTOMO')
    # dtcli5.to_csv(IMPORT_FOLDER+'dtcli5.csv', index=False)

    # Eliminamos las columnas que no necesitamos
    dtcli5.drop([
        'Unnamed: 0',
        'P_TIPOCL',
        'P_COD_BAN',
        'P_SUCUR',
        'ban_codcsp',
        'ban_sucursal',
        'P_FORM_PAG',
        'P_C_DTOMO',
        'P_PERFACD',
        'P_PERFACH',
    ], axis=1, inplace=True)

    # Renombramos las columnas con los nombres de las columnas en rprovcli
    dtcli5.rename(columns={
        'P_CODIGO': 'cli_codigo',
        'P_RAZSOC': 'cli_rsocial',
        'tcr_id': 'cli_tipcli',
        'P_DIREC': 'cli_direccion',
        'P_POBLA': 'cli_poblacion',
        'P_PROVIN': 'cli_provincia',
        'P_CPOST': 'cli_cpostal',
        'P_CIF': 'cli_cif',
        'P_TFNO': 'cli_telefono',
        'P_FAX': 'cli_fax',
        'P_IN_TFNO': 'cli_tlfmovil',
        'ban_id': 'cli_banco',
        'P_CTA': 'cli_cuenta',
        'fpg_id': 'cli_fpago',
        'P_DIASPAG': 'cli_diapagod',
        'P_DIASPAG1': 'cli_diapagoh',
        'P_C_DTOPZA': 'cli_dtopieza',
        'dmo_id': 'cli_dtomo',
        'P_DTOESP': 'cli_dtoesp',
        'P_F_ULFAC': 'cli_fultfac',
        'P_CREDISPO': 'cli_credispo',
        'P_CREDISPU': 'cli_credispu',
        'P_COD_BLOQ': 'cli_bloqcred',
        'P_IMVEREM': 'cli_imprecmes',
        'P_IMVEREA': 'cli_imprecano',
        'P_IMVEREA1': 'cli_imprecanoant',
        'P_COSVEREM': 'cli_cosrecmes',
        'P_COSVEREA': 'cli_cosrecano',
        'P_COSVREA1': 'cli_cosrecanoant',
        'P_IMVETAM': 'cli_imptalmes',
        'P_IMVETAA': 'cli_imptalano',
        'P_IMVETA1': 'cli_imptalanoant',
        'P_COSVETAM': 'cli_costalmes',
        'P_COSVETAA': 'cli_costalano',
        'P_COSVETA1': 'cli_costalanoant',
        'P_F_ULMOV': 'cli_fultmov',
        'P_COMPRAME': 'cli_comprasmes',
        'P_COMPRANO': 'cli_comprasano',
        'P_COMPRA1': 'cli_comprasanoant',
        'P_EMIREC': 'cli_emirec',
        'P_APLI_IVA': 'cli_apliva',
        'P_IRTM': 'cli_imprectalmes',
        'P_IRTA': 'cli_imprectalano',
        'P_IRTA1': 'cli_imprectalanoant',
        'P_CRTM': 'cli_cosrectalmes',
        'P_CRTA': 'cli_cosrectalano',
        'P_CRTA1': 'cli_cosrectalanoant',
        'P_ALBARSN': 'cli_lstnetdto',
        'P_MAILEXT': 'cli_exentomail',
        'P_PASAPORT': 'cli_pasaporte',
        'P_NOTA': 'cli_notas',
        'P_PVP_MO': 'cli_preciomo',
        'P_FEC_NAC': 'cli_fenaci',
        'P_IVAESP': 'cli_ivaesp',
        'P_MAIL': 'cli_email',
        'P_SMS': 'cli_envsms',
        'P_NOCTA': 'cli_ocucta',
        'P_IBAN': 'cli_iban',
        'P_DC': 'cli_dc'
    }, inplace=True)

    # Conversiones de tipo
    colsfloat = [
        'cli_diapagod',
        'cli_diapagoh',
        'cli_dtoesp',
        'cli_credispo',
        'cli_credispu',
        'cli_imprecmes',
        'cli_imprecano',
        'cli_imprecanoant',
        'cli_cosrecmes',
        'cli_cosrecano',
        'cli_cosrecanoant',
        'cli_imptalmes',
        'cli_imptalano',
        'cli_imptalanoant',
        'cli_costalmes',
        'cli_costalano',
        'cli_costalanoant',
        'cli_comprasmes',
        'cli_comprasano',
        'cli_comprasanoant',
        'cli_imprectalmes',
        'cli_imprectalano',
        'cli_imprectalanoant',
        'cli_cosrectalmes',
        'cli_cosrectalano',
        'cli_cosrectalanoant',
        'cli_preciomo',
        'cli_ivaesp',
    ]
    colsint = [
        'cli_diapagod',
        'cli_diapagoh'
    ]
    colsdatetime = [
        'cli_fultfac',
        'cli_fultmov',
        'cli_fenaci',
    ]
    colsdate = [
        'cli_fenaci',
    ]
    dbool = {
        'N': False,
        'S': True,
    }
    colsboolean = [
        'cli_bloqcred',
        'cli_emirec',
        'cli_apliva',
        'cli_lstnetdto',
        'cli_exentomail',
        'cli_ocucta',
    ]
    dtcli5['cli_ocucta'].where(dtcli5['cli_ocucta'].isin(['N', 'S']), 'N', inplace=True)
    dtcli5[colsfloat] = dtcli5[colsfloat].astype('float')
    dtcli5[colsfloat] = dtcli5[colsfloat].round(decimals=2)
    # convertimos primero a float y luego a int ya que son strings
    dtcli5[colsint] = dtcli5[colsint].astype('int64')
    dtcli5[colsdatetime] = dtcli5[colsdatetime].apply(pd.to_datetime)
    dtcli5['cli_fenaci'] = dtcli5['cli_fenaci'].dt.date
    # dtcli5[colsboolean].replace(dbool)
    dtcli5[colsboolean] = dtcli5[colsboolean].replace(dbool)
    dtcli5['cli_envsms'].where(dtcli5['cli_envsms'].isin(['0', '1', '2', '3', '4']), '0', inplace=True)
    # print(dtcli5['cli_envsms'])

    # Borramos el contenido de la tabla antes de insertar
    Cliente.objects.all().delete()
    # print(Cliente.objects.all())
    #
    # Insertamos todos los datos del dataframe en la tabla
    dtcli5.to_sql('sirtbcli', engine, if_exists='append', index=False)

    # Actualizamos campos de auditoría
    Cliente.objects.all().update(user_creation=USER_CREATION_ID)
    Cliente.objects.all().update(date_creation=datetime.now())

    print(pd.read_sql_query('select * from sirtbcli', engine))


# formasdepagoimport()
# tiposclienterecambiosimport()
# descuentosmoimport()
# bancosimport()
clientesimport()
