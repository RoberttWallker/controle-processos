import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .aux_function import (
    get_next_available_id,
    update_model_record,
    parse_date_to_iso,
    get_record_lancamento_de_lentes
)

from .models import (
    ComprasLentes
)

# Views de CRUD
@login_required  
def LancamentoLentesDeleteView(request):
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
    
# Views de registro e autenticação
def LogoutView(request):
    logout(request)
    return redirect('login')

def LoginView(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password = request.POST['password']
        
        # Autenticar o usuário
        try:
            user = User.objects.get(username=usuario)
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

def RegisterView(request):
    # Verifica se a senha foi validada na sessão
    if not request.session.get('senha_validada'):
        # Se a senha não foi validada, redireciona para a página de validação
        messages.error(request, "Para se registar, você precisa primeiro solicitar a senha temporária ao administrador e validá-la.")
        return redirect('validar_senha')
    
    if request.method == 'POST':
        usuario = request.POST['usuario']
        primeiro_nome = request.POST['primeiro_nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirm_senha = request.POST['confirm_senha']

        if senha != confirm_senha:
            messages.error(request, "Senhas não conferem, tente novamente!")
            return render(request, 'frontend_site/auth/register.html', 
                {
                    'usuario': usuario,
                    'primeiro_nome': primeiro_nome,
                    'sobrenome': sobrenome,
                    'email': email,
                }
            )
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado!")
            return redirect("register")
        
        try:
            user = User.objects.create_user(
                username=usuario,
                first_name=primeiro_nome,
                last_name=sobrenome,
                email=email,
                password=senha
            )

            user.save()

            # Remove a variável de sessão após o registro
            del request.session['senha_validada']

            messages.success(request, "Usuário registrado com sucesso!")

        except IntegrityError:
            messages.error(request, "Este nome de usuário já está em uso!")
            return redirect("register")
        
        return render(request, 'frontend_site/auth/register.html')

    return render(request, 'frontend_site/auth/register.html')

# Views de telas
@login_required
def AdminPanelView(request):
    return render(request, 'frontend_site/admin_panel/admin_panel.html')

@login_required
def LancamentoLentesCreateView(request):
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
            registro_info = get_record_lancamento_de_lentes(id_edicao=id_edicao, model= ComprasLentes, request=request)
            
            if not registro_info:
                return redirect('lancamento_de_lentes')
                
            registro_data = registro_info['data']
        
        except Exception as e:
            messages.error(request, f"Erro ao buscar registro: {str(e)}")
            registro_data = None
    else:
        registro_data = None

    proximo_id = get_next_available_id(ComprasLentes)
    if request.method == 'POST':
        # Verifica se é uma atualização (PUT via POST)
        if request.POST.get('_method') == 'PUT':
            id_edicao = request.GET.get('id')

            if not id_edicao:
                messages.error(request, "ID do registro não fornecido para atualização")
                return redirect('lancamento_de_lentes')
            
            try:
                registro_info = get_record_lancamento_de_lentes(id_edicao=id_edicao, model= ComprasLentes, request=request)
            
                if not registro_info:
                    return redirect('lancamento_de_lentes')
                
                registro_model = registro_info['model']

                update_model_record(id_edicao=id_edicao, model=registro_model, request=request)
                    
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

@login_required
def LancamentoLentesListView(request):
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
                valor = parse_date_to_iso(valor)
                dados = base_queryset.filter(data_compra=valor)
                
    context = {
        'colunas': colunas,
        'dados': dados,
        'filtro_aplicado': filtro_aplicado,
        'identificador': request.GET.get('identificador', ''),
        'valor_identificador': request.GET.get('valor_identificador', '')
    }
    
    return render(request, 'frontend_site/estoque/listagem_lancamentos.html', context)   