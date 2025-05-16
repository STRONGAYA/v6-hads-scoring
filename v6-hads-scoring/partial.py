import pandas as pd

from typing import Dict
from vantage6.algorithm.tools.decorators import algorithm_client, data
from vantage6.algorithm.client import AlgorithmClient

# General federated algorithm functions
from vantage6_strongaya_general.general_statistics import compute_local_general_statistics, \
    compute_local_adjusted_deviation
from vantage6_strongaya_general.miscellaneous import apply_data_stratification, set_datatypes, safe_log, StratificationDetails
from vantage6_strongaya_general.privacy_measures import apply_sample_size_threshold, mask_unnecessary_variables, \
    apply_differential_privacy
from vantage6_strongaya_rdf.collect_sparql_data import collect_sparql_data

# HADS scoring algorithm functions
from vantage6_strongaya_instruments_licenced.proms.hads_scoring import collect_variable_info, compose_variable_details, \
    orchestrate_scoring, ItemsToScoreInput


@data(1)
@algorithm_client
def partial_hads_general_statistics(client: AlgorithmClient, df: pd.DataFrame, items_to_score: ItemsToScoreInput,
                                    variables_to_stratify: StratificationDetails = None) -> Dict[str, str]:
    """
    Execute the partial algorithm for HADS scoring and general statistics computation.

    Args:
        client (AlgorithmClient): The client to communicate with the vantage6 server.
        df (pd.DataFrame): The DataFrame containing the data to be processed.
        items_to_score (ItemsToScoreInput): Dictionary of modules to score and their respective domains and information
                                           specifying where the necessary responses can be found in the data.
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
        variables_to_stratify (dict, optional): Dictionary of variables to stratify. Defaults to None.
                                                Example:
                                                    {'Age':
                                                            {
                                                            'end': 39,
                                                            'datatype': 'int'
                                                            }
                                                    }

    Returns:
        dict: A dictionary containing the computed general statistics.
    """
    safe_log("info",
             "Executing partial algorithm for HADS scoring and general statistics computation thereof.")

    # Collect the variables that are associated with requested scores
    variables_to_analyse = collect_variable_info(items_to_score)

    # Add the variables to stratify to the variables to analyse
    if isinstance(variables_to_stratify, dict):
        variables_to_analyse = variables_to_analyse + [variable_to_stratify for variable_to_stratify
                                                       in variables_to_stratify.keys()]

    # Retrieve RDF/SPARQL data if its use is indicated in the data - suboptimal solution, to be improved in the future
    if "endpoint" in df.columns:
        df = collect_sparql_data(variables_to_analyse, endpoint=df["endpoint"].iloc[0])

    # Mask unnecessary variables by removal - relevant, for example, with csv data
    df = mask_unnecessary_variables(df, variables_to_analyse)

    # Collect variable details from scoring tables
    variable_details = compose_variable_details(items_to_score, False)

    # Add the variables to stratify details to the variables to analyse details
    if isinstance(variables_to_stratify, dict):
        variable_details = variable_details | variables_to_stratify if variables_to_stratify else variable_details

    # Set datatypes for each variable
    df = set_datatypes(df, variable_details)

    # Apply stratification if necessary
    df = apply_data_stratification(df, variables_to_stratify)

    # Ensure that the sample size threshold is met
    df = apply_sample_size_threshold(client, df, variables_to_analyse)

    # Apply differential privacy (Laplace mechanism as per default)
    df = apply_differential_privacy(df, variables_to_analyse, epsilon=1.0, return_type='dataframe')

    # Perform scoring
    df = orchestrate_scoring(df, items_to_score)

    # Collect variable details for scores
    variable_details = compose_variable_details(items_to_score, True)

    # Ensure that the sample size threshold is met after scoring
    df = apply_sample_size_threshold(client, df, variables_to_analyse)

    # Set datatypes for each variable
    df = set_datatypes(df, variable_details)

    # Compute general statistics
    result = compute_local_general_statistics(df, variable_details)

    return result


@data(1)
@algorithm_client
def partial_hads_aggregate_adjusted_deviation(client: AlgorithmClient, df: pd.DataFrame,
                                              items_to_score: ItemsToScoreInput,
                                              numerical_aggregated_results: Dict[str, str],
                                              variables_to_stratify: StratificationDetails = None) -> dict[str, str]:
    """
    Execute the partial algorithm for HADS scoring and aggregate-adjusted deviation computation.

    Args:
        client (AlgorithmClient): The client to communicate with the vantage6 server.
        items_to_score (ItemsToScoreInput): Dictionary of modules to score and their respective domains and information
                                           specifying where the necessary responses can be found in the data.
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
        numerical_aggregated_results (dict): Dictionary of numerical aggregated results.
        variables_to_stratify (StratificationDetails, optional): Dictionary of variables to stratify. Defaults to None.
                                                                Example:
                                                                    {'Age':
                                                                            {
                                                                            'end': 39,
                                                                            'datatype': 'int'
                                                                            }
                                                                    }

    Returns:
        dict: A dictionary containing the computed aggregate adjusted deviation.
    """
    safe_log("info",
             "Executing partial algorithm to compute HADS scoring and aggregate adjusted deviation.")

    # Collect the variables that are associated with requested scores
    variables_to_analyse = collect_variable_info(items_to_score)

    # Add the variables to stratify to the variables to analyse
    variables_to_analyse = variables_to_analyse + [variable_to_stratify for variable_to_stratify
                                                   in variables_to_stratify.keys()]

    # Retrieve RDF/SPARQL data if its use is indicated in the data - suboptimal solution, to be improved in the future
    if "endpoint" in df.columns:
        df = collect_sparql_data(variables_to_analyse, endpoint=df["endpoint"].iloc[0])

    # Mask unnecessary variables by removal - relevant, for example, with csv data
    df = mask_unnecessary_variables(df, variables_to_analyse)

    # Collect variable details from scoring tables
    variable_details = compose_variable_details(items_to_score, False)

    # Add the variables to stratify details to the variables to analyse details
    variable_details = variable_details | variables_to_stratify

    # Set datatypes for each variable
    df = set_datatypes(df, variable_details)

    # Apply stratification if necessary
    df = apply_data_stratification(df, variables_to_stratify)

    # Ensure that the sample size threshold is met
    df = apply_sample_size_threshold(client, df, variables_to_analyse)

    # Apply differential privacy (Laplace mechanism as per default)
    df = apply_differential_privacy(df, variables_to_analyse, epsilon=1.0, return_type='dataframe')

    # Perform scoring
    df = orchestrate_scoring(df, items_to_score)

    # Collect variable details for scores
    variable_details = compose_variable_details(items_to_score, True)

    # Ensure that the sample size threshold is met after scoring
    df = apply_sample_size_threshold(client, df, variables_to_analyse)

    # Set datatypes for each variable
    df = set_datatypes(df, variable_details)

    # Compute aggregate-adjusted deviation
    result = compute_local_adjusted_deviation(df, numerical_aggregated_results)

    return result
