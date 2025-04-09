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
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', setupEventListeners);