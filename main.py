#Import the Azure OpenAI client used to connect to the LLM.
from llm.azure_client import AzureLLMClient

# mport the Connect-4 experiment functions for the three baseline matchups.
from experiments.llm_experiments import (
    run_llm_vs_random,
    run_llm_vs_heuristic,
    run_llm_vs_minimax,
)

#Import the CSV logger used to save summary results.
from experiments.csv_logger import append_result_to_csv

#Create the Azure LLM client using environment variable settings.
client = AzureLLMClient()

#Number of games to run for each matchup.
NUM_GAMES = 100

#Run the full set of final Connect-4 experiments.
results = [
    run_llm_vs_random(client, num_games=NUM_GAMES, llm_as="X", log_games=True),
    run_llm_vs_random(client, num_games=NUM_GAMES, llm_as="O", log_games=True),
    run_llm_vs_heuristic(client, num_games=NUM_GAMES, llm_as="X", log_games=True),
    run_llm_vs_heuristic(client, num_games=NUM_GAMES, llm_as="O", log_games=True),
    run_llm_vs_minimax(client, num_games=NUM_GAMES, llm_as="X", depth=3, log_games=True),
    run_llm_vs_minimax(client, num_games=NUM_GAMES, llm_as="O", depth=3, log_games=True),
]

#Print each summary result and save it to the final batch CSV file.
for result in results:
    print(result)
    append_result_to_csv(result, filename="final_batch_results_connect4.csv")