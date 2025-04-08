from datetime import datetime
from django.forms import ValidationError
from django.utils.dateparse import parse_date

def data_para_formato_iso(data_string):
    if not data_string or not isinstance(data_string, str):
        return None
    # Remove espaços extras
    data_string = data_string.strip()
    
    formatos_adicionais = [
        "%Y-%m-%d",  # 2023/12/31
        "%Y/%m/%d",  # 2023/12/31
        "%d/%m/%Y",  # 31/12/2023
        "%d-%m-%Y",  # 31-12-2023
        "%d.%m.%Y",  # 31.12.2023
        "%d %m %Y",  # 31 12 2023
        "%d/%m/%y",  # 31/12/23 (ano com 2 dígitos)
        "%m/%d/%Y",  # 12/31/2023 (formato americano)
        "%b %d, %Y", # Dec 31, 2023
        "%d %b %Y",  # 31 Dec 2023
    ]

    for formato in formatos_adicionais:
        try:
            data_obj = datetime.strptime(data_string, formato)
            return data_obj.date().isoformat()
        except ValueError:
            continue
    
    raise ValidationError(
        f"Data '{data_string}' não está em um formato reconhecido. "
        "Formatos aceitos: DD/MM/AAAA, AAAA-MM-DD, DD-MM-AAAA, etc."
    )
        
