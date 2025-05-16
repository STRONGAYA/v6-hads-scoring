from typing import Any, Dict, List

from vantage6.algorithm.tools.decorators import algorithm_client
from vantage6.algorithm.tools.exceptions import UserInputError
from vantage6.algorithm.client import AlgorithmClient

# General federated algorithm functions
from vantage6_strongaya_general.miscellaneous import collect_organisation_ids, safe_log, StratificationDetails
from vantage6_strongaya_general.general_statistics import compute_aggregate_general_statistics, \
    compute_aggregate_adjusted_deviation

# HADS scoring algorithm functions
from vantage6_strongaya_instruments_licenced.proms.hads_scoring import check_input_structure, ItemsToScoreInput


@algorithm_client
def central(client: AlgorithmClient, items_to_score: ItemsToScoreInput,
            variables_to_stratify: StratificationDetails = None,
            organisation_ids: List[int] = None) -> Dict[str, Any]:
    """
    Central function to aggregate HADS scoring results from multiple organisations.

    Args:
        client (AlgorithmClient): The client to communicate with the vantage6 server.
        items_to_score (ItemsToScoreInput): Dictionary of scales and information specifying where the necessary responses
                               can be found in the data.
                               Example:
                                {"items_to_score": {
                                                   "scale_to_score": ["anxiety", "depression"],
                                                   "variable_info": {
                                                                    "question_1": "Q1",
                                                                    "question_2": "Q2",
                                                                    "question_3": "Q3",
                                                                    "question_4": "Q4",
                                                                    "question_5": "Q5",
                                                                    "question_6": "Q6",
                                                                    "question_7": "Q7",
                                                                    "question_8": "Q8",
                                                                    "question_9": "Q9",
                                                                    "question_10": "Q10",
                                                                    "question_11": "Q11",
                                                                    "question_12": "Q12",
                                                                    "question_13": "Q13",
                                                                    "question_14": "Q14"
                                                                    }
                                                   }

                                }
        variables_to_stratify (StratificationDetails, optional): Dictionary of variables to stratify. Defaults to None.
                                                                Example:
                                                                    {'Age':
                                                                            {
                                                                            'end': 39,
                                                                            'datatype': 'int'
                                                                            }
                                                                    }
        organisation_ids (list[int], optional): List of organisation IDs to include.
                                                Defaults to None - therewith include all organisations.

    Returns:
        dict|None: A dictionary containing the aggregated HADS scoring results.
    """
    # Check if the users' input structure is correct
    if not check_input_structure(items_to_score):
        raise UserInputError("Algorithm input is incorrect. Please check the algorithm input.")

    # Collect all organisations that participate in this collaboration unless specified
    organisation_ids = collect_organisation_ids(organisation_ids, client)

    # Create the subtask for general statistics
    safe_log("info", "Creating subtask to calculate HADS scores and their general statistics.")

    input_ = {"method": "partial_hads_general_statistics",
              "kwargs": {
                  "items_to_score": items_to_score,
                  "variables_to_stratify": variables_to_stratify}
              }

    task_general_statistics = client.task.create(input_, organisation_ids,
                                                 "HADS Scoring - General Statistics",
                                                 "This subtask determines the general statistics of HADS scores.")

    # Wait for the node(s) to return the results of the subtask
    safe_log("info", f"Waiting for results of task {task_general_statistics.get('id')}")
    results_general_statistics = client.wait_for_results(task_general_statistics.get("id"))
    safe_log("info", f"Results of task {task_general_statistics.get('id')} obtained")

    # Aggregate the general statistics
    results_general_statistics = compute_aggregate_general_statistics(results_general_statistics)

    # Create a subtask to calculate aggregate-adjusted deviation; using the aggregated numerical general statistics
    safe_log("info", "Creating subtask to calculate aggregate-adjusted deviation using general statistics.")

    input_ = {"method": "partial_hads_aggregate_adjusted_deviation",
              "kwargs": {
                  "numerical_aggregated_results": results_general_statistics["numerical_general_statistics"],
                  "items_to_score": items_to_score,
                  "variables_to_stratify": variables_to_stratify}
              }

    task_adjusted_deviation = client.task.create(input_, organisation_ids,
                                                 "HADS Scoring - Aggregate Adjusted Deviation",
                                                 "This subtask determines the aggregate-adjusted deviation of "
                                                 "HADS scores.")

    # Wait for the node(s) to return the results of the subtask
    safe_log("info", f"Waiting for results of task {task_adjusted_deviation.get('id')}")
    results_deviation = client.wait_for_results(task_adjusted_deviation.get("id"))
    safe_log("info", f"Results of task {task_adjusted_deviation.get('id')} obtained")

    # Compute the aggregate of the aggregate-adjusted deviation and include it in the general statistics
    results = compute_aggregate_adjusted_deviation(results_deviation, results_general_statistics)

    # Return the final results of the algorithm
    return results
