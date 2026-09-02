\# PRISM Intelligence



> \*\*AI risk intelligence for payment systems.\*\*

> PRISM detects when multiple AI decision systems are likely to fail together—before isolated model errors become payment failures.



\## The problem



Payment platforms commonly use multiple AI systems for fraud detection, risk scoring, routing, and transaction decisions. A model can look accurate individually while several models still make similar errors under the same stressful conditions. That hidden correlation creates systemic payment risk.



\## Our solution



PRISM runs adversarial stress scenarios, measures correlated failures and confidence calibration, and converts the results into a single, understandable \*\*Trust Score\*\*. When risk crosses a threshold, it raises an alert and creates an incident report with an action recommendation.



\## Core capabilities



| Capability | What PRISM does |

| --- | --- |

| Trust Field | Combines performance, calibration, and correlation into one system-level trust view. |

| Stress Test | Simulates adverse operating conditions at a selected intensity. |

| Correlation Intelligence | Detects overlapping AI model failures rather than isolated mistakes. |

| Alert Center | Classifies systemic risk as Safe, Warning, or Critical. |

| Incident Report | Exports the latest stress-test result for review or PDF saving. |



\## Product screenshots



\### 1. Adversarial scenario detection



!\[PRISM detects the highest-risk adversarial scenario](assets/red-team-adversarial-result.png)



\### 2. Incident report



!\[PRISM incident report with trust and correlation-risk metrics](assets/incident-report.png)



\## 3. PRISM analysis pipeline



```mermaid

flowchart LR

&#x20;   A\["Payment AI outputs"] --> B\["Stress simulation"]

&#x20;   B --> C\["Performance + calibration"]

&#x20;   C --> D\["Correlation analysis"]

&#x20;   D --> E\["PRISM Trust Score"]

&#x20;   E --> F\["Alert Center + report"]

```



\## 4. Risk thresholds



```mermaid

flowchart TD

&#x20;   A\["Correlation risk"] --> B{"Risk level"}

&#x20;   B -->|"Below 20%"| C\["SAFE\\nContinue monitoring"]

&#x20;   B -->|"20% – 35%"| D\["WARNING\\nReview shared features"]

&#x20;   B -->|"35% and above"| E\["CRITICAL\\nOpen incident review"]

```



\## Where AI is used



PRISM evaluates the outputs of multiple payment-decision AI models. The prototype analyses these model metrics under stress:



\- `evaluate\_models()` evaluates model performance.

\- `create\_stress\_data()` creates adversarial payment conditions.

\- `calculate\_correlated\_failures()` identifies overlapping errors across models.

\- `calculate\_calibration()` checks whether model confidence is reliable.

\- `calculate\_prism\_trust\_score()` converts the combined signals into a trust score.



> This Buildathon prototype uses simulated payment data and model outputs. The monitoring workflow is designed to connect to real payment events in production.



\## Demo flow



1\. Open the dashboard and show the Trust Score, telemetry, and trust trajectory.

2\. Set the stress slider to `1.8x` or `2.0x`.

3\. Click \*\*Run Stress Test\*\*.

4\. Explain the trust score and correlation risk in the result.

5\. Open \*\*Alert Center\*\* to show severity and recommended action.

6\. Download or save the Incident Report as a PDF.



\## Future implementation



\### Real payment-event integration



In production, PRISM can consume verified Razorpay payment webhooks. The FastAPI backend would normalise safe payment signals—such as payment status, failure reason, retry count, method category, and timestamp—before analysing them. Raw card data or API secrets should never be sent to PRISM.



\### Real anomaly-detection model



An Isolation Forest or a supervised fraud-risk model can produce an anomaly score from transaction features. This score can become another input to the PRISM Trust Score.



\### LLM Incident Analyst



A lightweight LLM can explain a computed incident in plain language:



\- Why did the alert become Critical?

\- Which metric changed most?

\- What operational action is recommended?



The LLM would \*\*explain\*\* the deterministic risk calculations; it would not approve payments or calculate the correlation risk itself.



\### Razorpay Vulcan integration



Razorpay Vulcan is described publicly as Razorpay's proprietary payments foundation model. If Razorpay provides approved partner or merchant API access in the future, PRISM can ingest its permitted output signals as one more monitored model. PRISM does not currently claim direct Vulcan integration.



\## Tech stack



\- \*\*Frontend:\*\* HTML, Tailwind CSS, JavaScript, SVG visualisation

\- \*\*Backend:\*\* FastAPI and Python

\- \*\*Analytics:\*\* model performance, calibration, stress simulation, correlated-failure analysis



\## Local integration requirements



The frontend expects a FastAPI service at `http://127.0.0.1:8000` with these endpoints:



```text

GET /dashboard

GET /stress-test?stress\_level=<number>

GET /red-team

GET /correlation-intelligence

GET /trust-history

```



Enable CORS for the frontend origin during local development.

