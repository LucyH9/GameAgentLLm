from llm.azure_client import AzureLLMClient
from experiments.llm_experiments import (
    run_llm_vs_random,
    run_llm_vs_heuristic,
    run_llm_vs_minimax,
)
from experiments.csv_logger import append_result_to_csv

client = AzureLLMClient()

NUM_GAMES = 100

results = [
    run_llm_vs_random(client, num_games=NUM_GAMES, llm_as="X", log_games=True),
    run_llm_vs_random(client, num_games=NUM_GAMES, llm_as="O", log_games=True),
    run_llm_vs_heuristic(client, num_games=NUM_GAMES, llm_as="X", log_games=True),
    run_llm_vs_heuristic(client, num_games=NUM_GAMES, llm_as="O", log_games=True),
    run_llm_vs_minimax(client, num_games=NUM_GAMES, llm_as="X", depth=3, log_games=True),
    run_llm_vs_minimax(client, num_games=NUM_GAMES, llm_as="O", depth=3, log_games=True),
]

for result in results:
    print(result)
    append_result_to_csv(result, filename="final_batch_results_connect4.csv")