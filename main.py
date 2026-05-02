from llm.azure_client import AzureLLMClient
from experiments.llm_experiments import run_llm_vs_random, run_llm_vs_heuristic
from experiments.csv_logger import append_result_to_csv

client = AzureLLMClient()

results = [
    run_llm_vs_random(client, num_games=10, llm_as="X", log_games=True),
    run_llm_vs_random(client, num_games=10, llm_as="O", log_games=True),
    run_llm_vs_heuristic(client, num_games=10, llm_as="X", log_games=True),
    run_llm_vs_heuristic(client, num_games=10, llm_as="O", log_games=True),
]

for result in results:
    print(result)
    append_result_to_csv(result, filename="batch_results_10games.csv")