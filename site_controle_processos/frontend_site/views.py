from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ComprasLentes
from .aux_function import data_para_formato_iso

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
    if request.method == 'POST':
        try:
            # Converte para dicionário mutável
            post_data = request.POST.dict()

            # Tratamento campos opcionais
            data_lib_blu = post_data.get('data_lib_blu') or None
            
            # Criação direta sem variáveis intermediárias
            ComprasLentes.objects.create(
                descricao_lente=post_data['descricao'],
                nota_fiscal=post_data['nota_fiscal'],
                custo_nota_fiscal=float(post_data['valor_custo']),
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

            messages.success(request, "Entrada efetuada com sucesso.")
            return redirect('lancamento_de_lentes')
        
        except KeyError as e:
            messages.error(request, f"Campo obrigatório faltando: {e}")
        except ValueError as e:
            messages.error(request, f"Valor numérico inválido: {e}")
        except Exception as e:
            messages.error(request, f"Erro ao salvar: {str(e)}")

    return render(request, 'frontend_site/estoque/lancamento_de_lentes.html')

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