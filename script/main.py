import objetos

import os
from pathlib import Path

def main():

    print('\n')
    nome_dir_aud_cont = input('Nome do diretório de áudios contínuos: ')
    print('\n')

    caminho_dir_aud_cont = Path(nome_dir_aud_cont)
    if not caminho_dir_aud_cont.is_absolute():
        caminho_dir_aud_cont = Path(os.getcwd()) / nome_dir_aud_cont

    nomes_aud_cont = []

    if caminho_dir_aud_cont.exists() and caminho_dir_aud_cont.is_dir():
        for caminho_arq in caminho_dir_aud_cont.iterdir():
            if caminho_arq.is_file() and caminho_arq.suffix.lower() in ['.wav', '.mp3']:
                nomes_aud_cont.append(caminho_arq.name)
    else:
        print('Diretório não existe.')
        return

    if len(nomes_aud_cont) == 0:
        print('Sem áudios para analisar.')
        return

    dir_seg_temp = 'segmentos/seg_temp'
    dir_especies = 'segmentos/especies'
    dir_imagens = 'imagens'

    aud_cont_csv = 'csv/audios_continuas.csv'
    seg_csv = 'csv/segmentos.csv'
    candidatas_csv = 'csv/candidatas.csv'
    birdnet_csv = 'csv/birdnet.csv'

    tabela_referencia = 'data.csv'

    for index, nome_arq in enumerate(nomes_aud_cont):
        caminho_audio = os.path.join(str(caminho_dir_aud_cont), nome_arq)

        gravacao = objetos.Gravacao(
            id=index,
            nome=nome_arq,
            caminho=caminho_audio
        )
        gravacao.salvar_csv(aud_cont_csv)

        print(f'Processando gravação: {nome_arq}')

        segmentos = gravacao.gerar_segmentos(
            dir_destino=dir_seg_temp,
            duracao=3
        )

        for segmento in segmentos:
            segmento.salvar_csv(seg_csv)

            caracteristicas = objetos.CaractersticasAcusticas(
                segmento_id=segmento._id,
                caminho_audio=segmento._caminho,
                csv_referencia=tabela_referencia
            )
            caracteristicas.extrair_caracteristicas()

            caracteristicas.criar_espectrograma(dir_destino=dir_imagens)

            # metodo == 'cosseno'
            # metodo == 'euclidiana'
            candidatas = caracteristicas.especies_candidatas(metodo='euclidiana')

            if not candidatas:
                print(f'    Segmento {segmento._nome}: Nenhuma espécie correspondente')
                continue

            for candidata in candidatas:
                candidata.salvar_csv(
                    segmento_id=segmento._id,
                    nome_arquivo_segmento=segmento._nome,
                    csv_path=candidatas_csv
                )

            resultado = objetos.BirdNet.melhor_deteccao(
                segmento_id=segmento._id,
                caminho_audio=segmento._caminho,
                candidatas=candidatas
            )

            if resultado is not None:
                resultado.salvar_csv(birdnet_csv)
                segmento.salvar_dir(resultado._especie, dir_especies)
                print(f'    Segmento {segmento._nome}: {resultado._especie.nome_cientifico} (score={resultado._score:.3f})')

    print('\nProcessamento finalizado com sucesso')

if __name__ == '__main__':
    main()