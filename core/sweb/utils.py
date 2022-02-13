from django.core.exceptions import ValidationError


def digitos_control(cuenta:str):
    """Calcula el dígito de control de una CCC.
    Recibe una lista con 10 numeros enteros y devuelve el DC
    correspondiente"""
    # print(cuenta)
    if not cuenta.isdigit() or len(cuenta) != 10:
        raise ValidationError('La cuenta debe tener 10 dígitos: %(value)s', code='ctainvalid', params={'value': cuenta})

    factores = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
    resultado = 11 - sum(int(d) * f for d, f in zip(cuenta, factores)) % 11
    # print(resultado)
    if resultado == 10:
        return str(1)
    if resultado == 11:
        return str(0)
    return str(resultado)


def validar_porcentaje(value):
    if value and ((value > 100) or (value < 0)):
        raise ValidationError(f"{value} no es un porcentaje válido")
