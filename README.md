# Ground Risk

## Deep research prompt

### Agent-driven, domain-agnostic risk aggregation model

Act as an interdisciplinary research team spanning risk theory, probability and statistics, operations research, actuarial science, systems safety, network science, artificial intelligence, agentic systems, and information-system architecture.

### Objective

Determine which academically grounded theoretical approach—or defensible combination of approaches—is best suited to a domain-agnostic risk aggregation system that:

- Ingests very large numbers of individual risk elements.
- Produces aggregated probability and loss distributions rather than only scores, ratings, or risk matrices.
- Preserves tail behaviour, dependencies, and material uncertainty.
- Models statistical dependence, common causes, causal chains, conditional dependencies, contagion, feedback, cascading failures, and dependencies that change over time.
- Represents random variability in events and losses.
- Remains robust when observations are sparse or missing.
- Supports explainability, auditability, large-scale computation, and real-time or incremental updates.
- Operates through a hybrid batch-and-streaming architecture.
- Can be configured for different domains without changing its mathematical foundations.
- Uses AI and LLM-based agents to automate suitable parts of the traditionally manual risk-management lifecycle.

The research must culminate in:

1. Selection of a preferred risk-modelling approach or mathematically coherent hybrid.
2. Identification of where AI agents and LLMs can reliably reduce manual effort.
3. Definition of the boundary between agentic reasoning and authoritative probabilistic computation.
4. A prototype-ready system specification integrating the risk model, probabilistic engines, data pipelines, and governed AI agents.

Do not assume in advance that either a single risk theory or an LLM-centric solution will satisfy all requirements.

### Central research question

Which combination of risk theory, probabilistic computation, data architecture, and governed agentic inference offers the strongest foundation for large-scale, dynamic, distribution-preserving risk aggregation?

### Supporting AI research question

Where can LLMs and AI agents provide reliable, measurable value in generating, populating, updating, interrogating, and governing a risk model—and where must deterministic, statistical, causal, or human-controlled methods remain authoritative?

### Terminology

Clearly distinguish:

- **Probabilistic inference:** mathematically defined estimation or updating within a statistical model.
- **Agentic inference:** an AI agent's evidence-based reasoning, hypothesis generation, tool selection, and workflow decisions.
- **Accepted model state:** validated information that has passed the applicable technical and governance controls.
- **Candidate model state:** AI-generated or newly observed information awaiting validation.
- **Aggregate risk:** a joint probability and loss distribution, not merely a weighted score.

Do not use “inference” ambiguously.

### Working definition of a risk element

Treat an individual risk element as a versioned representation of a potential event, condition, or process containing:

- An occurrence model or probability distribution.
- A conditional loss or consequence distribution.
- A defined time horizon.
- Exposure and contextual attributes.
- Relationships to other risks, causes, controls, common factors, and system components.
- Supporting observations, documents, assumptions, and evidence.
- Provenance, confidence, validation status, and timestamps.
- The identity of the human, algorithm, or AI agent that proposed or changed it.

Treat aggregation as the mathematically justified composition of risk elements into a portfolio-, subsystem-, or system-level joint loss distribution.

Address how aggregation works when consequences are not naturally commensurable. Compare scalar, vector-valued, and multi-attribute loss representations. Do not assume that unlike harms can simply be added.

## Research tasks

### 1. Establish the conceptual foundation

Clarify, with citations:

- Risk, uncertainty, hazard, exposure, probability, consequence, and loss.
- Marginal, conditional, and joint distributions.
- Statistical dependence versus causal dependence.
- Aleatory variability versus uncertainty introduced by sparse or missing observations.
- Aggregation of distributions versus summarisation using expected loss, VaR, expected shortfall, or other metrics.
- Additive versus non-additive losses.
- Static, time-varying, cascading, and feedback-driven risks.
- Conditions under which aggregation is mathematically meaningful.
- Double counting caused by overlapping events, shared causes, hierarchical risks, duplicated evidence, or AI-generated duplicates.

### 2. Develop a taxonomy of risk-modelling approaches

At minimum, investigate:

- Classical probability aggregation, convolution, compound-loss models, and Monte Carlo simulation.
- Multivariate distributions, copulas, vine copulas, latent-factor models, and tail-dependence models.
- Bayesian hierarchical models, Bayesian networks, dynamic Bayesian networks, and probabilistic graphical models.
- Reliability and systems-safety methods, including fault trees, event trees, influence diagrams, and stochastic Petri nets.
- Stochastic processes, marked point processes, and self-exciting processes.
- Network, cascade, contagion, and systemic-risk models.
- Extreme-value theory.
- Agent-based, system-dynamics, and discrete-event simulation.
- Imprecise probability, evidence theory, possibility theory, and fuzzy methods where relevant to sparse evidence.
- Coherent and convex risk measures, distortion measures, expected shortfall, and related portfolio-risk concepts.
- Probabilistic programming and modern probabilistic machine learning.

Classify each approach according to whether it supplies:

- Risk representation.
- Dependence representation.
- Temporal or causal modelling.
- Aggregation computation.
- Parameter estimation or probabilistic inference.
- Simulation.
- Post-aggregation summary measures.

Do not compare approaches as substitutes if they solve different layers of the problem.

### 3. Investigate AI and LLM-supported risk modelling

Review academic and credible technical evidence for using LLMs, knowledge graphs, retrieval-augmented generation, tool-using agents, and multi-step agentic workflows in risk management and adjacent fields.

Evaluate AI assistance across the following activities:

#### Risk discovery and model population

- Extracting candidate risks, events, causes, consequences, controls, and indicators from documents, databases, messages, reports, incident records, and data streams.
- Mapping domain language into a canonical risk ontology.
- Identifying duplicate, overlapping, nested, or contradictory risk descriptions.
- Classifying risks and associating them with assets, processes, objectives, exposures, and controls.
- Proposing causal, conditional, common-factor, or dependency relationships.
- Building candidate knowledge graphs from structured and unstructured evidence.
- Detecting previously unmodelled risks or changes in known risks.

#### Model estimation and maintenance

- Retrieving relevant evidence for probability and loss models.
- Suggesting candidate distributions, priors, scenarios, or parameter ranges.
- Recognising sparse or missing information.
- Distinguishing missing observations from true zero values.
- Detecting when evidence may invalidate an existing assumption.
- Monitoring external or internal signals for changes to risks and dependencies.
- Initiating recalculation when relevant evidence changes.
- Proposing updates while preserving version history.
- Identifying stale, unsupported, or weakly evidenced model components.

Treat any LLM-generated distribution, parameter, probability, or causal relationship as a hypothesis unless validated through data, a formal method, or an authorised human decision.

#### Scenario and cascade analysis

- Generating plausible scenarios and counterfactuals.
- Identifying potential causal chains, feedback mechanisms, and cascade pathways.
- Translating scenarios into structured inputs for simulation.
- Calling causal, probabilistic, network, or simulation engines.
- Comparing scenario outcomes and identifying sensitive assumptions.
- Searching for overlooked combinations of events without presenting imaginative plausibility as statistical likelihood.

#### Explanation and interaction

- Translating natural-language questions into risk-model queries.
- Explaining aggregate results and changes in distributions.
- Producing contribution, attribution, and sensitivity narratives.
- Tracing an aggregate result back to source risks, evidence, assumptions, and model versions.
- Generating review packages for subject-matter experts.
- Supporting conversational exploration without changing accepted model state unless authorised.

#### Workflow orchestration

- Selecting appropriate validated tools for extraction, estimation, simulation, validation, and aggregation.
- Coordinating multi-stage risk-assessment workflows.
- Routing uncertain or high-impact proposals for review.
- Triggering batch or streaming recomputation.
- Monitoring jobs and responding to validation failures.
- Maintaining an auditable record of observations, reasoning steps, tool calls, proposed changes, approvals, and resulting model updates.

### 4. Define the correct boundary for agentic autonomy

Compare at least the following operating models:

1. **AI copilot:** generates recommendations but cannot change model state.
2. **Bounded agent:** can make low-impact changes that pass deterministic validation rules.
3. **Supervised agent:** can execute broader workflows with approval at defined checkpoints.
4. **Autonomous agent:** can update and operate the model within formally specified policies and limits.

Recommend an appropriate automation level for each risk-management activity.

Define escalation criteria based on factors such as:

- Expected impact on the aggregate distribution.
- Evidence quality.
- Model confidence.
- Novelty of the proposed risk or relationship.
- Irreversibility.
- Regulatory or governance significance.
- Disagreement among models, agents, data, or human reviewers.
- Detection of out-of-distribution conditions.

Investigate whether agentic AI should be treated as:

- An interface to the risk model.
- A model-building assistant.
- A continuous model-maintenance mechanism.
- A workflow orchestrator.
- A source of candidate hypotheses.
- A probabilistic estimator.
- An autonomous decision-maker.

Provide evidence-based conclusions for each role.

### 5. Evaluate theoretical strength

For every material risk-modelling approach, assess:

- Mathematical assumptions and axioms.
- Ability to produce a full aggregate distribution.
- Nonlinear and tail dependence.
- Common causes and latent factors.
- Causal chains, feedback, contagion, and cascades.
- Time-varying dependencies.
- Sparse and missing observations.
- Decomposability and risk attribution.
- Susceptibility to double counting.
- Calibration, validation, and identifiability.
- Data requirements and sensitivity to misspecification.
- Evidence of successful cross-domain use.
- Known failure modes.

### 6. Evaluate information-system feasibility

Assess:

- Required data and relationship schemas.
- Computational and memory complexity.
- Parallelisation and partitioning.
- Distributed batch computation.
- Incremental recomputation.
- Streaming and low-latency updating.
- Late, duplicated, corrected, or out-of-order events.
- Storage of distributions, simulations, graphs, and lineage.
- Explanation and attribution.
- Reproducibility and deterministic replay.
- Model and prompt versioning.
- Domain configurability.
- Numerical stability and approximation error.
- Operational monitoring.
- Security and privacy.

Where exact real-time aggregation is infeasible, investigate principled approximation, caching, surrogate models, or staged reconciliation. State what accuracy or consistency is sacrificed.

### 7. Evaluate AI feasibility and risk

Assess agentic approaches using measurable criteria, including:

- Extraction precision and recall.
- Ontology-mapping accuracy.
- Duplicate-detection accuracy.
- Accuracy of proposed dependencies and causal relationships.
- Evidence-citation correctness.
- Unsupported-claim and hallucination rates.
- Calibration of expressed confidence.
- Human acceptance, correction, and reversal rates.
- Effect of AI errors on the final aggregate distribution.
- Labour and elapsed-time reduction.
- Latency, throughput, and computational cost.
- Reproducibility across repeated runs.
- Performance under domain shift.
- Reliability when evidence is incomplete or contradictory.

Include the following failure and threat modes:

- Hallucinated risks, evidence, parameters, or causal links.
- Automation bias.
- Prompt injection and malicious documents.
- Data or knowledge-base poisoning.
- Unauthorised model changes.
- Feedback loops in which AI-generated content becomes evidence for later AI outputs.
- Loss of provenance.
- Confidential-data leakage.
- Model drift.
- Non-determinism.
- Tool misuse.
- Excessive reliance on fluent explanations.
- Failure to distinguish an absent observation from evidence of absence.

Specify mitigations such as structured outputs, constrained schemas, evidence grounding, deterministic validators, policy engines, access controls, confidence thresholds, sandboxed tools, approval gates, evaluation suites, and rollback.

### 8. Conduct a transparent comparison

Create a comparison matrix covering academic validity, implementation potential, and compatibility with agentic operation.

Treat these as dominant implementation criteria:

- Explainability and auditability.
- Scalability.
- Real-time or incremental updating.
- Robustness to sparse or missing data.
- Safe and effective use by AI agents.

Treat full distribution preservation and required dependency support as threshold requirements.

Define scoring anchors before assigning scores. Use Pareto and sensitivity analysis rather than relying only on an arbitrarily weighted total.

### 9. Select the preferred model

Recommend one primary approach or a mathematically coherent modular hybrid.

For a hybrid, specify which foundation governs:

- Risk-element semantics.
- Probability and loss representation.
- Dependence and common-factor modelling.
- Causal and temporal relationships.
- Cascade and contagion dynamics.
- Aggregation.
- Incremental approximation.
- Attribution and explanation.
- AI-generated candidate changes.
- Validation and acceptance into authoritative model state.

Demonstrate that the components are semantically and mathematically compatible.

### 10. Produce a prototype-ready architecture

Specify a technology-neutral hybrid batch-and-streaming architecture containing, where justified:

- Evidence and event connectors.
- Structured and unstructured ingestion.
- Retrieval and knowledge services.
- Risk ontology and entity-resolution service.
- AI agent runtime and orchestration layer.
- Tool and policy registry.
- Candidate-model workspace isolated from accepted model state.
- Evidence, provenance, and confidence store.
- Deterministic schema and policy validation.
- Human review and approval workflow.
- Authoritative risk-element registry.
- Distribution and parameter store.
- Dependency, causal, factor, or knowledge graph.
- Batch aggregation engine.
- Streaming and incremental-update engine.
- Simulation and probabilistic-inference services.
- Materialised aggregate store and cache.
- Explanation, attribution, and lineage services.
- APIs and conversational query interface.
- Model, prompt, agent, and tool version registry.
- Monitoring, evaluation, rollback, and audit services.

The LLM should use validated statistical, simulation, database, and calculation tools rather than performing complex probability calculations through free-form text generation.

### 11. Define the agentic model-update lifecycle

Design a controlled lifecycle such as:

1. Observe new evidence or receive a task.
2. Retrieve relevant model context and source material.
3. Extract structured candidate claims.
4. Attach evidence, provenance, timestamps, and confidence.
5. Validate schemas and ontology mappings.
6. Detect duplication, conflict, and possible double counting.
7. Propose risks, relationships, scenarios, or parameter updates.
8. Invoke authoritative probabilistic or simulation tools.
9. Measure the proposed change's effect on aggregate distributions.
10. Apply policy and materiality gates.
11. Commit an authorised change or route it for review.
12. Recompute affected aggregates.
13. Generate an evidence-linked explanation.
14. Monitor consequences and support rollback.

Provide pseudocode, state transitions, failure handling, and audit requirements for this lifecycle.

### 12. Provide implementation artefacts

Include:

- Logical entity and relationship model.
- Component responsibilities and data flows.
- Batch, streaming, and agentic processing sequences.
- Pseudocode for full aggregation and incremental updates.
- Agent tool contracts and structured output schemas.
- Example API operations or messages.
- Complexity estimates.
- Consistency and reconciliation strategy.
- Versioning and deterministic-replay requirements.
- Human-approval and policy-gate design.
- Minimum viable prototype scope.
- Phased implementation roadmap.
- Benchmark and evaluation plan.

Include a small domain-neutral example involving:

- Correlated risks.
- A shared cause.
- A causal cascade.
- A missing observation.
- A new document or event detected by an AI agent.
- An AI-proposed model update.
- Validation or human approval.
- Incremental recalculation of the aggregate loss distribution.
- A traceable explanation of what changed and why.

## Research method

Use a structured search across probability and statistics, actuarial science, quantitative finance, operations research, reliability engineering, safety science, network science, information systems, natural-language processing, knowledge graphs, probabilistic programming, human–AI interaction, and agentic systems.

Prioritise:

- Seminal primary works.
- Peer-reviewed research.
- Systematic reviews.
- Authoritative textbooks.
- Relevant technical standards.
- Recent evidence through August 2026.

Because agentic AI is an emerging field, clearly distinguish peer-reviewed evidence from preprints, demonstrations, vendor claims, and reasoned design proposals.

For each important claim:

- Provide an inline citation.
- Include a DOI or stable link where possible.
- State whether the evidence is theoretical, empirical, simulation-based, or inferred.
- Do not invent citations.

Document the search strategy, sources searched, representative search terms, inclusion and exclusion criteria, and important evidence gaps.

## Required report structure

1. Executive conclusion.
2. Definitions, assumptions, and research questions.
3. Research method and evidence assessment.
4. Taxonomy of risk-modelling theories.
5. Academic evaluation.
6. Information-system feasibility.
7. Taxonomy of AI and agentic roles.
8. Evidence for and against each AI role.
9. Risk, governance, and autonomy analysis.
10. Comparative matrices and sensitivity analysis.
11. Recommended mathematical and agentic model.
12. Prototype-ready reference architecture.
13. Data model, APIs, algorithms, and agent workflows.
14. Worked example.
15. Validation and benchmarking strategy.
16. Governance, security, audit, and rollback.
17. Implementation roadmap.
18. Research gaps and unresolved questions.
19. Complete bibliography.

## Quality controls

Do not:

- Treat a risk matrix or ordinal score as a full distribution.
- Assume independence because dependence data is unavailable.
- Confuse correlation, causal association, and LLM-generated plausibility.
- Collapse tail behaviour into expected loss.
- Combine unlike losses without an explicit rule.
- Hide missing data through silent imputation.
- Allow LLM output to enter accepted model state without appropriate validation.
- Let the LLM perform calculations better handled by validated computational tools.
- Treat generated scenarios as evidence of their probability.
- Allow AI-generated content to recursively validate itself.
- Recommend opaque AI solely because it scales.
- Claim that human oversight has been eliminated unless evidence supports safe autonomous operation.

If the evidence does not support a universal solution, recommend a modular architecture with an explicit mathematical core, an isolated candidate-model layer, governed agentic workflows, and risk-based human approval.
