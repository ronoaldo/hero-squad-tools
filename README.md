# Hero Squad Tools

Esse é um repositório de exemplos de como utilizar as ferramentas
Image Magick e Tesseract OCR para processamento de imagens
utilizando scripts. Além disso, é um exemplo de como interagir
com dispositivos Android por meio do `monkeyrunner`, automatizando
tarefas repetitivas via depuração USB.

Os scripts `squaddump.py` e `squadparse.sh` servem para extrair informações
do game Star Wars Galaxy of Heroes e montar uma planilha,
que pode ser útil para identificar dados de seus personagens no jogo
de uma forma bem simples.
Essas informações podem lhe ajudar a tomar decisões sobre quais heróis evoluir,
ou quais ativar mais rapidamente.

## Como fazer

*Disclaimer: utilize este script por sua conta e risco! Eu testei
apenas para o meu aparelho, com resolução 1920x1080.
O monkeyrunner vai enviar eventos de touch para seu aparelho,
e isso pode ter efeitos colaterais caso a tela de outra aplicação
"entre na frente" do jogo! Além disso, se a imagem não tiver exatamente
o mesmo tamanho, o OCR não vai funcionar. Pode ser necessário ajustar
alguns dos inúmeros números mágicos do script para isso.*

Você vai precisar de um comptuador com Linux instalado,
da SDK do Android em seu `$PATH` e dos pacotes a seguir:

	sudo apt-get install tesseract-ocr imagemagick

Em seguida, ative as ferramentas de desenvolvedor e a depuração USB
em seu dispositivo Android. Depois de conectar o dispositivo, abra o jogo,
e tenha certeza que ele está na tela inicial.

Primeiro, execute o script `squaddump.py` via Monkey Runner:

	monkeyrunner squaddump.py

No começo, o script vai conectar ao seu dispositivo, e em seguida,
vai tirar um print da página inicial do jogo. Neste ponto é importante
ter certeza que o game está na tela principal!
Depois de tirar o print inicial, o script mostra a tela pra você e
aguarda que você a feche para começar o "dump" do seu esquadrão.

Depois que você fechar a janela do print, o script vai controlar o seu Android
via `adb`, e tirar print-screen de várias telas do aparelho ao navegar pela
lista de personagens. O processo demora um pouco.

Depois disso, vai ficar tudo na pasta /tmp, várias imagens que você pode
inclusive dar uma conferida.

Para gerar o arquivo CSV a partir das imagens via OCR, utilize o `squadparse.sh`:

	squadparse.sh > /tmp/myherosquad.csv

Esse script vai fazer o OCR de áreas específicas da imagem para tentar extrair
a informação. Além do nome do personagem, do valor do poder, quantidade de
estrelas, fragmentos obtidos e fragmentos necessários para ativar/processar
e o nível do equipamento.
