<h1 align="center">
Análise das características acústicas de espécies de aves do Pantanal
</h1> 

## Índice

- [Titulo](#titulo)
- [Índice](#indice)
- [Descrição do Projeto](#descricao-do-projeto)
- [Status do Projeto](#status)
- [Funcionalidades](#funcionalidades)
- [Instruções para Executar o Projeto](#instrucoes-execucao)
- [Tecnologias e Ferramentas Utilizadas](#tecnologias-utilizadas)
- [Pessoas Contribuidoras](#pessoas-contribuidoras)
- [Pessoas Desenvolvedoras do Projeto](#pessoas-desenvolvedoras)
- [Conclusão](#conclusao)

## Descrição do Projeto

Este projeto é referida como a parte prática do projeto de iniciação científica do ciclo de 2025/2026 apoiado pela Universidade Federal de Mato Grosso (UFMT) e realizada pela estudante de graduação do curso de Ciência da Computação, Bianca Mitie Nakazawa, sob a orientação do Prof. Dr. Thiago Meirelles Ventura.

Tem como objetivo realizar a análise das características acústicas de espécies de aves do Pantanal a fim de auxiliar na criação de um banco de dados de aves pantaneiras para, posteriormente, a construção de modelos mais robustos de identificação automatizada de aves nesse bioma.

## Status do Projeto

<h4 align="center">
Projeto concluído
</h4>

## Funcionalidades

- **Funcionalidade 1**: Separação dos áudios em segmentos de 3s (padrão).
- **Funcionalidade 2**: Para cada segmento, encontra atividade sonora e faz uma demarcação para adiquirir informações de frequência miníma, frequência máxima e duração.
- **Funcionalidade 3**: Gera imagens do espectrograma desses segmentos e suas marcações de atividade sonora.
- **Funcionalidade 4**: Compara as informações de cada segmento com a tabela .csv para encontrar similaridades com alguma espécie (5 maiores similaridades são salvas).
- **Funcionalidade 5**: Roda o BirdNET e das espécies que teve similariedade tenta encontrar se foi uma das mesmas das 5 espécies encontradas na Funcionalidade 4.
- **Funcionalidade 6**: Caso haja alguma correspondencia, ele salva aquele segmento de áudio em uma pasta com o nome da espécie.

## Instruções para Executar o Projeto

Para esse projeto foi necessário a utilização da distribuição [Anaconda](https://www.anaconda.com/), ao abrir o *Anaconda Navigator* será possível acessar a aba de *Environments* (ou ambientes, em tradução). Ao acessá-lo será necessário criar um novo ambiente e selecionar a opção de utilizar um pacote [Python](https://www.python.org/) e escolher a versão 3.11.X.

Após isso, será necessário abrir o terminal desse ambiente virtual criado e baixar o repositório do [BirdNET Analyzer](https://github.com/birdnet-team/BirdNET-Analyzer) pelo comando:

```bash
pip install birdnet_analyzer
```

Com o repositório baixado será possível, ao acessar a aba *Home*, o acesso a alguns aplicativos que poderão ser instalados/executados nesse ambiente virtual. Para esse projeto será necessário executar o [VS Code](https://code.visualstudio.com/), caso não o tenha instalado, instalá-lo e, então, executá-lo.

Ao acessar o aplicativo será necessário clonar esse repositório, pode ser feito abrindo o terminal e digitando o seguinte comando:

```bash
git clone https://github.com/biancanakazawa/analise-das-caracteristicas-acusticas-de-especies-de-aves-do-pantanal
```

Após isso, pelo próprio terminal acessar a pasta script pelo comando:

```bash
cd script
```

Nesse diretório será possível executar a ```main.py``` pelo comando:

```bash
python main.py
```

Ao executar a ```main.py```, ele perguntará qual o 'nome do diretório de áudios contínuos', você terá que digitar o diretório que encontra os áudios que se deseja analisar, esse diretório deve estar localizada no diretório ```script```. Após isso, esperar para terminar de analisar todos os áudios que estão nesse diretório.

## Tecnologias e Ferramentas Utilizadas

| Ferramenta | Versão |
|---|---:|
| [Python](https://www.python.org/) | `3.11.15`|
| [Anaconda](https://www.anaconda.com/) | `26.5.3`|
| [BirdNET Analyzer](https://github.com/birdnet-team/BirdNET-Analyzer) | `2.4.0`|
| [VS Code](https://code.visualstudio.com/) | `1.135.0`|
| [GitHub](https://github.com/) | - |
| [Claude](https://claude.ai/) | `Sonnet 5` |

## Pessoas Contribuidoras

Esse projeto teve a contribuição do Prof. Dr. Thiago Meirelles Ventura, orientador da pesquisa que proporcionou esse projeto, e dos estudantes de graduação do curso de Ciência da Computação, Leandro Moreira de Carvalho e Rakell Aparecida Barbosa Guimarães, que auxiliaram na construção do arquivo base com as características acústicas. 

### Thiago Meirelles Ventura

### Leandro Moreira de Carvalho

### Rakell Aparecida Barbosa Guimarães

## Pessoas Desenvolvedoras do Projeto

### Bianca Mitie Nakazawa
- [GitHub](https://github.com/biancanakazawa)
- [ORCID](https://orcid.org/0009-0009-6658-0996)
- [Lattes]( http://lattes.cnpq.br/4629350229599265)
