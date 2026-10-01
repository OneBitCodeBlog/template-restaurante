# Casa da Esquina

Site do restaurante, construído a partir do `styleguide.html`, com os dois modelos GLB fornecidos para a apresentação das coxinhas.

## Executar

```sh
npm install
npm run dev -- --port 5173
```

A prévia abre em `http://127.0.0.1:5173/`. Para gerar os arquivos de publicação, execute `npm run build`; o resultado fica em `dist/`.

## Sequência de rolagem

- A seção permanece fixa enquanto o usuário percorre a sequência.
- Entre 0% e 47%, a bandeja gira e se aproxima.
- Entre 47% e 66%, a bandeja desaparece e a coxinha individual surge no mesmo centro visual, com brilho e desfoque suaves.
- Entre 66% e 100%, a coxinha cresce e gira levemente.
- Ao subir, todos os movimentos são revertidos.

A animação está em `src/main.js`; os intervalos `.47` e `.66` controlam a troca dos modelos. As dimensões e a aparência responsiva estão em `src/site.css`. O movimento reduzido do sistema troca os modelos sem a rotação contínua. Uma fotografia substitui a cena se os modelos ou o WebGL falharem.

## Arquivos

- `index.html`: apresentação, pratos filtráveis, ambiente, endereço com mapa e chamada de delivery.
- `src/main.js`: carregamento dos GLBs, luzes e animação pela rolagem.
- `src/site.css`: identidade visual e ajustes para celular.
- `public/models/bandeja-v2.glb`: Meshy_AI_Golden_Teardrop_Bites_0930231834_texture.glb (modelo atual).
- `model-sources/`: originais preservados, incluindo a bandeja anterior; não entram na publicação.
- `public/models/coxinha.glb`: Meshy_AI_Golden_Coxinha_0930223744_texture.glb.
- `styleguide.html`: referência visual atual, preservada.

Os originais são preservados em `model-sources/`; a página usa versões otimizadas. Iluminação difusa levemente quente, material fosco e relevo suave mantêm o acabamento atual. As fotografias dos pratos e da mesa são originais do cardápio; não há foto panorâmica do salão disponível.

Os dois botões de pedido apontam provisoriamente para `https://www.ifood.com.br/`, conforme autorizado para a prévia. Substituir pelo link oficial da loja antes de publicar. As fotografias não recebem o tratamento de cor aplicado ao canvas 3D. O filtro de pratos funciona sem navegar para outra página, e a localização inclui mapa e link para abrir rotas.

## Conversão e experiência

- CTA no cabeçalho, oito links de pedido nos pratos e barra móvel que aparece quando os CTAs de abertura e encerramento estão fora da tela. Todos usam o destino provisório do iFood autorizado para a prévia; os links dos pratos ainda não selecionam itens na plataforma.
- Entradas suaves das fotos respeitam a preferência por movimento reduzido. Filtros continuam disponíveis.
- `public/media/ambiente-ilustrativo.jpg`: imagem de referência de outro restaurante, baixada de https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1600&q=85&fit=crop . Identificada na página como ilustrativa; substituir por foto autorizada do salão real.
- `public/media/mesa-preview.mp4`: demonstração local de seis segundos feita com movimento sobre a foto real da chapa mista. Reprodução opcional, sem áudio, pausada ao sair da tela. Substituir pela filmagem real servindo o prato.
- Depoimentos, estrelas e clientes são fictícios, identificados em cada card e no cabeçalho da seção. Não representam avaliações de clientes. O link do Google leva ao perfil real, não é fonte dos depoimentos de exemplo.


## Otimização dos GLBs

Execute `npm run optimize:models` para reconstruir os dois modelos a partir dos originais. O processo usa [glTF Transform](https://gltf-transform.dev/cli), Meshopt e Sharp, instalados como dependências de desenvolvimento.

| Modelo | Original | Otimizado | Triângulos antes → depois |
|---|---:|---:|---:|
| Bandeja atual | 9.187.416 bytes | 1.748.120 bytes | 88.008 → 44.004 |
| Coxinha individual | 12.502.828 bytes | 2.189.836 bytes | 189.914 → 94.956 |

Total: 21.690.244 → 3.937.956 bytes, redução de 81,84%. Texturas de cor em WebP 2048×2048 (qualidade 88); normais em WebP sem perdas na resolução final de 1024×1024. Simplificação limitada a erro de 0,05% do raio e compressão/quantização Meshopt. O mapa de metal/rugosidade removido já não participava do acabamento renderizado. O decoder Meshopt é empacotado localmente com o site, sem CDN.

O relatório está em `pesquisa/model-optimization.json`. Os outputs foram relidos pelo decoder e conferidos na página, incluindo os dois estados da rolagem. O modelo antigo saiu de `public/` para evitar incluí-lo no build. Redução de bytes não representa uma medição de tempo de carregamento em rede móvel.
