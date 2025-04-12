// 1. Função para manipular o botão pesquisar
function handlePesquisarClick() {
    document.getElementById('form_filtro_lancamentos')?.submit();
}

// 2. Função para manipular o duplo clique na linha
function handleRowDoubleClick() {
    // Obtém apenas o ID do lançamento do atributo data-id da linha
    const lancamentoId = this.getAttribute('data-id');
    
    // Redireciona para a página de lançamentos com o ID como parâmetro
    window.location.href = `/lancamento-de-lentes/?id=${lancamentoId}&edit=true`;
}

function handleOpcaoLinha(event) {
    const selectElement = event.target;
    const selectedValue = selectElement.value;
    const lancamentoId = selectElement.closest('tr').getAttribute('data-id');

    if (selectedValue == 'editar') {
        // Redireciona para a página de lançamentos com o ID como parâmetro
        window.location.href = `/lancamento-de-lentes/?id=${lancamentoId}&edit=true`;        
    } else if (selectedValue == 'excluir') {
        if(confirm(`Deseja realmente excluir o lançamento ${lancamentoId}?`)) {
            fetch(`/excluir-lancamento-de-lentes/?id=${lancamentoId}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    selectElement.closest('tr').remove();
                    alert('Sucesso: ' + data.message)
                } else {
                    alert('Erro ao excluir: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro na requisição');
            });
        }
    } else {
        selectElement.value = '';
    }
}

// 3. Função para configurar os listeners de eventos
function setupEventListeners() {
    // Botão Pesquisar
    const botaoPesquisar = document.getElementById('botao_pesquisar');
    if (botaoPesquisar) {
        botaoPesquisar.addEventListener('click', handlePesquisarClick);
    }

    // Linhas da tabela
    const linhasTabela = document.querySelectorAll('#tabela_lancamentos tbody tr');
    linhasTabela.forEach(linha => {
        linha.addEventListener('dblclick', handleRowDoubleClick);
    });

    const opcaoLinhaTabela = document.querySelectorAll('#tabela_lancamentos tbody select[name="opcoes_linha"]');
    opcaoLinhaTabela.forEach(select => {
        select.addEventListener('change', handleOpcaoLinha);
    });

}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', setupEventListeners);