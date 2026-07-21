// Capturamos os elementos da tela
const form = document.getElementById('form-dragao');
const inputImagem = document.getElementById('imagem-input');
const containerResultado = document.getElementById('resultado-container');
const previewImagem = document.getElementById('preview-imagem');
const textoResultado = document.getElementById('texto-resultado');
const botaoSubmit = document.querySelector('button[type="submit"]');

// Capturamos o container principal para fazer ele tremer
const containerPrincipal = document.querySelector('.container');

form.addEventListener('submit', async (evento) => {
    evento.preventDefault(); 

    const arquivo = inputImagem.files[0];
    if (!arquivo) return;

    // --- MUDANÇA DE ESTADO: CARREGANDO ---
    // 1. Desativa o botão para o usuário não clicar duas vezes
    botaoSubmit.disabled = true;
    botaoSubmit.innerText = 'Consultando...';
    
    // 2. Inicia o tremor na tela
    containerPrincipal.classList.add('tremer');
    
    // 3. Prepara a prévia, mas remove animações antigas para resetar
    previewImagem.classList.remove('surgir');
    textoResultado.classList.remove('surgir');
    
    previewImagem.src = URL.createObjectURL(arquivo);
    containerResultado.style.display = 'block';
    textoResultado.innerText = 'Folheando os antigos registros...';
    textoResultado.style.color = '#3e2723';

    const formData = new FormData();
    formData.append('file', arquivo);

    try {
        // Envia para o servidor
        const resposta = await fetch('http://127.0.0.1:8000/identificar', {
            method: 'POST',
            body: formData
        });

        const dados = await resposta.json();

        // --- MUDANÇA DE ESTADO: FINALIZADO ---
        // 1. Para o tremor e aplica o surgimento suave
        containerPrincipal.classList.remove('tremer');
        previewImagem.classList.add('surgir');
        textoResultado.classList.add('surgir');

        if (dados.sucesso) {
            textoResultado.innerText = `Espécie detectada: ${dados.raca}!`;
            textoResultado.style.color = '#27ae60'; // Verde estilo poção
        } else {
            textoResultado.innerText = 'As runas estão confusas. Tente novamente.';
            textoResultado.style.color = '#c0392b'; // Vermelho sangue
        }

    } catch (erro) {
        console.error(erro);
        containerPrincipal.classList.remove('tremer');
        textoResultado.innerText = 'A conexão com Berk foi perdida.';
    } finally {
        // Devolve o botão ao estado normal independente de sucesso ou erro
        botaoSubmit.disabled = false;
        botaoSubmit.innerText = 'Identificar Espécie';
    }

    
});

document.addEventListener("DOMContentLoaded", () => {
    
    // Captura os elementos
    const musica = document.getElementById("musicaFundo");
    const btnMusica = document.getElementById("btnMusica");
    const sliderVolume = document.getElementById("volumeMusica");
    const telaEntrada = document.getElementById("telaEntrada");
    const btnEntrar = document.getElementById("btnEntrar");

    // ==========================================
    // 1. LÓGICA DA TELA DE ENTRADA (Independente)
    // ==========================================
    if (btnEntrar && telaEntrada) {
        btnEntrar.addEventListener("click", () => {
            // 1. Faz a tela sumir suavemente
            telaEntrada.style.opacity = "0";
            
            // 2. Tenta tocar a música se ela existir
            if (musica) {
                // O .catch captura qualquer erro do navegador para não quebrar o site
                musica.play().catch(erro => console.log("Aviso de áudio:", erro));
                if (btnMusica) btnMusica.textContent = "⏸️ Pausar Música";
            }

            // 3. Remove a tela de entrada do caminho após 1 segundo
            setTimeout(() => {
                telaEntrada.style.display = "none";
            }, 1000);
        });
    }

    // ==========================================
    // 2. LÓGICA DO BOTÃO DE PAUSAR/TOCAR
    // ==========================================
    if (btnMusica && musica) {
        btnMusica.addEventListener("click", () => {
            if (musica.paused) {
                musica.play();
                btnMusica.textContent = "⏸️ Pausar Música";
            } else {
                musica.pause();
                btnMusica.textContent = "🔊 Tocar Música";
            }
        });
    }

    // ==========================================
    // 3. LÓGICA DO SLIDER DE VOLUME
    // ==========================================
    if (sliderVolume && musica) {
        musica.volume = sliderVolume.value;
        
        sliderVolume.addEventListener("input", (evento) => {
            musica.volume = evento.target.value;
        });
    }
});