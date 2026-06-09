import json
import urllib.request
import urllib.parse
from collections import deque
from datetime import datetime, timedelta


ARQUIVO_JSON = "triagens_spacemed.json"


def carregar_triagens(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            triagens = json.load(arquivo)

        print(f"\n{len(triagens)} pacientes carregados do arquivo JSON.")
        return triagens

    except FileNotFoundError:
        print("\nArquivo JSON não encontrado.")
        return []

    except json.JSONDecodeError:
        print("\nO arquivo JSON está com erro de formatação.")
        return []


def criar_fila_triagens(triagens):
    fila = deque()

    for triagem in triagens:
        fila.append(triagem)

    return fila


def listar_triagens(triagens):
    print("\nLista de pacientes:")

    for triagem in triagens:
        print(
            f"{triagem['id']:02d} - "
            f"{triagem['paciente']} | "
            f"{triagem['comunidade']} | "
            f"risco: {triagem['risco']} | "
            f"status: {triagem['status']}"
        )


def ver_fila(fila):
    print("\nFila de atendimento:")

    if not fila:
        print("A fila está vazia.")
        return

    for posicao, triagem in enumerate(fila, start=1):
        print(
            f"{posicao}º - "
            f"ID {triagem['id']:02d} | "
            f"{triagem['paciente']} | "
            f"risco: {triagem['risco']} | "
            f"status: {triagem['status']}"
        )


def ordenar_por_id(triagens):
    return sorted(triagens, key=lambda triagem: triagem["id"])


def busca_binaria_recursiva(lista, id_procurado, inicio, fim):
    if inicio > fim:
        return None

    meio = (inicio + fim) // 2
    id_meio = lista[meio]["id"]

    if id_meio == id_procurado:
        return lista[meio]

    elif id_procurado < id_meio:
        return busca_binaria_recursiva(lista, id_procurado, inicio, meio - 1)

    else:
        return busca_binaria_recursiva(lista, id_procurado, meio + 1, fim)


def buscar_paciente_por_id(triagens):
    try:
        id_busca = int(input("\nDigite o ID do paciente: "))

        triagens_ordenadas = ordenar_por_id(triagens)

        resultado = busca_binaria_recursiva(
            triagens_ordenadas,
            id_busca,
            0,
            len(triagens_ordenadas) - 1
        )

        if resultado:
            exibir_analise_completa(resultado)
        else:
            print("\nPaciente não encontrado.")

    except ValueError:
        print("\nDigite apenas números.")


def atender_proximo_paciente(fila):
    if not fila:
        print("\nNão há pacientes na fila.")
        return

    triagem = fila.popleft()

    print("\nPaciente chamado para atendimento.")
    exibir_analise_completa(triagem)


def consultar_api_nasa_power(latitude, longitude):
    """
    Consulta a API pública NASA POWER.
    A data usada é de 7 dias atrás porque os dados do dia atual podem não estar disponíveis.
    """
    data_consulta = datetime.now() - timedelta(days=7)
    data_formatada = data_consulta.strftime("%Y%m%d")

    parametros = {
        "parameters": "T2M,RH2M,PRECTOTCORR",
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "start": data_formatada,
        "end": data_formatada,
        "format": "JSON"
    }

    url_base = "https://power.larc.nasa.gov/api/temporal/daily/point"
    url = url_base + "?" + urllib.parse.urlencode(parametros)

    try:
        with urllib.request.urlopen(url, timeout=10) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))

        parametros_climaticos = dados["properties"]["parameter"]

        temperatura = list(parametros_climaticos["T2M"].values())[0]
        umidade = list(parametros_climaticos["RH2M"].values())[0]
        chuva = list(parametros_climaticos["PRECTOTCORR"].values())[0]

        return {
            "temperatura": temperatura,
            "umidade": umidade,
            "chuva": chuva
        }

    except Exception:
        return None


def exibir_dados_paciente(triagem):
    print("\nPaciente encontrado:")
    print(f"ID: {triagem['id']:02d}")
    print(f"Nome: {triagem['paciente']}")
    print(f"Idade: {triagem['idade']}")
    print(f"Comunidade: {triagem['comunidade']}")
    print(f"Sintoma informado: {triagem['sintoma']}")
    print(f"Risco médico: {triagem['risco']}")
    print(f"Tipo de conexão: {triagem['conexao']}")
    print(f"Status: {triagem['status']}")


def exibir_dados_regiao(triagem):
    latitude = triagem["latitude"]
    longitude = triagem["longitude"]

    print("\nClima da comunidade:")
    print(f"Comunidade analisada: {triagem['comunidade']}")
    print(f"Localização usada: latitude {latitude}, longitude {longitude}")

    dados_clima = consultar_api_nasa_power(latitude, longitude)

    if dados_clima is None:
        print("\nNão foi possível consultar a API da NASA agora.")
        print("Mesmo assim, o sistema continua funcionando com os dados do JSON.")
        return None

    print(f"Temperatura média: {dados_clima['temperatura']} °C")
    print(f"Umidade relativa: {dados_clima['umidade']}%")
    print(f"Chuva registrada: {dados_clima['chuva']} mm")

    return dados_clima


def gerar_recomendacao_spacemed(triagem, dados_clima):
    risco = triagem["risco"].lower()

    print("\nRecomendação:")

    if dados_clima is None:
        if risco == "vermelho":
            print("Prioridade máxima para atendimento remoto via satélite.")
        elif risco == "amarelo":
            print("Manter acompanhamento e priorizar se houver piora.")
        else:
            print("Atendimento pode seguir o fluxo normal.")
        return

    temperatura = dados_clima["temperatura"]
    umidade = dados_clima["umidade"]
    chuva = dados_clima["chuva"]

    if risco == "vermelho":
        print("O paciente está em risco vermelho e deve ser atendido com prioridade.")

        if chuva > 10:
            print("A chuva está alta na região, então o deslocamento pode ser mais difícil.")
            print("Recomendação: atendimento remoto imediato e acionamento de uma equipe local.")
        elif temperatura > 32:
            print("A temperatura está alta e pode agravar o quadro do paciente.")
            print("Recomendação: atendimento remoto imediato e monitoramento contínuo.")
        else:
            print("Mesmo sem alerta climático crítico, o risco médico exige atendimento urgente.")

    elif risco == "amarelo":
        print("O paciente está em risco amarelo e precisa de acompanhamento.")

        if chuva > 10:
            print("A chuva pode atrasar deslocamentos. É melhor antecipar a avaliação remota.")
        elif umidade > 85:
            print("A umidade está elevada e pode piorar sintomas respiratórios.")
        else:
            print("As condições da região estão estáveis. Manter acompanhamento pela plataforma.")

    elif risco == "verde":
        print("O paciente está em risco verde, sem urgência imediata.")

        if temperatura > 34:
            print("Apesar do risco baixo, o calor está elevado.")
            print("Recomendação: orientar hidratação e repouso.")
        else:
            print("O caso pode seguir o fluxo normal de atendimento remoto.")

    else:
        print("O risco informado não foi reconhecido. Encaminhar para avaliação manual.")


def exibir_analise_completa(triagem):
    exibir_dados_paciente(triagem)
    dados_clima = exibir_dados_regiao(triagem)
    gerar_recomendacao_spacemed(triagem, dados_clima)


def consultar_clima_por_comunidade(triagens):
    comunidades = {}

    for triagem in triagens:
        nome_comunidade = triagem["comunidade"]

        if nome_comunidade not in comunidades:
            comunidades[nome_comunidade] = {
                "latitude": triagem["latitude"],
                "longitude": triagem["longitude"]
            }

    lista_comunidades = list(comunidades.keys())

    print("\nComunidades cadastradas:")

    for indice, comunidade in enumerate(lista_comunidades, start=1):
        print(f"{indice}. {comunidade}")

    try:
        escolha = int(input("\nEscolha uma comunidade pelo número: "))

        if escolha < 1 or escolha > len(lista_comunidades):
            print("\nComunidade inválida.")
            return

        comunidade_escolhida = lista_comunidades[escolha - 1]
        latitude = comunidades[comunidade_escolhida]["latitude"]
        longitude = comunidades[comunidade_escolhida]["longitude"]

        print(f"\nConsultando clima de {comunidade_escolhida}...")

        dados_clima = consultar_api_nasa_power(latitude, longitude)

        if dados_clima is None:
            print("Não foi possível consultar a API da NASA agora.")
            return

        print(f"Temperatura média: {dados_clima['temperatura']} °C")
        print(f"Umidade relativa: {dados_clima['umidade']}%")
        print(f"Chuva registrada: {dados_clima['chuva']} mm")

        print("\nAnálise da região:")

        if dados_clima["chuva"] > 10:
            print("Chuva elevada. Deslocamentos médicos podem ser dificultados.")
        elif dados_clima["temperatura"] > 32:
            print("Temperatura elevada. Atenção a pacientes sensíveis ao calor.")
        elif dados_clima["umidade"] > 85:
            print("Umidade elevada. Pode haver impacto em sintomas respiratórios.")
        else:
            print("Não há alerta climático crítico para essa comunidade.")

    except ValueError:
        print("\nDigite apenas números.")


def ver_resumo_sistema(triagens, fila):
    total = len(triagens)
    total_fila = len(fila)

    riscos = {"verde": 0, "amarelo": 0, "vermelho": 0}

    for triagem in triagens:
        risco = triagem["risco"].lower()
        if risco in riscos:
            riscos[risco] += 1

    print("\nResumo do sistema:")
    print(f"Pacientes carregados: {total}")
    print(f"Pacientes ainda na fila: {total_fila}")
    print(f"Casos verdes: {riscos['verde']}")
    print(f"Casos amarelos: {riscos['amarelo']}")
    print(f"Casos vermelhos: {riscos['vermelho']}")

    print("\nComo o projeto funciona:")
    print("O SpaceMed simula uma solução de telemedicina via satélite para comunidades isoladas.")
    print("Os pacientes ficam salvos em um arquivo JSON junto com a comunidade e a localização.")
    print("A fila organiza a ordem de atendimento.")
    print("A busca por ID usa busca binária recursiva.")
    print("A API NASA POWER traz dados climáticos reais da região do paciente.")


def menu():
    triagens = carregar_triagens(ARQUIVO_JSON)

    if not triagens:
        print("\nNão foi possível iniciar o sistema.")
        return

    fila = criar_fila_triagens(triagens)

    while True:
        print("\n--- SpaceMed ---")
        print("1. Resumo do sistema")
        print("2. Listar pacientes")
        print("3. Ver fila de atendimento")
        print("4. Atender próximo paciente")
        print("5. Buscar paciente por ID")
        print("6. Consultar clima por comunidade")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            ver_resumo_sistema(triagens, fila)

        elif opcao == "2":
            listar_triagens(triagens)

        elif opcao == "3":
            ver_fila(fila)

        elif opcao == "4":
            atender_proximo_paciente(fila)

        elif opcao == "5":
            buscar_paciente_por_id(triagens)

        elif opcao == "6":
            consultar_clima_por_comunidade(triagens)

        elif opcao == "0":
            print("\nSistema encerrado.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()