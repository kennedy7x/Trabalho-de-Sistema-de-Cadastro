import re
from datetime import datetime

class Validators:
    
    @staticmethod
    def validar_cpf(cpf):
        """Valida CPF"""
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf) != 11:
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto
        
        if int(cpf[9]) != digito1:
            return False
        
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto
        
        if int(cpf[10]) != digito2:
            return False
        
        return True
    
    @staticmethod
    def validar_cnpj(cnpj):
        """Valida CNPJ"""
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        if len(cnpj) != 14:
            return False
        
        if cnpj == cnpj[0] * 14:
            return False
        
        peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(12):
            soma += int(cnpj[i]) * peso1[i]
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto
        
        if int(cnpj[12]) != digito1:
            return False
        
        peso2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(13):
            soma += int(cnpj[i]) * peso2[i]
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto
        
        if int(cnpj[13]) != digito2:
            return False
        
        return True
    
    @staticmethod
    def validar_email(email):
        """Valida formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None
    
    @staticmethod
    def validar_celular(celular):
        """Valida formato do celular"""
        celular = re.sub(r'[^0-9]', '', celular)
        
        if len(celular) not in [10, 11]:
            return False
        
        ddd = int(celular[:2])
        if ddd < 11 or ddd > 99:
            return False
        
        return True
    
    @staticmethod
    def validar_cep(cep):
        """Valida formato do CEP"""
        cep = re.sub(r'[^0-9]', '', cep)
        return len(cep) == 8
    
    @staticmethod
    def validar_nome_completo(nome):
        """Valida se o nome tem pelo menos nome e sobrenome"""
        nome = nome.strip()
        # Verifica se tem pelo menos 2 palavras (nome + sobrenome)
        palavras = nome.split()
        if len(palavras) < 2:
            return False
        # Verifica se cada palavra tem pelo menos 2 caracteres
        for palavra in palavras:
            if len(palavra) < 2:
                return False
        return True
    
    @staticmethod
    def identificar_tipo_documento(documento):
        """Identifica se é CPF ou CNPJ"""
        documento = re.sub(r'[^0-9]', '', documento)
        if len(documento) == 11:
            return 'CPF'
        elif len(documento) == 14:
            return 'CNPJ'
        return None
    
    @staticmethod
    def formatar_cpf_cnpj(documento):
        """Formata CPF ou CNPJ"""
        documento = re.sub(r'[^0-9]', '', documento)
        
        if len(documento) == 11:
            return f"{documento[:3]}.{documento[3:6]}.{documento[6:9]}-{documento[9:]}"
        elif len(documento) == 14:
            return f"{documento[:2]}.{documento[2:5]}.{documento[5:8]}/{documento[8:12]}-{documento[12:]}"
        return documento
    
    @staticmethod
    def formatar_celular(celular):
        """Formata número de celular"""
        celular = re.sub(r'[^0-9]', '', celular)
        
        if len(celular) == 11:
            return f"({celular[:2]}) {celular[2:7]}-{celular[7:]}"
        elif len(celular) == 10:
            return f"({celular[:2]}) {celular[2:6]}-{celular[6:]}"
        return celular
    
    @staticmethod
    def formatar_cep(cep):
        """Formata CEP"""
        cep = re.sub(r'[^0-9]', '', cep)
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep