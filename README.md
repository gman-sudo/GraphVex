# GraphVex

GraphVex is a Python-based Anti-Money Laundering (AML) detection system
built as a portfolio project.

The project combines transaction behaviour analysis, rule-based
detection, transaction graph analysis, risk scoring, and customer-level
investigation cases into one pipeline.

The main goal of GraphVex is to explore how different AML signals can be
combined into an explainable workflow rather than treating every
transaction as an isolated event.

## What it does

GraphVex currently looks for four types of suspicious behaviour:

-   High transaction velocity
-   Unusual transaction amounts
-   Structuring-like activity
-   Circular movement of funds

The output is not limited to a transaction-level alert. Detected signals
are aggregated to the customer level and converted into investigation
cases with a risk score and an explanation.

The overall flow is:

``` text
Transactions
    |
    v
Canonical transaction schema
    |
    v
Feature engineering
    |
    +----------------------+
    |                      |
    v                      v
Rule-based detection    Graph analysis
    |                      |
    +----------+-----------+
               |
               v
        Transaction risk
               |
               v
        Customer risk
               |
               v
      Investigation cases
```

## Project structure

``` text
GraphVex/
|
├── data/
│   └── synthetic/
│       ├── ground_truth.parquet
│       └── transactions.parquet
|
├── src/
│   └── graphvex/
│       ├── anomaly/
│       ├── explainability/
│       │   ├── case_builder.py
│       │   └── explainer.py
│       │
│       ├── features/
│       │   └── transaction_features.py
│       │
│       ├── graph/
│       │   └── transaction_graph.py
│       │
│       ├── ingestion/
│       │   ├── adapters/
│       │   └── schema.py
│       │
│       ├── rules/
│       │   └── rules.py
│       │
│       ├── scoring/
│       │   ├── customer_risk.py
│       │   └── risk_score.py
│       │
│       ├── synthetic/
│       │   ├── dataset.py
│       │   ├── generator.py
│       │   ├── labels.py
│       │   └── scenarios.py
│       │
│       └── pipeline.py
|
├── tests/
│   ├── demo/
│   └── ingestion/
|
├── run_graphvex.py
├── pyproject.toml
└── .gitignore
```

## Detection approach

### Transaction features

GraphVex currently calculates two main behavioural features.

#### Transaction velocity

The pipeline counts outgoing transactions from a sender within a
configurable time window.

This is useful for identifying sudden bursts of activity that differ
from normal transaction behaviour.

#### Amount deviation

Transaction amounts are compared with the sender's historical
transaction behaviour.

A z-score is used to identify transactions that are unusually large or
small relative to the sender's normal activity.

## Rule-based detection

The current rule engine contains three transaction-level rules.

### High velocity

Flags transactions occurring when the sender has unusually high
transaction activity within the configured window.

### Unusual amount

Flags transactions where the amount deviation exceeds the configured
threshold.

### Structuring-like activity

Looks for multiple similar-value transactions from the same sender to
different recipients within a short period.

The current implementation is intentionally simple and is intended to
demonstrate the detection concept rather than reproduce the full
complexity of a production transaction monitoring system.

## Graph analysis

Transactions are represented as a directed `MultiDiGraph` using
NetworkX.

Customers are represented as nodes and individual transactions are
represented as edges.

A multi-edge graph is used so that multiple transactions between the
same pair of customers are not collapsed into a single edge.

For example:

``` text
C0010 -> C0020 -> C0030 -> C0040
   ^                         |
   |_________________________|
```

GraphVex currently uses the graph layer to detect short, time-ordered
circular fund flows.

A detected cycle must satisfy configurable limits for:

-   Maximum cycle length
-   Maximum duration
-   Amount similarity

The graph detector then marks the transactions involved in the detected
cycle.

## Risk scoring

Transaction risk is calculated using transparent, configurable weights.

  Signal                         Weight
  ---------------------------- --------
  High transaction velocity          20
  Unusual transaction amount         30
  Structuring-like activity          25
  Circular fund flow                 40

These values are demonstration weights for this project. They are not
intended to represent regulatory thresholds or production AML scoring
methodology.

At the customer level, each signal type contributes at most once to the
customer risk score.

Repeated alerts are tracked separately using `total_alerts`.

This means the system distinguishes between the type of risk signals
present and how frequently those signals occurred.

## Customer risk

Transaction-level results are aggregated into customer-level profiles.

A customer profile currently includes:

-   Number of transactions sent
-   Number of transactions received
-   Total amount sent
-   Total amount received
-   High velocity alerts
-   Unusual amount alerts
-   Structuring alerts
-   Circular flow alerts
-   Total alert count
-   Customer risk score
-   Risk level

Customers with a risk score above zero can be converted into
investigation cases.

## Investigation cases

GraphVex creates a case for each customer with detected risk signals.

A case contains:

-   Case ID
-   Customer ID
-   Customer risk score
-   Risk level
-   Total alert count
-   Number of transactions sent
-   Number of transactions received
-   Detection reasons
-   Investigation status

For example:

``` text
CASE-0001
Customer: C0020
Risk score: 70
Risk level: critical
Alert count: 2

Reasons:
Unusual transaction amounts
Circular fund flow

Status: open
```

The intention is to provide an investigator with a concise starting
point rather than simply returning a list of suspicious transaction IDs.

## Synthetic dataset

The current project uses a controlled synthetic dataset.

It contains:

-   1,016 transactions
-   100 customers
-   1,000 normal transactions
-   16 transactions belonging to injected AML scenarios

The injected scenarios are:

  Scenario               Transactions
  -------------------- --------------
  Normal                        1,000
  Structuring                       4
  Rapid movement                    3
  Circular flow                     4
  Network dispersion                5

Ground-truth labels are stored separately in `ground_truth.parquet`.

The synthetic data is reproducible and is intended to provide known
examples for testing the different components of the pipeline.

## Evaluation

Using the current synthetic dataset and treating every non-normal
scenario as suspicious, the current transaction-level evaluation
produced:

``` text
True positives : 16
False positives: 0
True negatives : 1000
False negatives: 0

Precision: 1.000
Recall:    1.000
F1 score:  1.000
```

The system also produced the following customer-level distribution:

``` text
Critical : 2
High     : 4
Medium   : 1
Low      : 93
```

There were 7 customers requiring investigation.

### Threshold analysis

The risk score can be evaluated at different alert thresholds.

    Threshold   Alerts   Precision   Recall      F1
  ----------- -------- ----------- -------- -------
            0     1016       0.016    1.000   0.031
           20       16       1.000    1.000   1.000
           25       16       1.000    1.000   1.000
           30       12       1.000    0.750   0.857
           40        9       1.000    0.562   0.720
           45        5       1.000    0.312   0.476

This demonstrates the effect of changing the risk threshold: higher
thresholds reduce the number of alerts but also reduce recall on this
dataset.

These results should be interpreted only as validation of the
implementation on controlled synthetic data. They should not be
interpreted as evidence of real-world AML detection performance.

## Running the project

### Requirements

-   Python 3.12 or compatible Python 3 version
-   Git

### Clone the repository

``` bash
git clone https://github.com/gman-sudo/GraphVex.git
cd GraphVex
```

### Create a virtual environment

On Windows:

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On Linux or macOS:

``` bash
python -m venv .venv
source .venv/bin/activate
```

### Install the project

``` bash
pip install -e .
```

### Run the demo

``` bash
python run_graphvex.py
```

The demo runs the complete pipeline and prints:

-   Number of transactions analysed
-   Number of transaction alerts
-   Number of customers analysed
-   Number of customers requiring investigation
-   Customer risk distribution
-   Investigation cases
-   Highest-risk case

Example summary:

``` text
Transactions analysed : 1016
Transaction alerts    : 16
Customers analysed    : 100
Customers requiring investigation : 7
```

## Development and tests

The repository contains the individual development checks used while
building the project under `tests/demo/`, along with the ingestion tests
under `tests/ingestion/`.

The main runnable demonstration is:

``` bash
python run_graphvex.py
```

## Design decisions

### Canonical transaction schema

GraphVex separates data ingestion from the detection pipeline.

Different transaction sources can be mapped into a common transaction
model before being processed by the rest of the system.

This keeps source-specific formatting out of the detection logic.

### Explainability

The system records the signals that caused an alert instead of returning
only a numerical score.

For example:

``` text
High transaction velocity; Structuring-like activity
```

This makes the output easier to inspect and reason about.

### Graph-based analysis

Some transaction patterns are difficult to represent using individual
transaction features alone.

Circular fund movement is an example where the relationship between
multiple accounts is important. The graph layer is therefore kept
separate from the transaction rules.

### Customer-level aggregation

Individual transaction alerts are useful, but an investigator generally
needs a view of the customer and their overall activity.

GraphVex therefore aggregates transaction signals into customer-level
risk profiles and investigation cases.

## Limitations

GraphVex is a portfolio and learning project, not a production AML
compliance platform.

The current implementation has several limitations:

-   The development and evaluation data is synthetic.
-   The detection rules are hand-crafted.
-   The risk weights are demonstration values.
-   Behavioural features are limited.
-   There is no KYC integration.
-   There is no sanctions or PEP screening.
-   There is no production case-management integration.
-   There is no investigator feedback loop.
-   There is no model governance or regulatory validation.
-   The current evaluation does not establish real-world AML
    performance.

These limitations are important because AML detection systems operating
in financial institutions require significantly more data, controls,
validation, governance, and domain-specific processes.

## Possible future work

The project could be extended with:

-   External dataset validation
-   Machine-learning anomaly detection
-   More advanced temporal graph analysis
-   Customer behavioural baselines
-   Network-level risk propagation
-   Investigator feedback
-   Case-management integration
-   API access
-   Model monitoring and governance

These are intentionally outside the current MVP.

## Technology

-   Python
-   Pandas
-   Pydantic
-   NetworkX
-   PyArrow
-   Parquet
-   Git
-   GitHub

## Project status

The current version is a completed portfolio MVP demonstrating an
end-to-end AML detection workflow from transaction ingestion through
customer investigation cases.

The project focuses on demonstrating the engineering and analytical
concepts behind an AML monitoring system rather than attempting to
reproduce a production banking platform.
