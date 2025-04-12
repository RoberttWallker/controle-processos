function gravarRegistro() {
    const form = document.getElementById('form_lancamento_lentes');
    // Usa a URL base do formulário (já configurada corretamente no HTML)
    form.action = form.action; // Mantém a URL original do formulário
    
    // Remove o campo _method se existir
    const methodInput = document.querySelector('input[name="_method"]');
    if (methodInput) {
        methodInput.remove();
    }
    
    form.submit();
}

function atualizarRegistro() {
    const form = document.getElementById('form_lancamento_lentes');
    const id = document.getElementById('id').value;
    
    form.method = 'POST';
    // Usa a URL base do formulário e adiciona os parâmetros
    form.action = `${form.action}?id=${id}&_method=PUT`;
    
    let methodInput = document.querySelector('input[name="_method"]');
    if (!methodInput) {
        methodInput = document.createElement('input');
        methodInput.type = 'hidden';
        methodInput.name = '_method';
        form.appendChild(methodInput);
    }
    methodInput.value = 'PUT';
    
    form.submit();
}

function preencherFormularioEdicao(registroEdicao) {
    if (!registroEdicao) return;

    // Mapeamento de campos (nome do campo no model -> id no HTML)
    const fieldMap = {
        'id': 'id',
        'descricao_lente': 'descricao_lente',
        'nota_fiscal': 'nota_fiscal',
        'custo_nota_fiscal': 'custo_nota_fiscal',
        'data_compra': 'data_compra',
        'sequencial_savwin': 'sequencial_savwin',
        'referencia_fabricante': 'referencia_fabricante',
        'observacao': 'observacao',
        'ordem_de_servico': 'ordem_de_servico',
        'num_loja': 'num_loja',
        'codigo': 'codigo',
        'num_pedido': 'num_pedido',
        'custo_site': 'custo_site',
        'data_liberacao_blu': 'data_liberacao_blu',
        'valor_pago': 'valor_pago',
        'custo_tabela': 'custo_tabela',
        'duplicata': 'duplicata'
    };

    // Preenche os campos do formulário
    for (const [modelField, formField] of Object.entries(fieldMap)) {
        const element = document.getElementById(formField);
        if (element && registroEdicao[modelField] !== null && registroEdicao[modelField] !== undefined) {
            // Tratamento especial para campos de data
            if (formField.includes('data_')) {
                if (registroEdicao[modelField]) {
                    element.value = registroEdicao[modelField].split('T')[0];
                }
            } else {
                element.value = registroEdicao[modelField];
            }
        }
    }

    // Altera o título para indicar modo de edição
    const headerTitle = document.querySelector('.header-title');
    if (headerTitle) {
        headerTitle.textContent = `Lançamento de Lentes - Editando ID: ${registroEdicao.id}`;
    }
    


    // Configura os botões para modo edição
    const gravarBtn = document.getElementById('botao_gravar');
    const atualizarBtn = document.getElementById('botao_update');
    
    if (gravarBtn) {
        gravarBtn.disabled = true;
        gravarBtn.style.opacity = '0.5';
        gravarBtn.style.cursor = 'not-allowed';
    }
    
    if (atualizarBtn) {
        atualizarBtn.disabled = false;
        atualizarBtn.style.opacity = '1';
        atualizarBtn.style.cursor = 'pointer';
        atualizarBtn.onclick = atualizarRegistro;
    }

    const elementosBloqueados = [
            'id',
            'nota_fiscal',
            'duplicata',
            'num_pedido',
            'data_compra',
            'ordem_de_servico',
            'num_loja',
            'codigo'
        ];

        elementosBloqueados.forEach(campoId => {
        const elemento = document.getElementById(campoId);
        if (elemento) {
            elemento.readOnly = true;
            elemento.style.opacity = '0.7';
            elemento.style.backgroundColor = '#f5f5f5';
            elemento.title = "Este campo não pode ser editado em modo de edição";
        }
    })
    


}

function configurarModoCriacao() {
    const gravarBtn = document.getElementById('botao_gravar');
    const atualizarBtn = document.getElementById('botao_update');
    
    if (gravarBtn) {
        gravarBtn.disabled = false;
        gravarBtn.style.opacity = '1';
        gravarBtn.style.cursor = 'pointer';
        gravarBtn.onclick = gravarRegistro;
    }
    
    if (atualizarBtn) {
        atualizarBtn.disabled = true;
        atualizarBtn.style.opacity = '0.5';
        atualizarBtn.style.cursor = 'not-allowed';
    }
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Configura os handlers dos botões
    document.getElementById('botao_gravar').onclick = gravarRegistro;
    document.getElementById('botao_update').onclick = atualizarRegistro;
    
    // Verifica se há dados de edição
    try {
        const djangoContext = JSON.parse(window.djangoContextData || '{}');
        if (djangoContext.modoEdicao && djangoContext.registroEdicao) {
            preencherFormularioEdicao(djangoContext.registroEdicao);
        } else {
            configurarModoCriacao();
        }
    } catch (e) {
        console.error("Erro ao analisar contexto Django:", e);
        configurarModoCriacao(); // Assume modo criação se houver erro
    }
});