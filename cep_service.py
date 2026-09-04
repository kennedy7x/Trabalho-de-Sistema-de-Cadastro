import requests
import json

class CEPService:
    def __init__(self):
        self.base_url = "https://viacep.com.br/ws/"
        self.timeout = 10  # segundos
        
    def consultar_cep(self, cep):
        """
        Consulta o endereço pelo CEP usando a API ViaCEP
        
        Retorna:
        - Sucesso: dict com os dados do endereço
        - Erro: dict com mensagem de erro
        """
        # Remove caracteres especiais
        cep = ''.join(filter(str.isdigit, cep))
        
        # Verifica se o CEP tem 8 dígitos
        if len(cep) != 8:
            return {
                'success': False,
                'error': 'CEP inválido. O CEP deve ter 8 dígitos.',
                'code': 'INVALID_CEP'
            }
        
        try:
            # Faz a consulta à API
            url = f"{self.base_url}{cep}/json/"
            response = requests.get(url, timeout=self.timeout)
            
            # Verifica o status da resposta
            if response.status_code == 200:
                data = response.json()
                
                # Verifica se o CEP foi encontrado
                if 'erro' in data:
                    return {
                        'success': False,
                        'error': 'CEP não encontrado. Verifique o número informado.',
                        'code': 'CEP_NOT_FOUND'
                    }
                
                # Retorna os dados do endereço
                return {
                    'success': True,
                    'data': {
                        'logradouro': data.get('logradouro', ''),
                        'bairro': data.get('bairro', ''),
                        'cidade': data.get('localidade', ''),
                        'estado': data.get('uf', ''),
                        'cep': data.get('cep', ''),
                        'complemento': data.get('complemento', '')
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro na consulta: {response.status_code}',
                    'code': 'API_ERROR'
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Tempo limite excedido. Verifique sua conexão com a internet.',
                'code': 'TIMEOUT'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Erro de conexão. Verifique sua internet.',
                'code': 'CONNECTION_ERROR'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Erro ao consultar CEP: {str(e)}',
                'code': 'REQUEST_ERROR'
            }
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': 'Erro ao processar resposta do servidor.',
                'code': 'PARSE_ERROR'
            }