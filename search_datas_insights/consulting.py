import pandas as pd
import google.generativeai as genai
from tqdm import tqdm
import os
from config import API_KEY

INPUT_FILE = '../data/anomalies_bc.csv'
OUTPUT_FILE = '../data/insights.csv'
MODEL_NAME = 'gemini-1.5-flash-latest'

SYSTEM_INSTRUCTION = (
    "Você é um especialista no tema de balança comercial no Brasil. "
    "Eu enviarei informações sobre dias específicos da balança comercial. "
    "Explique o que estava acontecendo nesses dias, procure por anomalias e "
    "me dê insights sobre isso. Por favor, um resumo por dia."
)

def configure_api():
    """Configura a API do Gemini com a chave fornecida."""
    if not API_KEY:
        raise ValueError("A variável API_KEY não foi encontrada. Verifique seu arquivo config.py.")
    genai.configure(api_key=API_KEY)

def generate_insight(row, model):
    """
    Gera um insight para uma única linha do DataFrame usando a API do Gemini.
    """
    date_str = row['ds'].strftime('%Y-%m-%d')
    value = row['y']
    
    prompt = (
        f"Na data de {date_str}, o valor da balança comercial foi {value}. "
        "Com base no seu conhecimento da economia brasileira, quais eventos ou fatores econômicos "
        "significativos poderiam explicar este valor específico neste dia? Forneça um resumo conciso."
    )
    
    try:
        response = model.generate_content(prompt)
        if response.candidates and response.text:
            return response.text.strip()
        else:
            return "Conteudo bloqueado, nao sendo gerado"
    except Exception as e:
        print(f"Ocorreu um erro para a data {date_str}: {e}")
        return "Erro ao gerar o insight."

def main():
    """
    Função principal para ler os dados, gerar os insights e salvar os resultados.
    """
    print("Iniciando o processo de geração de insights...")
    
    configure_api()
    model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_INSTRUCTION)

    try:
        df = pd.read_csv(INPUT_FILE, parse_dates=['ds'])
        print(f"Carregados {len(df)} registros de {INPUT_FILE}")
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada não encontrado em {INPUT_FILE}")
        return

    tqdm.pandas(desc="Gerando Insights")
    df['insights'] = df.progress_apply(lambda row: generate_insight(row, model), axis=1)
    
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\nProcesso concluído. Insights salvos em {OUTPUT_FILE}")
    print("\nAmostra do resultado final:")
    print(df.head())

if __name__ == "__main__":
    main()
