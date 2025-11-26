import os
import django
import pandas as pd
from unidecode import unidecode

# Inicializa o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projeto_GetOS.settings')
django.setup()

from setores.models import Setor
from servidores.models import Servidor


def importar_planilha():
    file_path = 'DEPARTAMENTOS SMPOFTI - EVANDRO.ods'

    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return

    print('📥 Lendo planilha...')
    df = pd.read_excel(file_path, engine='odf')

    secretaria_atual = ''
    setor_atual = ''
    total_servidores = 0
    setores_criados = 0

    for _, row in df.iterrows():
        cel0 = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
        cel1 = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ''
        cel2 = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ''

        # Detectar nova secretaria
        if "SECRETARIA" in cel0:
            secretaria_atual = cel0
            continue

        # Detectar novo setor (aparece como "ORD" em col 0 e o nome do setor na col 1)
        if cel0.upper() == "ORD" and cel1:
            setor_atual = cel1
            continue

        # Ignorar cabeçalhos ou separadores
        if cel1.upper() in ["SERVIDOR", "ORD"] or not cel1 or cel1.isdigit():
            continue

        # Dados válidos
        nome = cel1
        matricula = cel2

        # Gerar sigla do setor
        sigla = ''.join([word[0] for word in unidecode(setor_atual).split() if word.isalpha()][:4]).upper()

        # Criar setor (se ainda não existe)
        setor_obj, created = Setor.objects.get_or_create(
            nome=setor_atual,
            defaults={
                'sigla': sigla,
                'secretaria': secretaria_atual,
                'ramal': '0000'
            }
        )
        if created:
            setores_criados += 1

        # Criar servidor
        servidor_obj, criado = Servidor.objects.get_or_create(
            nome=nome,
            matricula=matricula,
            setor=setor_obj
        )
        if criado:
            total_servidores += 1

    print('\n✅ Importação concluída com sucesso!')
    print(f'📌 Setores criados: {setores_criados}')
    print(f'👥 Servidores inseridos: {total_servidores}')


if __name__ == '__main__':
    importar_planilha()
