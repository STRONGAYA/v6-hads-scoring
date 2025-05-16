Privacy
=======

Guards
------
The algorithm uses 4 privacy-enhancing functions:

Removal of redundant data
~~~~~~~~~~~~~~~~~~~~~~~~~
As a simple precaution, any redundant data is removed from the working draft of the data to reduce the likelihood that sensitive information is logged.
The redundancy is determined by specifying the variables necessary to calculate the HADS scores and the variables that are used for data stratification.

Sample size threshold
~~~~~~~~~~~~~~~~~~~~~
Sample size thresholding is included to prevent the identification of individuals in case of small sample sizes.
The algorithm tries to fetch the sample size threshold from the environment variables, which are specified in the data station configuration file.
In case the environment variable is not set, the algorithm will use a default value of 10.

Differential privacy
~~~~~~~~~~~~~~~~~~~~
Differential privacy using a Laplace mechanism to add noise to the data.
The epsilon value is set to 1, which is a sensible value for questionnaire responses.
Differential privacy is applied after any data stratification, and before any scores are computed.


Safe computation and logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The algorithm uses two helper functions that reduce the chance of leaking sensitive information in the logs.

The safe computation function makes sure that any computation is performed in a try and except block.
This means that if an error occurs, the algorithm will not crash and prevent that any sensitive data make it directly to the log.
Instead the error is logged separately of computation using safe logging.

The safe logging for example enforces that only strings are passed to the Vantage6 logging functions.
It also limits the number of variable names shown in the log to 5 to reduce the risk of data mining.


Data sharing
------------

The algorithm shares general statistics of the HADS scores (the user can specify which modules exactly).
The general statistics contain:
- Minimum;
- 25th percentile;
- 50th percentile;
- 75th percentile;
- Maximum;
- Mean;
- Standard deviation;
- Missing value count;
- Row count;
- Outlier count (what is considered an outlier is based on the HADS questions).

Vulnerabilities to known attacks
--------------------------------

    * - Attack
      - Risk eliminated?
      - Risk analysis
    * - Reconstruction
      - ✔
      - The amount of information shared was considered insufficient to allow reconstruction of the data underlying the model.
        Especially seeing the incorporated sample size threshold and differential privacy.
    * - Differencing
      - ✔
      - This is indeed possible in two scenarios:
        1) If a data station manager were to change the dataset after performing a task, reperforming the task could be used to perform a differencing attack;
        2) If a user makes minor tweaks to the stratification setup, this could be used to perform a differencing attack.
        These risk of two scenarios is reduced in the algorithm by:
        1) not allowing data station managers to run tasks in the Vantage6 framework;
        2) adding deterministic noise using differential privacy before any computations are performed or data is shared.
    * - Deep Leakage from Gradients (DLG)
      - ✔
      - This is not possible with the data that is shared, especially given the use of differential privacy.
    * - Generative Adversarial Networks (GAN)
      - ✔
      - Synthetic can indeed be used to (statistically) reproduce the data that underlies the statistics, but without knowing the sensitive information the adversary will not be able to assess its authenticity.
        On top of that, the incorporated differential privacy further reduces this risk.
    * - Model Inversion
      - ✔
      - This is not possible with the data that is shared and without knowing the sensitive information the adversary will not be able to assess the authenticity if information was inferred.
        The incorporated differential privacy further reduces this risk.
    * - Watermark Attack
      - ⚠
      - To be determined

For reference:

- Reconstruction: This attack involves an adversary trying to reconstruct the original dataset from the shared model parameters. This is a risk if the model reveals too much information about the data it was trained on.
- Differencing: This attack involves an adversary trying to infer information about a specific data point by comparing the outputs of a model trained with and without that data point.
- Deep Leakage from Gradients (DLG): In this attack, an adversary tries to infer the training data from the shared gradient updates during the training process. This is a risk in federated learning where model updates are shared between participants.
- Generative Adversarial Networks (GAN): This is not an attack per se, but GANs can be used by an adversary to generate synthetic data that is statistically similar to the original data, potentially revealing sensitive information.
- Model Inversion: This attack involves an adversary trying to infer the input data given the output of a model. In a federated learning context, this could be used to infer sensitive information from the model's predictions.
- Watermark Attack: This attack involves an adversary embedding a "watermark" in the model during training, which can later be used to identify the model or the data it was trained on. This is a risk in federated learning where multiple parties contribute to the training of a model.
