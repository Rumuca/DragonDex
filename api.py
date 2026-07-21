import torch
import torch.nn.functional as F
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from torchvision import models, transforms
from PIL import Image
import io

app = FastAPI(title="DragonDex API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cpu")

# ==========================================
# 1. A LISTA DE RAÇAS (ATENÇÃO AQUI)
# ==========================================
# Substitua esta lista pela ordem EXATA que o terminal imprimiu no treinamento.
# Exemplo (se você adicionou o Gronckle e ele ficou na letra G):
racas = ['Fúria da Noite', 'Gronckle', 'Nadder Mortal', 'Pesadelo Monstruoso']

# O código agora conta as raças sozinho para não quebrar mais!
numero_de_racas = len(racas)

# ==========================================
# 2. CARREGANDO O CÉREBRO
# ==========================================
modelo = models.resnet18(weights=None)
numero_de_features = modelo.fc.in_features

# Adaptamos a saída do cérebro dinamicamente
modelo.fc = torch.nn.Linear(numero_de_features, numero_de_racas) 

modelo.load_state_dict(torch.load("modelo_dragoes.pth", map_location=device))
modelo.eval()

padronizacao_imagem = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ==========================================
# 3. ROTAS DA API
# ==========================================
@app.get("/")
def rota_principal():
    return {"mensagem": "A DragonDex API está online!"}

@app.post("/identificar")
async def identificar_dragao(file: UploadFile = File(...)):
    try:
        imagem_bytes = await file.read()
        imagem = Image.open(io.BytesIO(imagem_bytes)).convert("RGB")
        
        imagem_tensor = padronizacao_imagem(imagem).unsqueeze(0).to(device)
        
        with torch.no_grad():
            previsoes = modelo(imagem_tensor)
            probabilidades = F.softmax(previsoes, dim=1)[0] * 100
            
            # --- O NOVO RAIO-X INTELIGENTE ---
            print("\n--- RAIO-X DA IA ---")
            # O laço 'for' passa por todos os dragões da sua lista automaticamente
            for i, raca in enumerate(racas):
                # O .ljust(20) apenas alinha o texto para a tabela ficar bonita no terminal
                print(f"{raca.ljust(20)}: {probabilidades[i]:.2f}%")
            print("--------------------\n")
            
            _, indice = torch.max(previsoes, 1)
            
        raca_identificada = racas[indice.item()]
        
        return {"sucesso": True, "raca": raca_identificada}

    except Exception as e:
        return {"sucesso": False, "erro": str(e)}