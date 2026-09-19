# quelve — pacote inicial do aplicativo

Este pacote contém a primeira versão de testes do quelve e a estrutura para transformá-lo em um aplicativo instalável (PWA) para Android e iPhone.

## Já incluído
- Campo de pergunta por teclado.
- Botão Enviar com explicação de demonstração.
- Contador de respostas.
- Oferta após cada 5 perguntas.
- Premium de R$ 1/mês sem novas ofertas após ativação de demonstração.
- Câmera com captura de imagem.
- Microfone com transcrição pelo navegador.
- Manifesto de aplicativo e service worker para instalação como PWA.

## Para virar a versão final
A hospedagem precisa servir o projeto por HTTPS e conectar:
- Um serviço de IA para respostas reais.
- OCR para interpretar fotos.
- Banco seguro para conta, histórico e contador.
- Pagamento recorrente de R$ 1/mês.
- Fluxos de consentimento e privacidade para menores.

O arquivo HTML sozinho funciona como demonstração, mas não substitui a publicação em uma hospedagem compatível com PWA.

## Publicação
O pacote já inclui `Dockerfile` e `START.txt`. Publique os arquivos em uma hospedagem HTTPS que execute Python e configure `GEMINI_API_KEY` como segredo da hospedagem. Nunca coloque a chave dentro do HTML. Depois, no celular, use “Adicionar à tela inicial” para instalar o quelve como aplicativo.
