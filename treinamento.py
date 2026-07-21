import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from torch import nn
import torch.optim as optim
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Preparando os dragões usando: {device}")

# ================================
# 1. A TUBULAÇÃO (Data Augmentation)
# ================================
padronizacao_imagem = transforms.Compose([
    transforms.Resize((236, 236)),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
])

caminho_dataset = "dataset_dragoes"

# ================================
# 2. MAPEANDO O DATASET PRIMEIRO
# ================================
dataset_completo = datasets.ImageFolder(root=caminho_dataset, transform=padronizacao_imagem)
racas_encontradas = dataset_completo.classes
numero_de_racas = len(racas_encontradas)
print(f"Raças detectadas ({numero_de_racas}): {racas_encontradas}")

# ================================
# 3. PREPARANDO O MODELO
# ================================
print("Baixando o cérebro base...")
modelo = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

numero_de_features = modelo.fc.in_features

# Aqui a mágica acontece: o modelo se adapta sozinho à quantidade de pastas!
modelo.fc = nn.Linear(numero_de_features, numero_de_racas)
modelo = modelo.to(device)

print("Modelo adaptado e pronto para aprender!")

# ================================
# 4. DIVISÃO E TREINAMENTO
# ================================
tamanho_total = len(dataset_completo)
tamanho_treino = int(0.8 * tamanho_total)
tamanho_validacao = tamanho_total - tamanho_treino

dataset_treino, dataset_validacao = random_split(
    dataset_completo, 
    [tamanho_treino, tamanho_validacao]
)

loader_treino = DataLoader(dataset_treino, batch_size=32, shuffle=True)
loader_validacao = DataLoader(dataset_validacao, batch_size=32, shuffle=False)

# Fine-Tuning ativo com Taxa de Aprendizado ajustada
criterio = nn.CrossEntropyLoss()
otimizador = optim.Adam(modelo.parameters(), lr=0.0001)

numero_de_epocas = 30

print("Iniciando o treinamento dos dragões...")

for epoca in range(numero_de_epocas):
    
    # FASE DE TREINAMENTO
    modelo.train() 
    acertos_treino = 0
    total_treino = 0
    
    for imagens, rotulos_corretos in loader_treino:
        imagens = imagens.to(device)
        rotulos_corretos = rotulos_corretos.to(device)
        
        otimizador.zero_grad()
        previsoes = modelo(imagens)
        perda = criterio(previsoes, rotulos_corretos)
        
        perda.backward()
        otimizador.step()
        
        _, chute_final = torch.max(previsoes, 1)
        acertos_treino += (chute_final == rotulos_corretos).sum().item()
        total_treino += rotulos_corretos.size(0)

    acuracia_treino = acertos_treino / total_treino
    
    # FASE DE VALIDAÇÃO
    modelo.eval() 
    acertos_validacao = 0
    total_validacao = 0
    
    with torch.no_grad():
        for imagens, rotulos_corretos in loader_validacao:
            imagens = imagens.to(device)
            rotulos_corretos = rotulos_corretos.to(device)
            
            previsoes = modelo(imagens)
            _, chute_final = torch.max(previsoes, 1)
            
            acertos_validacao += (chute_final == rotulos_corretos).sum().item()
            total_validacao += rotulos_corretos.size(0)
            
    acuracia_validacao = acertos_validacao / total_validacao
    
    print(f"Época [{epoca+1}/{numero_de_epocas}] | "
          f"Acc Treino: {acuracia_treino*100:.2f}% | "
          f"Acc Validação: {acuracia_validacao*100:.2f}%")

torch.save(modelo.state_dict(), "modelo_dragoes.pth")
print("\nTreinamento blindado concluído e modelo salvo!")