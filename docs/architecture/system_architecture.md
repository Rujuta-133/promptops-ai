# System Architecture

## 1. Purpose

This document defines the system architecture of PromptOps AI, including its major components, responsibilities, interactions, governance mechanisms, evaluation workflows, diagnostic capabilities, and deployment boundaries.

It serves as the architectural reference for implementation. Decisions that require further discussion or validation are documented under the To Be Reviewed section.

## 2. Architectural Overview

PromptOps AI is a domain-agnostic Prompt Governance, Evaluation, and Observability Platform.

The initial implementation focuses on Retrieval-Augmented Generation (RAG) applications and provides its own runtime for executing RAG workflows, managing prompts, evaluating outputs, and capturing application behaviour.

The platform combines deterministic services, orchestrated workflows, and specialized agents where reasoning provides measurable value.

Governance, evaluation, and interpretability are foundational principles across the architecture.

### 2.1 Architectural Principles

The architecture follows these principles:

* Independent deployment and operation.
* Clear component responsibilities and boundaries.
* Business-driven and configurable evaluation.
* Deterministic enforcement of mandatory governance controls.
* Evidence-based diagnostics and recommendations.
* Traceability across prompts, executions, evaluations, and changes.
* Human oversight where required by policy.
* Incremental implementation and avoidance of premature abstraction.

### 2.2 High-Level Component Model

The logical architecture consists of the following components:

1. Prompt Management and Registry.
2. RAG Runtime and Orchestration.
3. Context Construction and Retrieval.
4. Model Invocation and Inference Configuration.
5. Evaluation Engine.
6. Governance and Lifecycle Management.
7. Observability and Trace Management.
8. Diagnostic and Incident Knowledge System.
9. Improvement and Optimization System.
10. Agent Orchestration.
11. Supporting Persistence and Integration Interfaces.

These are logical responsibilities, not necessarily separate deployable services. Related components may initially be grouped within a modular application.

## 3. Component Responsibilities

### 3.1 Prompt Management and Registry

The Prompt Registry manages prompt definitions, versions, metadata, and lifecycle information.

Responsibilities include:

* Registering prompts.
* Maintaining traceable prompt versions.
* Recording version metadata and change history.
* Retrieving the applicable prompt version for execution.
* Comparing prompt versions.
* Associating prompt versions with evaluation results and deployments.

Prompt registration and version management use deterministic service logic.

The registry does not independently approve changes or bypass governance requirements.

### 3.2 RAG Runtime and Orchestration

The RAG Runtime executes the initial application workflow.

Responsibilities include:

* Receiving an application request.
* Identifying the applicable workflow and prompt version.
* Retrieving relevant information.
* Constructing model context.
* Invoking the configured model.
* Applying configured output validation and error handling.
* Returning the result.
* Emitting execution and evaluation events.

The runtime coordinates modular operations rather than embedding every responsibility in one indivisible component.

### 3.3 Context Construction and Retrieval

This component prepares the information supplied to the model.

Responsibilities include:

* Retrieving relevant documents.
* Applying configured retrieval and filtering strategies.
* Constructing context from retrieved information and applicable conversation history.
* Managing context ordering and token constraints.
* Capturing relevant context metadata for diagnostics and evaluation.
* Supporting investigation of retrieval and context-quality problems.

Context engineering focuses on measurable improvements to the information supplied to the model, not merely prompt formatting.

### 3.4 Model Invocation and Inference Configuration

This component manages model execution within the runtime.

Responsibilities include:

* Invoking the configured model provider.
* Applying model and generation settings.
* Capturing token usage and execution latency where available.
* Recording provider errors and invocation outcomes.
* Supporting model configuration comparisons and cost analysis.

Inference engineering focuses on trade-offs among quality, latency, throughput, reliability, and cost.

Provider-specific implementation details should remain behind suitable interfaces where abstraction provides practical value.

### 3.5 Evaluation Engine

The Evaluation Engine measures application behaviour against configured evaluation criteria.

Responsibilities include:

* Running evaluations against defined datasets.
* Applying application-specific evaluation metrics.
* Comparing prompt versions and candidate changes.
* Detecting regressions against configured thresholds.
* Recording evaluation results and supporting evidence.
* Producing structured results for governance and diagnostics.

Potential evaluation dimensions include correctness, faithfulness, relevance, completeness, consistency, regression rate, latency, token consumption, cost, and reliability.

Applicable metrics and acceptance thresholds depend on the application's requirements.

Evaluation results provide evidence for decisions; they do not independently authorize production deployment.

### 3.6 Governance and Lifecycle Management

The Governance component controls permitted actions and lifecycle transitions.

Responsibilities include:

* Enforcing role-based access control.
* Applying governance policies.
* Enforcing approval requirements.
* Enforcing separation of duties.
* Controlling prompt promotion and rollback.
* Recording approval and lifecycle events.
* Maintaining auditability of governed operations.

Governance enforcement must be deterministic.

Agents may recommend actions but cannot bypass authorization checks, mandatory approval gates, or applicable policies.

### 3.7 Observability and Trace Management

Observability captures information needed to understand application behaviour and investigate failures.

Responsibilities include:

* Recording execution traces and relevant events.
* Associating traces with prompt versions and execution configuration.
* Capturing retrieval, model invocation, and output-handling information where appropriate.
* Recording latency, token usage, cost estimates, and errors where available.
* Associating evaluation outcomes with relevant executions.
* Supporting trace inspection and historical comparisons.

Sensitive information must be handled according to the platform's security and data-protection requirements.

### 3.8 Diagnostic and Incident Knowledge System

This component investigates failures using execution evidence, evaluation results, and relevant historical incidents.

Responsibilities include:

* Identifying affected components and observed symptoms.
* Generating plausible diagnostic hypotheses.
* Presenting evidence supporting or contradicting each hypothesis.
* Communicating uncertainty.
* Recommending further investigation.
* Recording investigation outcomes and verified root causes.
* Retrieving potentially relevant historical incidents.

Historical similarity must not be treated as proof of a shared root cause.

Diagnostic records distinguish observations, hypotheses, and verified findings.

### 3.9 Improvement and Optimization System

This component supports the investigation, generation, and evaluation of candidate changes.

Responsibilities include:

* Accepting engineer-initiated improvement requests.
* Assessing whether sufficient evidence exists to proceed.
* Identifying relevant prompts, context construction, model configuration, execution workflows, or caching behaviour.
* Generating candidate changes where appropriate.
* Evaluating candidates against configured datasets and acceptance criteria.
* Comparing quality, latency, cost, and other relevant trade-offs.
* Presenting evidence and recommendations to responsible engineers.

An improvement request does not automatically authorize implementation or production promotion.

Resource-intensive improvement cycles are initially engineer-initiated. Monitoring, feedback collection, alerting, and configured safety responses continue independently.

## 4. Agentic Architecture

This section defines the proposed agents and their responsibilities. It distinguishes agent-based reasoning from deterministic services and coordinated workflows.

The agents listed here describe the intended architectural direction. Their final boundaries, implementation strategy, and inclusion in the initial release remain subject to review.

### 4.1 Evaluation Agent

**Primary responsibility:** Interpret evaluation results and help engineers understand application quality.

Potential capabilities:

* Analyze evaluation results across prompt versions.
* Identify quality changes and potential regressions.
* Explain performance against configured acceptance criteria.
* Compare quality, latency, cost, and other relevant metrics.
* Identify evaluation gaps and potentially missing test cases.
* Summarize evidence for engineering review.

**Dependencies:**

* Evaluation Engine.
* Evaluation datasets and configurations.
* Prompt Registry.
* Observability and Trace Management.

**Boundaries:**

* Does not invent evaluation results.
* Does not change acceptance criteria without authorization.
* Does not independently approve production promotion.
* Must distinguish measured results from inferred explanations.

### 4.2 Regression Analysis Agent

**Primary responsibility:** Investigate regressions and identify plausible causes.

Potential capabilities:

* Analyze changes in evaluation results.
* Compare affected prompt versions and execution configurations.
* Identify which quality dimensions deteriorated.
* Correlate regressions with relevant traces and changes.
* Generate and rank possible causes using available evidence.
* Recommend additional investigations.

**Dependencies:**

* Evaluation Engine.
* Prompt Registry.
* Observability and Trace Management.
* Diagnostic Agent.

**Boundaries:**

* Does not assume that every regression originates in the prompt.
* Does not present an unverified hypothesis as a confirmed root cause.
* Does not independently initiate production rollback unless a separately authorized deterministic policy permits the action.

### 4.3 Diagnostic Agent

**Primary responsibility:** Investigate application failures across relevant system components.

Potential capabilities:

* Synthesize evidence from traces, evaluations, configuration, and change history.
* Generate multiple plausible root-cause hypotheses.
* Explain evidence supporting or contradicting each hypothesis.
* Communicate uncertainty and identify missing evidence.
* Recommend investigative steps.
* Retrieve potentially relevant historical incidents.
* Summarize findings for human verification.

Relevant investigation areas include prompts, retrieval, context construction, model configuration, execution workflows, output validation, and caching.

**Dependencies:**

* Observability and Trace Management.
* Evaluation Engine.
* Prompt Registry.
* Context Construction and Retrieval.
* Model Invocation and Inference Configuration.
* Harness-related execution components.
* Incident Knowledge Store.

**Boundaries:**

* Similarity to a historical incident does not establish a shared root cause.
* Unverified findings must not become trusted diagnostic knowledge.
* Human verification must follow the authorized process.
* Insufficient evidence must be reported explicitly.

### 4.4 Prompt Optimization Agent

**Primary responsibility:** Generate candidate prompt improvements based on identified problems and available evidence.

Potential capabilities:

* Analyze an existing prompt and its intended behaviour.
* Use verified findings and evaluation evidence to identify improvement opportunities.
* Generate alternative prompt versions.
* Explain the intended effect of each change.
* Identify potential trade-offs and risks.
* Submit candidates to the Evaluation Engine for testing.

**Dependencies:**

* Prompt Registry.
* Evaluation Engine.
* Diagnostic capabilities.
* Governance policies.
* Relevant application requirements.

**Boundaries:**

* Cannot assume that a generated prompt is better than the current version.
* Cannot approve or promote its own changes.
* Must not bypass evaluation or mandatory governance controls.
* Must provide candidates for evaluation rather than treating generation as proof of improvement.

### 4.5 Context Engineering Agent

**Primary responsibility:** Investigate and propose improvements to the information supplied to the model.

Potential capabilities:

* Analyze retrieval results and context composition.
* Investigate missing, irrelevant, redundant, or poorly ordered information.
* Examine context selection and token utilization.
* Identify possible retrieval and context-construction problems.
* Propose context-engineering changes.
* Evaluate whether proposed changes improve relevant quality metrics.

**Dependencies:**

* Context Construction and Retrieval.
* Observability and Trace Management.
* Evaluation Engine.
* Diagnostic capabilities.

**Boundaries:**

* Must distinguish retrieval problems from context-assembly problems where evidence allows.
* Must not assume that adding more context necessarily improves quality.
* Proposed changes must be evaluated against application-specific requirements.

### 4.6 Harness Analysis Agent

**Primary responsibility:** Investigate execution workflows and the systems surrounding model calls.

Potential capabilities:

* Analyze output-validation failures.
* Investigate retry behaviour and error handling.
* Examine workflow sequencing and execution failures.
* Identify reliability risks in tool or component interactions.
* Propose improvements to execution control and failure handling.
* Evaluate the impact of candidate changes on reliability and latency.

**Dependencies:**

* RAG Runtime and Orchestration.
* Observability and Trace Management.
* Evaluation Engine.
* Diagnostic capabilities.

**Boundaries:**

* Must not bypass execution safeguards or governance checks.
* Must account for the risk of duplicated side effects when recommending retries.
* Proposed changes must be tested against relevant failure scenarios.

### 4.7 Inference Optimization Agent

**Primary responsibility:** Investigate model execution and recommend improvements to inference configuration.

Potential capabilities:

* Compare model choices and configurations.
* Analyze latency, throughput, token usage, and cost.
* Investigate model-related quality or reliability changes.
* Identify candidate configuration changes.
* Explain trade-offs among quality, performance, and cost.
* Submit candidates for evaluation.

**Dependencies:**

* Model Invocation and Inference Configuration.
* Evaluation Engine.
* Observability and Trace Management.
* Diagnostic capabilities.

**Boundaries:**

* Must respect application requirements and configured constraints.
* Must not optimize cost or latency at the expense of mandatory quality or safety requirements.
* Model or configuration changes must be evaluated before promotion.

### 4.8 Cache Analysis Agent

**Primary responsibility:** Investigate caching behaviour and propose improvements where caching is appropriate.

Potential capabilities:

* Analyze cache hit rates and effectiveness.
* Investigate cache invalidation and freshness problems.
* Identify potential opportunities to reduce latency and model costs.
* Investigate correctness risks associated with cached results.
* Recommend cache policy or configuration changes.
* Evaluate the effect of candidate changes on correctness, latency, and cost.

**Dependencies:**

* RAG Runtime and Orchestration.
* Observability and Trace Management.
* Evaluation Engine.
* Relevant cache implementation and metadata.

**Boundaries:**

* Must not prioritize cache hit rate over correctness.
* Must account for data freshness and invalidation requirements.
* Proposed changes must be evaluated for their effects on application behaviour.

### 4.9 Governance Analysis Agent

**Primary responsibility:** Assist engineers in understanding governance state, compliance with configured policies, and the evidence required for lifecycle decisions.

Potential capabilities:

* Summarize applicable governance requirements.
* Identify missing approvals or required evaluation evidence.
* Explain why a proposed lifecycle transition does not satisfy policy.
* Summarize approval history and audit evidence.
* Identify potential governance gaps for human review.

**Dependencies:**

* Governance and Lifecycle Management.
* Evaluation Engine.
* Prompt Registry.
* Audit Records.

**Boundaries:**

* Authorization and policy enforcement remain deterministic.
* The agent cannot grant permissions or bypass approval requirements.
* The agent cannot approve its own proposed changes.
* Any recommended action must pass the applicable deterministic controls.

## 5. Agent Orchestration and Interaction

### 5.1 Orchestration Principles

Agent orchestration coordinates investigations and improvement workflows.

It should:

* Select agents according to the problem being investigated.
* Provide each agent with the relevant evidence and authorized tools.
* Maintain traceability across agent requests and results.
* Track workflow state and failures.
* Validate agent outputs before downstream use where necessary.
* Respect governance policies and permission boundaries.
* Avoid invoking every agent for every request.

Not every multi-step workflow requires autonomous agent orchestration. Deterministic workflows should be preferred when they provide sufficient capability.

### 5.2 Example: Regression Investigation

When a regression is detected:

1. The Evaluation Engine identifies a regression against configured criteria.
2. The Regression Analysis Agent examines the affected metrics and relevant changes.
3. The Diagnostic Agent investigates plausible causes using traces and execution evidence.
4. If the evidence suggests a context problem, the Context Engineering Agent may investigate retrieval and context construction.
5. If the evidence suggests a model configuration problem, the Inference Optimization Agent may investigate model behaviour and operational trade-offs.
6. Relevant findings are consolidated into an evidence-based diagnostic report.
7. The engineer reviews the findings and decides on further action, subject to applicable governance policies.

Only relevant agents are invoked. This example does not require every agent to participate in every regression investigation.

### 5.3 Example: Prompt Improvement

1. An engineer initiates an improvement request.
2. The platform assesses available evidence.
3. Relevant diagnostic capabilities investigate the problem.
4. The Prompt Optimization Agent generates candidate changes when appropriate.
5. The Evaluation Engine tests the candidates.
6. The Evaluation Agent summarizes measured results and trade-offs.
7. The engineer reviews the evidence.
8. Governance and lifecycle services enforce applicable approval and promotion requirements.

The Prompt Optimization Agent cannot approve or promote its own candidate.

### 5.4 Agent Failure and Uncertainty

If an agent fails, produces insufficient evidence, or cannot distinguish between plausible causes, the workflow should record the failure or uncertainty and provide an appropriate status.

The system must not fabricate missing evidence or automatically treat an unsupported hypothesis as verified.

Where human investigation is necessary, the workflow should make that requirement explicit.

## 6. Core Workflows

### 6.1 RAG Execution Workflow

1. Receive an application request.
2. Resolve the applicable workflow and prompt version.
3. Retrieve relevant information.
4. Construct the model context.
5. Invoke the configured model.
6. Apply configured output validation and error handling.
7. Return the result.
8. Record relevant execution traces and metadata.
9. Run configured evaluations where required.
10. Associate evaluation results with the relevant prompt version and execution.

### 6.2 Prompt Evaluation Workflow

1. Select the prompt version or candidate to evaluate.
2. Load the applicable evaluation dataset and configuration.
3. Execute the required test cases.
4. Calculate configured evaluation metrics.
5. Compare results against acceptance criteria and relevant baselines.
6. Record results and supporting evidence.
7. Identify regressions and relevant trade-offs.
8. Use the Evaluation Agent to interpret results where appropriate.
9. Present findings for engineering review.

### 6.3 Promotion Workflow

1. Identify the candidate prompt version.
2. Validate applicable governance requirements.
3. Check required evaluation results and acceptance criteria.
4. Compare the candidate against the current production version where required.
5. Check critical regressions and configured operational constraints.
6. Obtain independent human approval where required.
7. Record the promotion decision and supporting evidence.
8. Promote the candidate only if all mandatory conditions are satisfied.

Passing evaluation does not automatically establish production readiness.

### 6.4 Production Monitoring and Rollback Workflow

1. Capture relevant production execution data.
2. Compare observed behaviour with configured monitoring thresholds.
3. Detect significant regressions or operational failures.
4. Generate alerts and diagnostic information.
5. Apply configured incident-response and safety policies.
6. Execute automated rollback only when explicitly authorized by policy.
7. Support authorized human-initiated rollback.
8. Record the event, decision, and resulting system state.

Critical incidents follow their applicable response policies without waiting for routine improvement activities.

### 6.5 Diagnostic Workflow

1. Identify the affected application behaviour and observed symptoms.
2. Gather relevant traces, evaluation results, configuration, and change history.
3. Generate plausible hypotheses across relevant components.
4. Present supporting evidence, uncertainty, and recommended investigative steps.
5. Compare potentially relevant historical incidents.
6. Obtain further evidence or human investigation when necessary.
7. Record the investigation outcome.
8. Mark a root cause as verified only after the authorized verification process.

### 6.6 Improvement Workflow

1. An engineer initiates an improvement request.
2. PromptOps AI assesses the request and available evidence.
3. The request proceeds when sufficient evidence exists or is deferred when additional evidence is needed.
4. Deferrals follow the applicable approval policy.
5. A rejected deferral returns the request for further investigation.
6. Critical production issues follow the relevant incident-response policies.
7. Relevant agents generate or analyze candidate changes where appropriate.
8. Candidates are evaluated independently.
9. Results, evidence, and trade-offs are presented to the responsible engineer.
10. Governance and approval requirements determine whether a candidate may proceed toward deployment.

An unsuccessful candidate may be revised and retested or rejected.

## 7. Governance and Security

Governance and security are cross-cutting concerns.

### 7.1 Role-Based Access Control

The platform will use configurable roles and permissions to control actions such as prompt modification, evaluation, approval, production promotion, rollback, and audit review.

The precise role catalogue and permission matrix will be defined during implementation design.

### 7.2 Separation of Duties

Where independent approval is required, the proposer and approver must be different authorized individuals.

The rule must be enforced in backend authorization and lifecycle logic rather than relying on the interface alone.

### 7.3 Policy-Driven Automation

The platform may support both mandatory human approval and explicitly authorized automated operations.

Automation must not disable essential authorization, auditability, or policy enforcement.

### 7.4 Auditability

Governed actions should record relevant information, including:

* Actor or authorized automation identity.
* Action performed.
* Relevant prompt or configuration version.
* Applicable policy and approval outcomes.
* Evaluation evidence where required.
* Timestamp and resulting lifecycle state.

### 7.5 Production Safety

Production promotion and rollback must respect configured policies, authorization requirements, and operational safeguards.

The architecture distinguishes ordinary improvement activities from critical incident response.

## 8. Evaluation and Interpretability

Evaluation and interpretability work together.

Evaluation determines what the available evidence supports. Interpretability helps engineers understand why results differ and where uncertainty remains.

The platform should support:

* Configurable metrics and thresholds.
* Repeatable evaluation datasets.
* Comparisons against relevant baselines.
* Regression detection.
* Evidence-backed diagnostic findings.
* Explicit representation of uncertainty.
* Traceability between changes and outcomes.
* Explanations of quality, latency, cost, and reliability trade-offs.

Agent-generated explanations must not be treated as definitive proof of production safety or root cause.

## 9. Engineering Disciplines

### 9.1 Context Engineering

Context engineering focuses on the information supplied to the model.

Relevant capabilities include retrieval analysis, context selection, context construction, token efficiency, and context-quality evaluation.

The Context Engineering Agent may investigate and propose changes in this area.

### 9.2 Harness Engineering

Harness engineering focuses on the execution system surrounding model calls.

Relevant capabilities include execution control, output validation, retries, guardrails, error handling, and workflow reliability.

The Harness Analysis Agent may investigate and propose changes in this area.

### 9.3 Inference Engineering

Inference engineering focuses on model execution and its operational trade-offs.

Relevant capabilities include model configuration, model selection, latency, throughput, reliability, and cost.

The Inference Optimization Agent may investigate and propose changes in this area.

### 9.4 Cache Engineering

Cache engineering focuses on caching behaviour and its effect on correctness and performance.

Relevant capabilities include cache effectiveness, invalidation, freshness, latency, cost, and the correctness of cached results.

The Cache Analysis Agent may investigate and propose changes in this area.

These disciplines will be introduced incrementally. Each capability should be assessed using measurable outcomes appropriate to its purpose.

## 10. Data and Persistence

The platform will need to persist or access the following categories of information:

* Prompt definitions and versions.
* Prompt metadata and lifecycle history.
* Evaluation datasets and configurations.
* Evaluation results and comparison records.
* Runtime execution traces and metadata.
* Governance policies and approval records.
* Audit events.
* Diagnostic investigations and verified incident records.
* Improvement requests and deferral history.
* Candidate changes and their evaluation results.
* Relevant deployment and rollback history.
* Agent execution metadata and relevant outputs.

The specific storage technologies, schemas, retention policies, and data-access patterns will be selected during implementation design.

Persistence must preserve the traceability required to connect changes, executions, evaluations, diagnostic findings, and lifecycle decisions.

## 11. Deployment and Integration Boundaries

### 11.1 Independent Deployment

PromptOps AI must be deployable and useful without CoreFlow AI.

The architecture should keep product logic independent of any optional shared-infrastructure integration.

### 11.2 CoreFlow AI Integration

Future integration may provide access to shared capabilities through defined interfaces or adapters.

Potential shared capabilities include model-provider access, authentication, configuration, secrets management, logging, monitoring, storage, and deployment infrastructure.

These integrations are future architectural options, not prerequisites for the initial implementation.

### 11.3 Future Existing-Application Integration

The initial runtime-first approach may later be extended to support existing AI applications that execute outside the PromptOps AI runtime.

This future integration mode should reuse applicable governance, evaluation, diagnostics, and observability capabilities without forcing every application to adopt the PromptOps AI runtime.

## 12. Reliability and Failure Handling

The architecture must account for failures in model invocation, retrieval, evaluation, external dependencies, and internal workflows.

Relevant mechanisms may include:

* Bounded retries for appropriate transient failures.
* Output validation.
* Explicit error states.
* Timeouts and failure isolation.
* Traceable workflow execution.
* Configurable fallback behaviour.
* Monitoring and alerting.
* Policy-governed rollback.

Retries and fallbacks must be designed to avoid uncontrolled execution, duplicated side effects, and misleading success signals.

Agent failures must also be recorded and handled explicitly. An unavailable agent must not cause the system to fabricate results or bypass mandatory governance controls.

The exact reliability mechanisms will be selected according to the initial runtime's requirements and dependencies.

## 13. Initial Implementation Scope

The initial implementation will prioritize a coherent RAG-first platform with:

* Prompt registration and version management.
* A functional RAG runtime.
* Context construction and model invocation.
* Configurable evaluation and version comparison.
* Governance and approval controls.
* Execution tracing and observability.
* Regression identification.
* Evidence-based diagnostic capabilities.
* An engineer-initiated improvement workflow.
* Basic support for relevant context, harness, inference, and cache investigations.

The agent catalogue describes proposed responsibilities across the architecture. It does not require every agent to be implemented as a separate service or delivered in the initial release.

Advanced autonomous optimization, broad support for all LLM application types, extensive agent collaboration, and integration with CoreFlow AI remain future capabilities unless explicitly brought into the initial scope.

The implementation plan will determine the precise sequence and depth of each capability.

## 14. To Be Reviewed

The following architectural questions are intentionally left open for a future review session.

### 14.1 Agent Boundaries and Implementation

* Which proposed agents should be separate agents, and which responsibilities should be combined?
* Which agents are necessary for the initial release?
* Which agent responsibilities should initially be implemented as deterministic logic or ordinary application services?
* What interfaces should agents use to access tools and supporting components?

### 14.2 Agent Orchestration

* Should orchestration be centralized or distributed across specific workflows?
* How should agents pass structured findings and evidence between one another?
* How should agent execution be bounded by time, cost, and iteration limits?
* Which workflows require sequential execution, and which can run in parallel?

### 14.3 Evaluation Design

* Which evaluation methods and metrics should be implemented first?
* How should evaluation datasets be organized and versioned?
* How should evaluation reliability and evaluator quality be assessed?
* How should evaluation thresholds be configured for different application requirements?

### 14.4 Diagnostic Knowledge

* What schema should be used for incident records and verified root causes?
* How should structured incident retrieval and similarity-based retrieval work together?
* What verification and authorization process should establish trusted diagnostic knowledge?
* How should conflicting investigation findings be represented?

### 14.5 Governance Implementation

* What initial roles and permission matrix should be supported?
* Which lifecycle transitions require human approval?
* How should configurable governance policies be represented and evaluated?
* What audit-event schema and retention requirements are necessary?

### 14.6 Runtime and Persistence

* Which backend and frontend technologies should be used?
* Which database and storage technologies best fit the initial scope?
* How should prompt versions, evaluations, traces, incidents, and audit records be stored and related?
* Which model-provider and retrieval interfaces are necessary for the first release?

### 14.7 Initial Delivery Priorities

* Which capabilities should be implemented first to deliver a coherent end-to-end workflow?
* Which proposed agents can be introduced incrementally after the basic platform works?
* What measurable acceptance criteria will define a successful initial release?

These questions will be resolved as part of architecture review and implementation planning. They do not prevent us from documenting the current architectural direction.

## 15. Future Architecture Decisions

Implementation-level decisions will be documented when sufficient information is available.

These may include:

* Backend and frontend technologies.
* Database and storage selection.
* Model-provider interfaces.
* Retrieval and vector-store implementation.
* Evaluation frameworks and metrics.
* Trace and incident data schemas.
* Agent orchestration mechanisms.
* Authentication and authorization implementation.
* Deployment architecture.
* Caching strategy.
* Operational monitoring and alerting.

These decisions should remain consistent with accepted project decisions and architectural principles.
