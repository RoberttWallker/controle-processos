from datetime import datetime

from django.contrib import messages
from django.forms import ValidationError

### -----------------------------------------------------
### Helpers
### -----------------------------------------------------

def parse_date_to_iso(data_string):
    """
    Converte uma string de data em formato ISO 8601 (YYYY-MM-DD).
    Suporta múltiplos formatos de entrada.
    
    Args:
        date_string (str): String contendo a data em qualquer formato suportado
        
    Returns:
        str: Data no formato ISO ou None se inválida
        
    Raises:
        ValidationError: Se o formato não for reconhecido
    """
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

### -----------------------------------------------------
### Model CRUD Operations
### -----------------------------------------------------

def update_model_record(id_edicao, model, request):
    """
    Atualiza um registro do modelo com dados de uma requisição POST.
    Converte automaticamente os tipos de campo conforme necessário.
    
    Args:
        record_id: ID do registro a ser atualizado
        model: Instância do modelo Django
        request: Objeto HttpRequest com dados POST
        
    Returns:
        None (salva o modelo diretamente)
    """
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
                field_new_value = parse_date_to_iso(field_new_value) if field_new_value else None
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

def get_next_available_id(model):
    """
    Obtém o próximo ID disponível para um modelo.
    Útil para pré-visualização antes da criação.
    
    Args:
        model: Classe do modelo Django
        
    Returns:
        int: Próximo ID disponível
    """
    try:
        ultimo_id = model.objects.all().order_by('-id').first()
        proximo_id = (ultimo_id.id + 1) if ultimo_id else 1 # type: ignore
    except Exception as e:
        proximo_id = 1  # Fallback caso ocorra algum erro
    
    return proximo_id

### -----------------------------------------------------
### Business Logic
### -----------------------------------------------------

def get_record_lancamento_de_lentes(id_edicao, model, request):
    """
    Obtém um registro específico de lançamento de lentes.
    Inclui validações específicas do domínio.
    
    Args:
        record_id: ID do registro
        model: Modelo de lançamento de lentes
        request: Objeto HttpRequest
        
    Returns:
        Model instance or None
    """
    try:
        registro_edicao = model.objects.get(id=id_edicao)
        # Prepara os dados para o template
        registro_data = {
            'id': registro_edicao.id, # type: ignore
            'descricao_lente': registro_edicao.descricao_lente,
            'nota_fiscal': registro_edicao.nota_fiscal,
            'custo_nota_fiscal': float(registro_edicao.custo_nota_fiscal),
            'data_compra': registro_edicao.data_compra.strftime('%Y-%m-%d') if registro_edicao.data_compra else '',
            'sequencial_savwin': registro_edicao.sequencial_savwin,
            'referencia_fabricante': registro_edicao.referencia_fabricante,
            'observacao': registro_edicao.observacao or '',
            'ordem_de_servico': registro_edicao.ordem_de_servico,
            'num_loja': registro_edicao.num_loja,
            'codigo': registro_edicao.codigo,
            'num_pedido': registro_edicao.num_pedido,
            'custo_site': float(registro_edicao.custo_site),
            'data_liberacao_blu': registro_edicao.data_liberacao_blu.strftime('%Y-%m-%d') if registro_edicao.data_liberacao_blu else '',
            'valor_pago': float(registro_edicao.valor_pago),
            'custo_tabela': float(registro_edicao.custo_tabela),
            'duplicata': registro_edicao.duplicata
        }
        return {
            'model': registro_edicao, #Retorna o objeto do banco de dados (para updates)
            'data': registro_data #Retorna dicinário formatado (para templates)
        }
    
    except model.DoesNotExist:
        messages.warning(request, f"Registro com ID {id_edicao} não encontrado")
        return None