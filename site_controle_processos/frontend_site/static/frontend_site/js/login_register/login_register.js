function esconderListaDeMensagens(lista_mensagens) {
    setTimeout(function() {
        if (lista_mensagens) {
            lista_mensagens.style.display = 'none';
        }
    }, 2000);
}

// Função para redirecionar após 2 segundos
function redirecionarParaLogin(url) {
    setTimeout(function() {
        window.location.href = url;
    }, 2000);
}

document.addEventListener('DOMContentLoaded', function() {
    const listaMensagens = document.querySelector('.lista_mensagens');
    
    if (listaMensagens) {
        // Verifica cada mensagem
        const mensagens = listaMensagens.querySelectorAll('.message');
        let shouldRedirect = false; // Inicia variável de controle para redirecionamento
        let shouldHide = false; // Inicia variável de controle para esconder elemento

        mensagens.forEach(msg => {
            if (msg.classList.contains('success')) {
                if (msg.textContent.trim() === 'Senha validada!') {
                    shouldHide = true;
                } else {
                    shouldRedirect = true;
                }
            }
        });

        // Executa as ações
        if (shouldRedirect) {
            const redirectUrl = listaMensagens.getAttribute('data-redirect-url');
            redirecionarParaLogin(redirectUrl);
        } else if (shouldHide) {
            esconderListaDeMensagens(listaMensagens);
        }
    }
});