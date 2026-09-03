# Eye Tracker

Projeto de iniciação ao rastreamento do olhar usando a webcam do computador. A aplicação identifica a posição da íris e estima para qual direção a pessoa está olhando.

O objetivo principal é apoiar testes de usabilidade, ajudando a observar se uma pessoa está olhando para uma determinada região da tela durante a utilização de uma interface.

## Objetivos

- Detectar um rosto pela webcam.
- Identificar os pontos principais do rosto e das íris.
- Estimar se o olhar está para a esquerda, direita, cima, baixo ou centro.
- Servir como base para futuros testes de usabilidade e análise de atenção visual.

## Como funciona

O programa captura imagens da webcam usando OpenCV. Cada frame é analisado pelo MediaPipe Face Landmarker, que identifica os landmarks do rosto e das íris.

A posição da íris é comparada com os cantos dos olhos. Com essa comparação, o programa calcula uma direção aproximada e mostra o resultado na janela da câmera.

Além da direção, a janela mostra um painel que representa a tela. O ponto vermelho indica a posição estimada do olhar, e os valores `X` e `Y` mostram uma coordenada baseada em uma tela de referência de `1920x1080`.

As direções exibidas são:

- `esquerda`
- `direita`
- `cima`
- `baixo`
- `centro`

## Requisitos

- Python 3.14 ou superior.
- Uma webcam funcionando.
- Conexão com a internet na primeira execução, para baixar o modelo do MediaPipe.
- Linux, Windows ou macOS com suporte ao OpenCV.

## Instalação

Este projeto usa o [uv](https://docs.astral.sh/uv/) para gerenciar o ambiente e as dependências.

Depois de clonar o projeto, execute:

```bash
uv venv
source .venv/bin/activate
uv sync
```

## Execução

Inicie o programa com:

```bash
uv run src/main.py
```

Na primeira execução, o modelo `face_landmarker.task` será baixado automaticamente e salvo na pasta `models`.

Para fechar a janela e encerrar o programa, pressione a tecla `Esc`.

## Estrutura do projeto

```text
eye-tracker/
├── models/
│   └── face_landmarker.task
├── src/
│   ├── main.py
│   ├── cam.py
│   ├── face.py
│   ├── eyes.py
│   ├── gaze.py
│   └── calibration.py
├── pyproject.toml
└── README.md
```

Cada arquivo possui uma responsabilidade diferente:

- `main.py`: executa o fluxo principal do programa.
- `cam.py`: abre a webcam, captura os frames e encerra a câmera.
- `face.py`: baixa o modelo e detecta os landmarks do rosto.
- `eyes.py`: trabalha com os pontos dos olhos e calcula o centro das íris.
- `gaze.py`: compara as posições dos olhos e calcula a direção do olhar.
- `calibration.py`: define a classificação das direções do olhar.

## Limitações atuais

Este projeto fornece uma estimativa simples da direção e da posição do olhar. O painel de coordenadas ainda não representa com precisão o ponto real da tela, pois precisa de uma etapa de calibração individual para cada pessoa e cada webcam.

Os resultados podem variar de acordo com a iluminação, a posição da webcam, a distância do rosto e a qualidade da câmera.
