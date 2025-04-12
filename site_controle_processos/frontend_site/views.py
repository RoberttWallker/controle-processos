import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .aux_function import atualizarRegistro, data_para_formato_iso, proximoId
from .models import ComprasLentes


#Funções auxiliares do banco de dados
def getRegistroLancamentoDeLentes(id_edicao, request):
    try:
        registro_edicao = ComprasLentes.objects.get(id=id_edicao)
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
    
    except ComprasLentes.DoesNotExist:
        messages.warning(request, f"Registro com ID {id_edicao} não encontrado")
        return None
    
def excluirRegistroLancamentoLentes(request):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Requisição inválida'}, status=400)

    # Verifica se foi passado um ID para edição (via GET)
    id_edicao = request.GET.get('id')

    try:
        registro_edicao = ComprasLentes.objects.get(id=id_edicao)
        registro_edicao.delete()
        return JsonResponse({'success': True, 'message': 'Registro excluído com sucesso!'})

    except ComprasLentes.DoesNotExist:
        return JsonResponse({'success': False, 'message': f'Registro com ID {id_edicao} não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
#Views de registro e autenticação
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Autenticar o usuário
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return render(request, 'frontend_site/auth/login.html')
        else:
            messages.error(request, "E-mail ou senha inválidos.")
            return render(request, 'frontend_site/auth/login.html')

    return render(request, 'frontend_site/auth/login.html')

def register_view(request):
    # Verifica se a senha foi validada na sessão
    if not request.session.get('senha_validada'):
        # Se a senha não foi validada, redireciona para a página de validação
        messages.error(request, "Para se registar, você precisa primeiro solicitar a senha temporária ao administrador e validá-la.")
        return redirect('validar_senha')
    
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirm_senha = request.POST['confirm_senha']

        if senha != confirm_senha:
            messages.error(request, "Senhas não conferem, tente novamente!")
            return render(request, 'frontend_site/auth/register.html', {'nome': nome, 'email': email})
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Este e-mail já está cadastrado!")
            return redirect("register")
        
        user = User.objects.create_user(
            username=nome,
            email=email,
            password=senha
        )

        user.save()

        # Remove a variável de sessão após o registro
        del request.session['senha_validada']

        messages.success(request, "Usuário registrado com sucesso!")
        return render(request, 'frontend_site/auth/register.html')

    return render(request, 'frontend_site/auth/register.html')

#Views de páginas do sistema
@login_required
def admin_panel_view(request):
    return render(request, 'frontend_site/admin_panel/admin_panel.html')

@login_required
def lanc_lentes_view(request):
    # Verifica se foi passado um ID para edição (via GET)
    id_edicao = request.GET.get('id')

    modo_edicao = request.GET.get('edit') == 'true'  # Parâmetro para identificar edição
    registro_data = None
    
    if id_edicao and modo_edicao:
        try:
            id_edicao = int(id_edicao)  # Garante que é um número
        except ValueError:
            raise BadRequest("ID de edição inválido")
        
        try:            
            registro_info = getRegistroLancamentoDeLentes(id_edicao=id_edicao, request=request)
            
            if not registro_info:
                return redirect('lancamento_de_lentes')
                
            registro_data = registro_info['data']
        
        except Exception as e:
            messages.error(request, f"Erro ao buscar registro: {str(e)}")
            registro_data = None
    else:
        registro_data = None

    proximo_id = proximoId(ComprasLentes)
    if request.method == 'POST':
        # Verifica se é uma atualização (PUT via POST)
        if request.POST.get('_method') == 'PUT':
            id_edicao = request.GET.get('id')

            if not id_edicao:
                messages.error(request, "ID do registro não fornecido para atualização")
                return redirect('lancamento_de_lentes')
            
            try:
                registro_info = getRegistroLancamentoDeLentes(id_edicao=id_edicao, request=request)
            
                if not registro_info:
                    return redirect('lancamento_de_lentes')
                
                registro_model = registro_info['model']

                atualizarRegistro(id_edicao=id_edicao, model=registro_model, request=request)
                    
                return redirect('lancamento_de_lentes')

            except Exception as e:
                messages.error(request, f"Erro ao atualizar registro: {str(e)}")
            
            return redirect('lancamento_de_lentes')
        
        #Lançamento de compra de lentes

        try:

            # Converte para dicionário mutável
            post_data = request.POST.dict()

            # Tratamento campos opcionais
            data_liberacao_blu = post_data.get('data_liberacao_blu') or None
            
            try:
                # Extrai o ID esperado do post_data (se existir)
                expected_id = post_data.get('id', proximo_id)

                # Tenta criar com o ID esperado
                try:
                    obj = ComprasLentes.objects.create(
                        id=expected_id,
                        descricao_lente=post_data['descricao_lente'],
                        nota_fiscal=post_data['nota_fiscal'],
                        custo_nota_fiscal=float(post_data['custo_nota_fiscal']),
                        data_compra=post_data['data_compra'],
                        sequencial_savwin=post_data['sequencial_savwin'],
                        referencia_fabricante=post_data['referencia_fabricante'],
                        observacao=post_data['observacao'],
                        ordem_de_servico=post_data['ordem_de_servico'],
                        num_loja=post_data['num_loja'],
                        codigo=post_data['codigo'],
                        num_pedido=post_data['num_pedido'],
                        custo_site=float(post_data['custo_site']),
                        data_liberacao_blu=data_liberacao_blu,
                        valor_pago=float(post_data['valor_pago']),
                        custo_tabela=float(post_data['custo_tabela']),
                        duplicata=post_data['duplicata']
                    )
                    messages.success(request, f"Entrada efetuada com sucesso. ID: {obj.id}") # type: ignore
                    
                except IntegrityError:
                    # Se o ID já existe, cria com novo ID
                    novo_id = ComprasLentes.objects.latest('id').id + 1 # type: ignore
                    obj = ComprasLentes.objects.create(
                        id=novo_id,
                        descricao_lente=post_data['descricao_lente'],
                        nota_fiscal=post_data['nota_fiscal'],
                        custo_nota_fiscal=float(post_data['custo_nota_fiscal']),
                        data_compra=post_data['data_compra'],
                        sequencial_savwin=post_data['sequencial_savwin'],
                        referencia_fabricante=post_data['referencia_fabricante'],
                        observacao=post_data['observacao'],
                        ordem_de_servico=post_data['ordem_de_servico'],
                        num_loja=post_data['num_loja'],
                        codigo=post_data['codigo'],
                        num_pedido=post_data['num_pedido'],
                        custo_site=float(post_data['custo_site']),
                        data_liberacao_blu=data_liberacao_blu,
                        valor_pago=float(post_data['valor_pago']),
                        custo_tabela=float(post_data['custo_tabela']),
                        duplicata=post_data['duplicata']
                    )
                    messages.warning(
                        request,
                        f"O ID {expected_id} já estava em uso. "
                        f"Registro criado com novo ID: {obj.id}" # type: ignore
                    )

                return redirect('lancamento_de_lentes')
            
            except Exception as e:
                messages.error(request, f"Erro ao criar registro: {str(e)}")
                return redirect('lancamento_de_lentes')

        except KeyError as e:
            messages.error(request, f"Campo obrigatório faltando: {e}")
        except ValueError as e:
            messages.error(request, f"Valor numérico inválido: {e}")
        except Exception as e:
            messages.error(request, f"Erro ao salvar: {str(e)}")
    
    context = {
        'proximo_id': proximo_id,
        'registro_edicao': registro_data,
        'modo_edicao': modo_edicao,
        'django_context_json': json.dumps({
            'modoEdicao': modo_edicao,
            'registroEdicao': registro_data
        }, default=str)
    }
    
    return render(request, 'frontend_site/estoque/lancamento_de_lentes.html', context)

def listagem_lancamentos_view(request):
    dados = None
    filtro_aplicado = False
    
    base_queryset = ComprasLentes.objects.defer(
        'usuario_criacao',
        'data_criacao',
        'usuario_atualizacao',
        'data_atualizacao'
    )

    colunas = [
        'id lancamento',
        'data compra',
        'ordem de servico',
        'sequencial savwin',
        'loja',
        'codigo',
        'descricao lente',
        'referencia fabricante',
        'numero pedido',
        'custo site',
        'data liberacao blu',
        'valor pago',
        'custo tabela',
        'nota fiscal',
        'custo nota fiscal',
        'duplicata',
        'observacao'
    ]

    if request.method == 'GET':
        identificador = request.GET.get('identificador', '')
        valor = request.GET.get('valor_identificador', '')

         # Aplicar filtros se existirem
        if identificador and valor:
            filtro_aplicado = True

            if identificador == 'nota_fiscal':
                dados = base_queryset.filter(nota_fiscal=valor)
            elif identificador == 'duplicata':
                dados = base_queryset.filter(duplicata=valor)
            elif identificador == 'numero_pedido':
                dados = base_queryset.filter(numero_pedido=valor)
            elif identificador == 'ordem_servico':
                dados = base_queryset.filter(ordem_de_servico=valor)
            elif identificador == 'loja':
                dados = base_queryset.filter(num_loja=valor)
            elif identificador == 'data_compra':
                valor = data_para_formato_iso(valor)
                dados = base_queryset.filter(data_compra=valor)
                
    context = {
        'colunas': colunas,
        'dados': dados,
        'filtro_aplicado': filtro_aplicado,
        'identificador': request.GET.get('identificador', ''),
        'valor_identificador': request.GET.get('valor_identificador', '')
    }
    
    return render(request, 'frontend_site/estoque/listagem_lancamentos.html', context)   