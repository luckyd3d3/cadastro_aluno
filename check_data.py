import re
from enum import Enum, auto


class Checks(Enum):
    OK = auto()
    IDADE = auto()
    NOME = auto()
    TELEFONE = auto()
    EMAIL = auto()
    ETNIA = auto()
    CPF = auto()
    FAIXA_SALARIAL = auto()
    PESSOAS_FAMILIA = auto()
    RELIGIÃO = auto()


def check_data(
        idade: str = "1",
        nome: str = "",
        etnia: str = "Amarelo",
        telefone: str = "1111111111",
        email: str = "a@b.com",
        cpf: str = "76685756268",
        faixa_salarial: str = "0",
        pessoas_familia: str = "0",
        religião: str = "",
) -> list[Checks]:
    checks_failed: list[Checks] = []

    if not check_idade(idade):
        checks_failed.append(Checks.IDADE)
    if not check_str(nome):
        checks_failed.append(Checks.NOME)
    if not check_telefone(telefone):
        checks_failed.append(Checks.TELEFONE)
    if not check_email(email):
        checks_failed.append(Checks.EMAIL)
    if not check_cpf(cpf):
        checks_failed.append(Checks.CPF)
    if etnia == "Selecione":
        checks_failed.append(Checks.ETNIA)
    if not check_faixa_salarial(faixa_salarial):
        checks_failed.append(Checks.FAIXA_SALARIAL)
    if not check_familia(pessoas_familia):
        checks_failed.append(Checks.PESSOAS_FAMILIA)
    if not check_str(religião):
        checks_failed.append(Checks.RELIGIÃO)

    if checks_failed:
        return checks_failed

    return [Checks.OK]


def check_idade(idade: str) -> bool:
    if not idade.isdigit():
        return False
    elif 1 >= int(idade) >= 122:
        return False

    return True


def check_cpf(cpf: str) -> bool:
    cpf_digits_rex = re.compile(r"^\d{11}$")
    cpf_repeat_rex = re.compile(r"^(\d)\1*$")

    cpf = cpf.replace(".", "").replace("-", "")

    if not cpf_digits_rex.match(cpf) or cpf_repeat_rex.match(cpf):
        return False

    checksum = [0, 0]

    for i, n in enumerate(cpf[:-1]):
        if i != 9:
            checksum[0] += int(n) * (10 - i)
        checksum[1] += int(n) * (11 - i)

    checksum[0] = (checksum[0] * 10) % 11
    checksum[0] = 0 if checksum[0] == 10 else checksum[0]
    checksum[1] = (checksum[1] * 10) % 11
    checksum[1] = 0 if checksum[1] == 10 else checksum[1]

    if checksum[0] != int(cpf[9]) or checksum[1] != int(cpf[10]):
        return False

    return True


def check_email(email: str) -> bool:
    email_rex = re.compile(r"^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$")

    email = email.strip()

    if len(email) > 255 or not email_rex.match(email):
        return False

    return True


def check_telefone(telefone: str) -> bool:
    telefone_rex = re.compile(r"^(55)?(?:([1-9]{2})?)(\d{4,5})(\d{4})$")

    telefone = telefone.replace("+", "").replace("-", "").replace(" ", "").strip()

    if not telefone_rex.match(telefone):
        return False

    return True


def check_str(string: str) -> bool:
    if len(string) > 512:
        return False

    return True


def check_faixa_salarial(faixa_salarial: str) -> bool:
    if not is_float(faixa_salarial):
        return False
    elif float(faixa_salarial) < 0:
        return False

    return True


def check_familia(familia: str) -> bool:
    if not familia.isdigit():
        return False
    elif int(familia) < 0:
        return False

    return True


def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except:
        return False


def in_check(check: Checks, list: list[Checks]) -> bool:
    return any([check.value == i.value for i in list])


if __name__ == "__main__":
    data = check_data(
        "19",
        "A",
        "111111111",
        "C",
        "D",
        "Selecione",
        "10a",
        "10.1",
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    )

    print(data)