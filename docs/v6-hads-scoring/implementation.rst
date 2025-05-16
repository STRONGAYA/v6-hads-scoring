Implementation
==============

Overview
--------

Central
-------
The central part is responsible for the orchestration and aggregation of the algorithm.

``central``
~~~~~~~~~~~

In this case, the `central` function aggregates HADS results from multiple organisations.

1) Input Validation: The code begins by checking if the user's input structure is correct. If not, it raises a UserInputError.

2) Organisation IDs Collection: It collects all organisation IDs that participate in the collaboration, unless specific organisation IDs are provided.

3) General Statistics Subtask Creation: The code creates a partial task to calculate HADS scores and their general statistics.
This involves specifying the method and its parameters, creating the task, and waiting for the results.
This partial task is using the `partial_hads_general_statistics` function.

4) Aggregate General Statistics: Once the results are obtained, the code aggregates the general statistics.

5) Aggregate-Adjusted Deviation Subtask Creation: Another subtask is created to calculate the aggregate-adjusted deviation using the aggregated numerical general statistics.
This subtask is also created, and the code waits for its results.
This partial task is using the `partial_hads_aggregate_adjusted_deviation` function.

6) Final Aggregation: The code computes the aggregate of the aggregate-adjusted deviation and includes it in the general statistics.

Overall, the code orchestrates the processing of the HADS questionnaire, handling input validation, task creation, result aggregation, and final computation.

Partials
--------
Partials are the computations that are executed on each data station (or node). The partials have access
to the data that is stored on the node. The partials are executed in parallel on each
node.

``partial_hads_general_statistics``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function executes the partial algorithm for HADS scoring and general statistics computation.

1) Variable Collection: It collects the variables associated with the requested scores and adds any variables specified for stratification.

2) Data Retrieval: If the DataFrame contains an "endpoint" column, it retrieves RDF/SPARQL data.

3) Mask redundant variables: Removes unnecessary variables from the DataFrame.

4) Variable Details Composition: The function composes variable details from the scoring tables and adds stratification details if necessary.

5) Data Preparation: It sets the datatypes for each variable and applies stratification if required.

6) Sample Size Threshold: The function ensures that the sample size threshold is met before and after scoring.

7) Differential Privacy: It applies differential privacy using the Laplace mechanism.

8) Scoring: The function performs the scoring based on the provided items to score.

9) Post-Scoring Processing: It composes variable details for the scores, ensures the sample size threshold is met again, and sets the datatypes for each variable.

10) General Statistics Computation: Finally, it computes the local general statistics and returns the result.

Overall, the function orchestrates the scoring and general statistics computation for the HADS questionnaire, handling variable collection, data retrieval, preparation, scoring, and final computation.

``partial_hads_aggregate_adjusted_deviation``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function executes the partial algorithm for HADS scoring and aggregate adjusted deviation computation.

1) Variable Collection: It collects the variables associated with the requested scores and adds any variables specified for stratification.

2) Data Retrieval: If the DataFrame contains an "endpoint" column, it retrieves RDF/SPARQL data.

3) Mask redundant variables: Removes unnecessary variables from the DataFrame.

4) Variable Details Composition: The function composes variable details from the scoring tables and adds stratification details if necessary.

5) Data Preparation: It sets the datatypes for each variable and applies stratification if required.

6) Sample Size Threshold: The function ensures that the sample size threshold is met before and after scoring.

7) Differential Privacy: It applies differential privacy using the Laplace mechanism.

8) Scoring: The function performs the scoring based on the provided items to score.

9) Post-Scoring Processing: It composes variable details for the scores, ensures the sample size threshold is met again, and sets the datatypes for each variable.

10) Aggregate-Adjusted Deviation Computation: Finally, it computes the local aggregate-adjusted deviation using the numerical aggregated results and returns the result.

Overall, the function orchestrates the scoring and aggregate-adjusted deviation computation for the HADS questionnaire, handling variable collection, data retrieval, preparation, scoring, and final computation.