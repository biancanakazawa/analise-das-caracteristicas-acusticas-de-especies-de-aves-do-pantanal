from __future__ import annotations

import librosa
import librosa.display
import os

import soundfile as sf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from pathlib import Path
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer

class Gravacao:
    def __init__(self, id, nome, caminho):
        self._id = id
        self._nome = nome
        self._caminho = caminho
        self._data = None
        self._hora = None
        self._local = None

    def gerar_segmentos(self, dir_destino: str, duracao: int = 3) -> list[Segmento]:
        segmentos = []

        audio, sr = librosa.load(self._caminho, sr=None)
        samples_seg = sr * duracao

        caminho_destino = Path(dir_destino)
        caminho_destino.mkdir(parents=True, exist_ok=True)

        for i, inicio in enumerate(range(0, len(audio), samples_seg)):
            fim = min(inicio + samples_seg, len(audio))

            trecho = audio[inicio:fim]

            if len(trecho) < sr * 1:
                break

            inicio_segundos = inicio / sr
            fim_segundos = fim / sr

            nome_arquivo = f'{self._nome}_seg_{i:04d}.wav'
            caminho_seg = caminho_destino / nome_arquivo

            sf.write(caminho_seg, trecho, sr)

            segmento = Segmento(
                id=i,
                gravacao_id=self._id,
                inicio=inicio_segundos,
                fim=fim_segundos,
                nome=nome_arquivo,
                caminho=str(caminho_seg)
            )

            segmentos.append(segmento)

        return segmentos

    def salvar_csv(self, caminho_csv: str):
        Path(caminho_csv).parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame([{
            'id': self._id,
            'nome': self._nome,
            'caminho': self._caminho,
            'data': self._data,
            'hora': self._hora,
            'local': self._local
        }])

        if not Path(caminho_csv).exists():
            df.to_csv(caminho_csv, index=False)
        else:
            df.to_csv(caminho_csv, mode='a', header=False, index=False)

class Segmento:
    def __init__(self, id, gravacao_id, inicio, fim, nome, caminho):
        self._id = id
        self._gravacao_id = gravacao_id
        self._inicio = inicio
        self._fim = fim
        self._nome = nome
        self._caminho = caminho

    def salvar_csv(self, caminho_csv: str):
        Path(caminho_csv).parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame([{
            'id': self._id,
            'gravacao_id': self._gravacao_id,
            'inicio': self._inicio,
            'fim': self._fim,
            'nome': self._nome,
            'caminho': self._caminho
        }])

        if not Path(caminho_csv).exists():
            df.to_csv(caminho_csv, index=False)
        else:
            df.to_csv(caminho_csv, mode='a', header=False, index=False)

    def salvar_dir(self, especie: Especie, dir_base: str):
        dir_especie = Path(dir_base) / especie.nome_cientifico.replace(' ', '_')
        dir_especie.mkdir(parents=True, exist_ok=True)

        destino = dir_especie / self._nome
        Path(self._caminho).replace(destino)
        self._caminho = str(destino)

class Especie:
    def __init__(self, nome_cientifico, nome_comum=''):
        self.nome_cientifico = nome_cientifico
        self.nome_comum = nome_comum

class CaractersticasAcusticas:
    def __init__(self, segmento_id: int, caminho_audio: str, csv_referencia: str = "data.csv"):
        self._segmento_id = segmento_id
        self._caminho_audio = caminho_audio
        self._csv_referencia = csv_referencia
        self._caracteristicas = []

    def extrair_caracteristicas(self, top_db: int = 15):
        y, sr = librosa.load(self._caminho_audio, sr=None)
        intervals = librosa.effects.split(y=y, top_db=top_db)

        self._caracteristicas = []

        for i, (start, end) in enumerate(intervals):
            segment = y[start:end]
            length_segment = (end - start) / sr
            start_segment = start / sr
            end_segment = end / sr

            n_fft = 2048 if len(segment) >= 2048 else len(segment)
            if n_fft < 2:
                continue

            D = np.abs(librosa.stft(segment, n_fft=n_fft))
            DB = librosa.amplitude_to_db(D, ref=np.max)
            freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
            db_per_bin = DB.max(axis=1)

            active_bins = np.where(db_per_bin > -top_db)[0]
            if len(active_bins) == 0:
                min_freq, max_freq = None, None
            else:
                min_freq = float(freqs[active_bins].min())
                max_freq = float(freqs[active_bins].max())

            if i + 1 < len(intervals):
                gap = (intervals[i + 1][0] / sr) - end_segment
            else:
                gap = None

            self._caracteristicas.append({
                'start_segment': start_segment,
                'length_segment': length_segment,
                'f_min': min_freq,
                'f_max': max_freq,
                'intersyllable_gap': gap,
            })

        return self._caracteristicas

    def criar_espectrograma(self, dir_destino: str):
        Path(dir_destino).mkdir(parents=True, exist_ok=True)

        audio, sr = librosa.load(self._caminho_audio, sr=None)
        D = librosa.stft(audio)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

        coordenadas = [
            (
                coordenada['start_segment'],
                coordenada['f_min'],
                coordenada['start_segment'] + coordenada['length_segment'],
                coordenada['f_max'],
            )
            for coordenada in self._caracteristicas
            if coordenada['f_min'] is not None and coordenada['f_max'] is not None
        ]

        nome_audio = Path(self._caminho_audio).name

        self._criar_imagem_espectrograma(dir_destino, nome_audio, S_db, sr, coordenadas)

    @staticmethod
    def _criar_imagem_espectrograma(dir_destino, nome_audio, S_db, sr, coordenadas):
        nome_sem_extensao = os.path.splitext(nome_audio)[0]
        caminho_imagem = os.path.join(dir_destino, nome_sem_extensao + '.png')

        fig, ax = plt.subplots(figsize=(12, 4))

        img = librosa.display.specshow(
            S_db,
            sr=sr,
            x_axis='time',
            y_axis='linear',
            ax=ax
        )

        for t_min, f_min, t_max, f_max in coordenadas:
            width = t_max - t_min
            height = f_max - f_min

            rectangle = patches.Rectangle(
                xy=(t_min, f_min),
                width=width,
                height=height,
                linewidth=0.5,
                edgecolor='green',
                facecolor='none'
            )
            ax.add_patch(rectangle)

        ax.set(title=nome_sem_extensao + ' Espectrograma')

        fig.colorbar(img, ax=ax, format='%2.0f dB')

        plt.savefig(caminho_imagem)
        plt.close(fig=fig)

    def especies_candidatas(self, top_n: int = 5, metodo: str = 'cosseno') -> list['EspecieCandidata']:
        if not self._caracteristicas:
            return []

        df_ref = pd.read_csv(self._csv_referencia).rename(columns={
            'End Time (s)': 'end_time',
            'Start of the next vocalization (s)': 'start_next',
        })

        colunas = ['f_min', 'f_max', 'start_segment', 'length_segment', 'intersyllable_gap']
        medias = df_ref[colunas].mean()
        desvios = df_ref[colunas].std().replace(0, 1)

        def vetorizar(valores: dict) -> np.ndarray:
            return np.array([
                0.0 if valores[c] is None else (valores[c] - medias[c]) / desvios[c]
                for c in colunas
            ])

        vetores_por_especie: dict[str, list[np.ndarray]] = {}
        for _, linha in df_ref.iterrows():
            vetores_por_especie.setdefault(linha['Specie'], []).append(
                vetorizar(linha[colunas].to_dict())
            )

        melhores_por_especie = {}

        for caracteristica in self._caracteristicas:
            vetor_segmento = vetorizar(caracteristica)

            for nome, vetores in vetores_por_especie.items():
                for vetor_especie in vetores:
                    sim = self._calcular_similaridade(vetor_segmento, vetor_especie, metodo)

                    atual = melhores_por_especie.get(nome)
                    melhor = (
                        atual is None
                        or (metodo != 'euclidiana' and sim > atual)
                        or (metodo == 'euclidiana' and sim < atual)
                    )
                    if melhor:
                        melhores_por_especie[nome] = sim

        candidatas = [
            EspecieCandidata(Especie(nome.replace('_', ' ')), sim)
            for nome, sim in melhores_por_especie.items()
        ]
        candidatas.sort(key=lambda c: c._similaridade, reverse=(metodo != 'euclidiana'))
        
        return candidatas[:top_n]

    @staticmethod
    def _calcular_similaridade(v1, v2, metodo):
        if metodo == 'cosseno':
            n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
            return 0.0 if n1 == 0 or n2 == 0 else float(np.dot(v1, v2) / (n1 * n2))
        
        elif metodo == 'euclidiana':
            return float(np.linalg.norm(v1 - v2))
        
        raise ValueError(f'Método desconhecido: {metodo}')

class EspecieCandidata:
    def __init__(self, especie: Especie, similaridade):
        self._especie = especie
        self._similaridade = similaridade

    def salvar_csv(self, segmento_id, nome_arquivo_segmento, csv_path: str):
        Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame([{
            'segmento_id': segmento_id,
            'segmento_arquivo': nome_arquivo_segmento,
            'especie_cientifica': self._especie.nome_cientifico,
            'similaridade': self._similaridade
        }])
        if not Path(csv_path).exists():
            df.to_csv(csv_path, index=False)
        else:
            df.to_csv(csv_path, mode='a', header=False, index=False)

_analyzer_global = None

def get_analyzer() -> Analyzer:
    global _analyzer_global
    if _analyzer_global is None:
        _analyzer_global = Analyzer()
    return _analyzer_global

class BirdNet:
    def __init__(self, segmento_id, especie: Especie, score):
        self._segmento_id = segmento_id
        self._especie = especie
        self._score = score

    @staticmethod
    def melhor_deteccao(segmento_id: int, caminho_audio: str, candidatas: list[EspecieCandidata], min_conf: float = 0.01) -> 'BirdNet | None':
        nomes_candidatos = {c._especie.nome_cientifico.lower() for c in candidatas}

        analyzer = get_analyzer()
        recording = Recording(analyzer, caminho_audio, min_conf=min_conf)
        recording.analyze()

        deteccoes_filtradas = [
            d for d in recording.detections
            if d['scientific_name'].lower() in nomes_candidatos
        ]

        if not deteccoes_filtradas:
            return None

        melhor = max(deteccoes_filtradas, key=lambda d: d['confidence'])

        especie_vencedora = Especie(
            nome_cientifico=melhor['scientific_name'],
            nome_comum=melhor['common_name']
        )

        return BirdNet(segmento_id=segmento_id, especie=especie_vencedora, score=melhor['confidence'])

    def salvar_csv(self, caminho_csv: str):
        Path(caminho_csv).parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame([{
            'segmento_id': self._segmento_id,
            'especie_cientifica': self._especie.nome_cientifico,
            'especie_comum': self._especie.nome_comum,
            'score': self._score
        }])

        if not Path(caminho_csv).exists():
            df.to_csv(caminho_csv, index=False)
        else:
            df.to_csv(caminho_csv, mode='a', header=False, index=False)
