import json
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ComprasLentes
from .aux_function import data_para_formato_iso
from django.core.serializers import serialize

# Create your views here.
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

@login_required
def admin_panel_view(request):
    return render(request, 'frontend_site/admin_panel/admin_panel.html')

@login_required
def lanc_lentes_view(request):
    # Calcula o próximo ID disponível
    try:
        ultimo_id = ComprasLentes.objects.all().order_by('-id').first()
        proximo_id = (ultimo_id.id + 1) if ultimo_id else 1 # type: ignore
    except Exception as e:
        proximo_id = 1  # Fallback caso ocorra algum erro

    # Verifica se foi passado um ID para edição (via GET)
    id_edicao = request.GET.get('id')
    modo_edicao = request.GET.get('edit') == 'true'  # Novo parâmetro para identificar edição

    registro_edicao = None
    
    if id_edicao and modo_edicao:
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
                'ordem_servico': registro_edicao.ordem_servico,
                'loja': registro_edicao.loja,
                'codigo': registro_edicao.codigo,
                'numero_pedido': registro_edicao.numero_pedido,
                'custo_site': float(registro_edicao.custo_site),
                'data_liberacao_blu': registro_edicao.data_liberacao_blu.strftime('%Y-%m-%d') if registro_edicao.data_liberacao_blu else '',
                'valor_pago': float(registro_edicao.valor_pago),
                'custo_tabela': float(registro_edicao.custo_tabela),
                'duplicata': registro_edicao.duplicata
            }
        
        except ComprasLentes.DoesNotExist:
            messages.warning(request, f"Registro com ID {id_edicao} não encontrado")
            registro_data = None
        except Exception as e:
            messages.error(request, f"Erro ao buscar registro: {str(e)}")
            registro_data = None
    else:
        registro_data = None

    if request.method == 'POST':
                # Verifica se é uma atualização (PUT via POST)
        if request.POST.get('_method') == 'PUT':
            id_edicao = request.GET.get('id')
            if not id_edicao:
                messages.error(request, "ID do registro não fornecido para atualização")
                return redirect('lancamento_de_lentes')
            
            try:
                registro = ComprasLentes.objects.get(id=id_edicao)
                
                # Atualiza os campos
                registro.descricao_lente = request.POST['descricao']
                registro.nota_fiscal = request.POST['nota_fiscal']
                registro.custo_nota_fiscal = float(request.POST['custo_nota_fiscal'])
                registro.data_compra = request.POST['data_compra']
                registro.sequencial_savwin = request.POST['sequencial_prod']
                registro.referencia_fabricante = request.POST['ref_fabricante']
                registro.observacao = request.POST['observacao']
                registro.ordem_servico = request.POST['ordem_de_servico']
                registro.loja = request.POST['num_loja']
                registro.codigo = request.POST['codigo']
                registro.numero_pedido = request.POST['num_pedido']
                registro.custo_site = float(request.POST['custo_site'])
                registro.data_liberacao_blu = request.POST.get('data_lib_blu') or None
                registro.valor_pago = float(request.POST['valor_pago'])
                registro.custo_tabela = float(request.POST['custo_tabela'])
                registro.duplicata = request.POST['duplicata']
                
                registro.save()
                messages.success(request, f"Registro ID {id_edicao} atualizado com sucesso!")
                return redirect('lancamento_de_lentes')
            
            except ComprasLentes.DoesNotExist:
                messages.error(request, f"Registro com ID {id_edicao} não encontrado")
            except Exception as e:
                messages.error(request, f"Erro ao atualizar registro: {str(e)}")
            
            return redirect('lancamento_de_lentes')
        
        try:
            # Converte para dicionário mutável
            post_data = request.POST.dict()

            # Tratamento campos opcionais
            data_lib_blu = post_data.get('data_lib_blu') or None
            
            try:
                # Extrai o ID esperado do post_data (se existir)
                expected_id = post_data.get('id', proximo_id)

                # Tenta criar com o ID esperado
                try:
                    obj = ComprasLentes.objects.create(
                        id=expected_id,
                        descricao_lente=post_data['descricao'],
                        nota_fiscal=post_data['nota_fiscal'],
                        custo_nota_fiscal=float(post_data['custo_nota_fiscal']),
                        data_compra=post_data['data_compra'],
                        sequencial_savwin=post_data['sequencial_prod'],
                        referencia_fabricante=post_data['ref_fabricante'],
                        observacao=post_data['observacao'],
                        ordem_servico=post_data['ordem_de_servico'],
                        loja=post_data['num_loja'],
                        codigo=post_data['codigo'],
                        numero_pedido=post_data['num_pedido'],
                        custo_site=float(post_data['custo_site']),
                        data_liberacao_blu=data_lib_blu,
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
                        descricao_lente=post_data['descricao'],
                        nota_fiscal=post_data['nota_fiscal'],
                        custo_nota_fiscal=float(post_data['custo_nota_fiscal']),
                        data_compra=post_data['data_compra'],
                        sequencial_savwin=post_data['sequencial_prod'],
                        referencia_fabricante=post_data['ref_fabricante'],
                        observacao=post_data['observacao'],
                        ordem_servico=post_data['ordem_de_servico'],
                        loja=post_data['num_loja'],
                        codigo=post_data['codigo'],
                        numero_pedido=post_data['num_pedido'],
                        custo_site=float(post_data['custo_site']),
                        data_liberacao_blu=data_lib_blu,
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
        'ordem servico',
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
                dados = base_queryset.filter(ordem_servico=valor)
            elif identificador == 'loja':
                dados = base_queryset.filter(loja=valor)
            elif identificador == 'data_compra':
                valor = data_para_formato_iso(valor)
                dados = base_queryset.filter(data_compra=valor)
                

    return render(request, 'frontend_site/estoque/listagem_lancamentos.html', {
        'colunas': colunas,
        'dados': dados,
        'filtro_aplicado': filtro_aplicado,
        'identificador': request.GET.get('identificador', ''),
        'valor_identificador': request.GET.get('valor_identificador', '')
    })   