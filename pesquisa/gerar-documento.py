import csv, json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
acu=json.loads((ROOT/'pesquisa/fontes/acuolina-dados.json').read_text())['data'][0]['menu']['sections']
with (ROOT/'pesquisa/fontes/pedyun-cardapio.tsv').open() as f: rows=list(csv.DictReader(f,delimiter='\t'))
imgs=json.loads((ROOT/'pesquisa/inventario-imagens.json').read_text())
for im in imgs:
    out=subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',str(ROOT/im['arquivo'])],capture_output=True,text=True,check=True).stdout
    im['largura']=int(re.search(r'pixelWidth: (\d+)',out).group(1));im['altura']=int(re.search(r'pixelHeight: (\d+)',out).group(1))
(ROOT/'pesquisa/inventario-imagens.json').write_text(json.dumps(imgs,ensure_ascii=False,indent=2))
def money(v):return 'R$ '+f'{float(v):.2f}'.replace('.',',')
text='''# Casa da Esquina — levantamento para o rebranding e novo site

Pesquisa realizada em **30 de setembro de 2026**, com base no cardápio Acuolina, na página de pedidos PedyUN e no perfil público do Instagram. Este documento reúne a oferta gastronômica, os dados de contato, a identidade atual e os materiais disponíveis para a criação do novo site. Os preços representam o que cada canal mostrava no momento da consulta; as divergências foram preservadas.

## 1. O que é a Casa da Esquina

A **Casa da Esquina** é um estabelecimento gastronômico em **Janaúba, Minas Gerais**, com endereço no Centro da cidade. A oferta reúne petiscos e porções para compartilhar, hambúrgueres, carnes e peixes grelhados, caldos, salada, acompanhamentos, sobremesas e bebidas. O cardápio combina preparações como carne de sol, mandioca, cupim e torresmo com bruschetta, carpaccio, molho chimichurri e arroz piamontese. [Fontes: Acuolina e PedyUN](#9-fontes-e-limites-da-pesquisa).

O nome apresentado no Instagram e no Acuolina é **Casa da Esquina**. O logo usa **Espaço Casa da Esquina Gourmet**. A página de pedidos exibe a variante “CASA DE ESQUINA”, enquanto seu título é “Espaço Casa Da Esquina - Gourmet”. Essa variação de nome precisa ser padronizada na nova identidade.

**Leitura de posicionamento para o projeto, não uma declaração oficial:** a variedade de porções, grelhados, cervejas e a comunicação de funcionamento noturno sugerem um restaurante com proposta de encontro e convivência, além do delivery. Não há evidência suficiente nas páginas acessíveis para afirmar capacidade do salão, serviço de reservas ou características físicas do ambiente.

## 2. Endereço, atendimento e canais

| Informação | Dado observado | Fonte |
|---|---|---|
| Cidade | Janaúba, MG | Acuolina e PedyUN |
| Endereço | Rua Rui Barbosa, 107 — Centro, Janaúba | Acuolina e bio do Instagram |
| Telefone / WhatsApp anunciado | (38) 99944-5000 | Acuolina e bio do Instagram |
| E-mail cadastrado | casaesquinagourmet@gmail.com | Dados públicos da página Acuolina; confirmar antes de publicar |
| Horário anunciado | Terça a domingo, 18h30 às 00h | Bio pública do Instagram |
| Instagram | [@casadaesquinajba](https://www.instagram.com/casadaesquinajba/) | Perfil informado |
| Pedidos online | [PedyUN](https://pedyun.com.br/casadaesquina) | Página de pedidos e link da bio |
| Cardápio digital | [Acuolina](https://acuolina.com/pt/casa-da-esquina/62f81d41237340002367940c) | Cardápio informado |
| Prazo exibido para delivery | 60–120 minutos | PedyUN; indicador dinâmico, não prazo garantido |

O Acuolina contém configuração pública de horários iniciando às 18h e encerrando às 23h ou 00h, dependendo da entrada. Isso difere da bio do Instagram. Para o novo site, validar com o restaurante qual é o horário oficial e se salão e delivery têm horários distintos. A segunda-feira não aparece no intervalo anunciado pela bio; não foi confirmada uma política para feriados.

O perfil do Instagram anuncia o WhatsApp na bio. Um link que pode ser construído a partir do número confirmado é [wa.me/5538999445000](https://wa.me/5538999445000); esta URL é derivada do telefone, não foi testada com envio de mensagem.

## 3. Oferta gastronômica e pratos que ajudam a explicar a casa

| Linha | O que oferece | Exemplos observados |
|---|---|---|
| Petiscos e porções | Entradas, frituras, carnes e combinações para compartilhar | Coxinha de cupim, croquete de costela, dadinho de tapioca, chapa mista, torre de fritas |
| Hambúrgueres | Sanduíches com pão brioche, diferentes carnes e maionese da casa | Burger da Casa, Cheese Bacon, Mexicano, Supremo, La Casa Turbo |
| Grelhados | Bovinos, frango e tilápia com acompanhamentos e molhos | Maminha ao provolone, picanha, cupim rústico, tilápia ao molho de maracujá |
| Caldos | Carne, frango e feijão | Torrada, torresmo e cheiro-verde aparecem nos acompanhamentos |
| Salada | Caesar com frango | Alface, parmesão, croutons e molho Caesar |
| Sobremesas | Chocolate, sorvete e cheesecake | Brownie com sorvete, sorvete da casa com Oreo, cheesecake |
| Bebidas | Refrigerantes, águas, energético, sucos e cervejas | Maracujá, morango, Heineken, Stella Artois, Corona |

O PedyUN lista um hambúrguer **Vegetariano**, de soja e com queijos. A descrição não o caracteriza como vegano. O destaque **Kids** existe no Instagram, e o cardápio apresenta o sanduíche Junior; isso não confirma a existência de espaço infantil. O destaque **Drinks** indica essa frente na comunicação, mas receitas e preços de coquetéis não ficaram disponíveis nas páginas consultadas.

Não foi possível estabelecer quais itens são os mais vendidos, premiados ou “carro-chefe”. Os exemplos acima descrevem a oferta, sem atribuir popularidade não demonstrada.

## 4. Cardápio completo observado no PedyUN

Fonte desta seção: [página de pedidos](https://pedyun.com.br/casadaesquina), consultada em 30/09/2026. Nomes e descrições tiveram ajustes de ortografia para leitura, preservando ingredientes, porções e valores. “Não informada” significa ausência de descrição no canal. As categorias seguem a organização da plataforma, inclusive a mini porção de batata em Hambúrgueres. Há **81 itens** listados, incluindo bebidas, acompanhamentos e meias porções; isso não equivale a 81 pratos diferentes.
'''
for cat in dict.fromkeys(r['Categoria'] for r in rows):
    text+=f'\n### {cat}\n\n| Produto | Descrição / composição | Preço observado |\n|---|---|---|\n'
    for r in rows:
        if r['Categoria']==cat:text+=f"| {r['Produto']} | {r['Descrição'] or 'Não informada'} | {money(r['Preço'])} |\n"
text+='''
## 5. Diferenças entre os cardápios

Os canais não têm exatamente a mesma seleção, preços ou descrições. O Acuolina também apresenta **Filé aperitivo (R$ 78,00)** e **Provoleta (R$ 34,00)**, que não aparecem na listagem PedyUN consultada. O PedyUN acrescenta, entre outros, hambúrguer Vegetariano, mini porção de batata, alcatra com fritas, arroz ao alho e bebidas. A picanha é marcada “sob consulta” no Acuolina.

### Divergências de preço observadas

| Produto ou preparação equivalente | Acuolina | PedyUN |
|---|---|---|
| Bolinho de mandioca | R$ 22,00 | R$ 26,00 |
| Croquete de costela | R$ 34,00 | R$ 38,00 |
| Dadinho de tapioca | R$ 16,00 | R$ 19,00 |
| Panceta | R$ 29,00 | R$ 34,00 |
| Carne de sol com mandioca | R$ 64,00 | R$ 72,00 |
| Meia porção de carne de sol com mandioca | R$ 42,00 | R$ 49,00 |
| Chapa mista | R$ 64,00 | R$ 72,00 |
| Meia porção de chapa mista | R$ 42,00 | R$ 49,00 |
| Tiras de frango crocante | R$ 39,00 | R$ 44,00 |
| Salada Caesar | R$ 26,00 | R$ 29,00 |
| Maminha ao provolone | R$ 84,00 | R$ 88,00 |
| Contra filé / contra filé ao molho três queijos | R$ 78,00 | R$ 82,00 |
| Alcatra / alcatra mineira | R$ 80,00 | R$ 84,00 |
| Cupim / cupim rústico | R$ 68,00 | R$ 72,00 |

Os dois últimos pares têm nomes diferentes e foram aproximados para comparação; validar se são a mesma preparação. Não é possível concluir se as diferenças resultam de atualização, modalidade de serviço ou outra política comercial.

### Divergências de descrição que precisam de validação

- **Carpaccio:** pão sírio no Acuolina; torradas no PedyUN.
- **Coxinha da casa:** molho de azeitonas no Acuolina; maionese da casa no PedyUN.
- **Croquete de costela:** molho especial e 6 unidades no Acuolina; molho de azeitonas e molho do chef no PedyUN, sem quantidade informada.
- **Mexicano:** molho agridoce picante no Acuolina; geleia de pimenta no PedyUN.
- **La Casa Turbo:** tomate aparece no PedyUN e não na descrição Acuolina.
- **Picanha:** mini batatas rústicas, vinagrete e farofa no Acuolina; batata rústica, chimichurri, vinagrete e farofa no PedyUN.
- **Torre de fritas:** o Acuolina informa acréscimo de cheddar por R$ 8,00; esse acréscimo não consta na descrição PedyUN consultada.
- **Pastel de carne:** o Acuolina especifica carne de sol; o PedyUN usa “carne”.

### Registro completo do Acuolina

Fonte: [Acuolina](https://acuolina.com/pt/casa-da-esquina/62f81d41237340002367940c). Além do texto inicial, foram lidos os dados de cardápio enviados publicamente pela própria página, incluindo itens das categorias recolhidas. Abaixo estão os **51 itens** cadastrados nesse cardápio; a presença no cadastro não confirma estoque ou disponibilidade no dia.
'''
for sec in acu:
    text+=f"\n#### {sec['name']}\n\n| Produto | Descrição no Acuolina | Preço observado |\n|---|---|---|\n"
    for d in sec['dishes']:
        desc=(d.get('description') or 'Não informada').replace('\n',' ').replace('|','/')
        text+=f"| {d['name'].strip()} | {desc} | {money(d['salePrice'])} |\n"
text+='''
## 6. Identidade visual atual e comunicação

O logo baixado do Acuolina é um selo circular com fundo dourado/mostarda, contorno marrom e lettering branco. “Casa da Esquina” ocupa o centro, com escrita expressiva e inclinada; “Espaço” e “Gourmet” aparecem ao redor. Há formas decorativas em tom dourado mais escuro atrás do nome. A observação é visual, baseada no arquivo original baixado.

![Logo atual da Casa da Esquina](assets/logo/casa-da-esquina-acuolina.jpeg)

O Acuolina usa a cor **#BD7F22** na configuração pública da interface. Ela é uma referência da presença digital atual, não um manual de marca. Não foram encontrados arquivos vetoriais, fontes tipográficas oficiais ou orientações de aplicação do logo.

Na bio do Instagram, a comunicação é direta e informal, voltada a horário, localização e contato para pedidos. Os destaques visíveis são **Drinks, Grelhados, Petiscos, Burguer, Kids, Caldos, Sobremesas, Halloween, Carna 2025 e Saladas**. Os nomes dos destaques mostram temas da comunicação; não comprovam, por si só, serviços, instalações ou uma programação atual de eventos.

## 7. Banco de imagens baixado

Foram salvos **52 arquivos JPEG: 50 imagens de produtos e 2 arquivos de logo**, provenientes do Acuolina e do PedyUN. Há pratos representados nos dois canais; portanto, a quantidade de arquivos não corresponde à quantidade de produtos distintos. Os logos também podem representar a mesma arte em versões ou tamanhos diferentes.

- [Pasta de logos](assets/logo/): duas versões de origem, sem redesenho.
- [Pasta de produtos](assets/produtos/): imagens com nomes descritivos e identificação do canal.
- [Inventário de imagens](pesquisa/INVENTARIO-IMAGENS.md): relação de cada arquivo com prato e URL de origem.
- [Inventário estruturado](pesquisa/inventario-imagens.json): origem, tamanho em bytes, dimensões e hash de cada arquivo.

As imagens do Acuolina foram baixadas na versão de maior resolução encontrada, em vez das miniaturas da tela inicial. Todas as imagens foram reconhecidas como JPEG e tiveram as dimensões verificadas. Os arquivos foram preservados sem recortes, compressão adicional ou criação de transparência. Não foram obtidas fotos verificadas do salão, fachada ou equipe, nem o histórico completo de mídia do Instagram.

## 8. Base para o rebranding e conteúdo do novo site

As sugestões a seguir são **direções de projeto**, não fatos já aprovados pela Casa da Esquina.

1. **Padronizar o nome:** decidir como “Casa da Esquina” e “Espaço Casa da Esquina Gourmet” entram na nova marca e corrigir a variante do PedyUN.
2. **Representar a variedade da cozinha:** a oferta de grelhados e porções merece espaço junto aos hambúrgueres; o levantamento dá suporte a uma marca de restaurante com várias ocasiões de consumo.
3. **Organizar o site pelas necessidades do visitante:** conhecer a casa, consultar o cardápio, fazer pedido, verificar horário e encontrar o endereço.
4. **Unificar os dados comerciais:** obter uma lista oficial de produtos, preços, receitas, quantidades e disponibilidade para evitar reproduzir as divergências atuais.
5. **Completar o material visual:** obter fotos autorizadas da fachada, ambiente, equipe e drinks, além de um logo vetorial para a nova identidade.

Uma estrutura inicial de conteúdo pode ter: apresentação da casa, categorias do cardápio, galeria de pratos e ambiente, informações de visita, telefone/WhatsApp e botão para pedidos. Uma seção de história depende de entrevista ou material institucional fornecido pelo restaurante.

### Informações ainda não confirmadas

- Ano de fundação, história do negócio, proprietários, chef e equipe.
- Capacidade do salão, acessibilidade, estacionamento e estrutura infantil.
- Música ao vivo, reservas, eventos privados, taxas de serviço e formas de pagamento.
- Área de entrega, taxa de delivery, pedido mínimo e possibilidade de retirada.
- Carta de drinks, alergênicos, restrições alimentares e procedimentos de preparo.
- Pratos mais vendidos, avaliações e reconhecimentos.

Esses campos devem ser preenchidos com confirmação do restaurante. A existência do destaque Kids, por exemplo, não autoriza escrever “tem espaço kids”. Da mesma forma, as tags do cardápio não substituem informações confirmadas de alergênicos ou de preparo.

## 9. Fontes e limites da pesquisa

| Fonte | URL | Uso no levantamento |
|---|---|---|
| Cardápio Acuolina | [Casa da Esquina](https://acuolina.com/pt/casa-da-esquina/62f81d41237340002367940c) | Cardápio, ingredientes, preços, dados cadastrais, logo e fotografias |
| PedyUN | [Casa da Esquina](https://pedyun.com.br/casadaesquina) | Listagem de pedidos, bebidas, descrições, preços, logo e fotografias |
| Instagram | [@casadaesquinajba](https://www.instagram.com/casadaesquinajba/) | Nome, bio, horário, endereço, telefone e nomes dos destaques |

O HTML do Acuolina e seus dados públicos foram preservados em `pesquisa/fontes/`. O HTML inicial do PedyUN depende de carregamento dinâmico; o cardápio acima foi lido na página carregada no navegador e transcrito no arquivo [pedyun-cardapio.tsv](pesquisa/fontes/pedyun-cardapio.tsv). O rastreamento do link de Instagram enviado foi removido da URL PedyUN, mantendo a mesma página do restaurante.

O Instagram permitiu ler a bio e os nomes dos destaques, mas exigiu login ao tentar abrir publicações e expandir conteúdo. Não foi possível consultar integralmente legendas, stories, carrosséis e histórico. Nenhuma afirmação sobre ambiente ou eventos foi deduzida de descrições automáticas de imagens.

Este é um levantamento das informações publicamente acessíveis nos três canais na data de coleta, não uma declaração de que todo o histórico do estabelecimento foi recuperado. As lacunas e inconsistências permanecem explícitas para orientar a próxima etapa do projeto.
'''
(ROOT/'CASA-DA-ESQUINA.md').write_text(text)
print('Documento salvo. PedyUN:',len(rows),'itens. Acuolina:',sum(len(s['dishes']) for s in acu),'itens. Imagens:',len(imgs))
print('Dimensões:',sorted(set((i['largura'],i['altura']) for i in imgs)))
