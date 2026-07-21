# 🐉 DragonDex - O Livro dos Dragões com Visão Computacional

Um sistema inteligente *end-to-end* de classificação de imagens capaz de identificar espécies de dragões do universo de "Como Treinar o Seu Dragão". O projeto une Inteligência Artificial avançada, uma API de alta performance e uma interface web temática com imersão sonora.

## 🚀 Tecnologias Utilizadas

**Inteligência Artificial & Dados:**
* **PyTorch & Torchvision:** Construção, *Fine-Tuning* completo e execução de redes neurais.
* **ResNet18:** Arquitetura base de Redes Neurais Convolucionais (CNN) utilizada via *Transfer Learning*.
* **Data Augmentation & Normalização:** Tratamento de imagens para otimização da acurácia e generalização.

**Back-end & API:**
* **FastAPI:** Criação de uma API assíncrona e dinâmica para receber as imagens, calcular as probabilidades de inferência e retornar os resultados em JSON.
* **Uvicorn:** Servidor ASGI para execução do servidor local.

**Front-end & UX:**
* **HTML5, CSS3 & JavaScript Vanilla:** Interface responsiva customizada em formato de pergaminho antigo.
* **Web Audio API:** Sistema interativo de trilha sonora em loop com controle de volume e tela de entrada (*Splash Screen*).

## 🧠 Arquitetura do Modelo
O classificador foi treinado para reconhecer dinamicamente as raças suportadas, processando a entrada do usuário através de padronização geométrica (*CenterCrop* e tensores normalizados) antes de passá-la pela matriz de decisão.

### Raças Mapeadas Atualmente:
1. Fúria da Noite 
2. Gronckle
3. Nadder Mortal 
4. Pesadelo Monstruoso 

---

## ⚙️ Como Executar o Projeto Localmente

### 1. Clonar o Repositório e Configurar o Ambiente
Certifique-se de ter o Python instalado. No terminal, execute:
```bash
git clone [https://github.com/Rumuca/DragonDex.git](https://github.com/Rumuca/DragonDex.git)
cd dragondex
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install torch torchvision fastapi uvicorn python-multipart Pillow