"""
Run this script to test your algorithm locally (without building a Docker
image) using the mock client.

Run as:

    python test.py

Make sure to do so in an environment where `vantage6-algorithm-tools` is
installed. This can be done by running:

    pip install vantage6-algorithm-tools
"""
from vantage6.algorithm.tools.mock_client import MockAlgorithmClient
from pathlib import Path

# get path of current directory
current_path = Path(__file__).parent

## Mock client
client = MockAlgorithmClient(
    datasets=[
        # Data for first organization
        [{
            "database": current_path / "test_data.csv",
            "db_type": "csv",
            "input_data": {}
        }],
        # Data for second organization
        [{
            "database": current_path / "test_data.csv",
            "db_type": "csv",
            "input_data": {}
        }]
    ],
    module="v6-hads-scoring"
)

# list mock organizations
organizations = client.organization.list()
print(organizations)
org_ids = [organization["id"] for organization in organizations]

# Run the central method on 1 node and get the results
central_task = client.task.create(
    input_={
        "method": "central",
        "kwargs": {
            "items_to_score": {"items_to_score": {
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

        }
    },
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))
print(results)

# Run the partial method for all organizations
task = client.task.create(
    input_={
        "method": "partial",
        "kwargs": {
            "items_to_score": {"items_to_score": {
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
        }
    },
    organizations=org_ids
)
print(task)

# Get the results from the task
results = client.wait_for_results(task.get("id"))
print(results)
