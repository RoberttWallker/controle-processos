from datetime import datetime

from django.contrib import messages
from django.forms import ValidationError


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

# Faz a atualização de um registro, passando o ID do registro, Model e Request
# para capturar os dados e responder.
def atualizarRegistro(id_edicao, model, request):
    for attr in request.POST:
        if attr in ['csrfmiddlewaretoken', '_method']:  # Ignora campos especiais
            continue

        if hasattr(model, attr):
            field = model._meta.get_field(attr)
            field_new_value = request.POST[attr]

            # Conversão de tipos
            if field.get_internal_type() in ('FloatField', 'DecimalField'):
                field_new_value = float(field_new_value) if field_new_value else 0.0
            elif field.get_internal_type() == 'DateField':
                field_new_value = data_para_formato_iso(field_new_value) if field_new_value else None
            elif field.get_internal_type() == 'IntegerField':
                field_new_value = int(field_new_value) if field_new_value else 0
            elif field.get_internal_type() in ('TextField', 'CharField'):
                field_new_value = str(field_new_value) if field_new_value else ''
            elif field.get_internal_type() == 'BooleanField':
                field_new_value = field_new_value.lower() in ('true', '1', 'yes') if field_new_value else False

            setattr(model, attr, field_new_value)

        else:
            print(f"O campo {attr} não existe no modelo")

    model.save()
    messages.success(request, f"Registro ID {id_edicao} atualizado com sucesso!")

# Calcula o próximo ID disponível
def proximoId(model):
    try:
        ultimo_id = model.objects.all().order_by('-id').first()
        proximo_id = (ultimo_id.id + 1) if ultimo_id else 1 # type: ignore
    except Exception as e:
        proximo_id = 1  # Fallback caso ocorra algum erro
    
    return proximo_id