# PromptOps AI — Technology Stack

**Document path:** `docs/architecture/tech_stack.md`
**Project:** PromptOps AI
**Document status:** Initial baseline
**Last updated:** October 31, 2026

---

## 1. Purpose

This document defines the technology stack for PromptOps AI, a domain-agnostic Prompt Governance, Evaluation, and Observability Platform.

It records technology decisions, explains their rationale, and identifies unresolved choices that require further evaluation.

PromptOps AI will initially focus on RAG applications, with an architecture that supports future expansion to other LLM-powered applications.

The technology stack must support:

* Prompt versioning, lifecycle management, and governance.
* Repeatable evaluation and benchmarking.
* Regression detection and diagnostic investigation.
* RAG execution and context engineering.
* Agentic workflows with deterministic control boundaries.
* Human approval and policy-driven automation.
* Observability, traceability, and auditability.
* Reliable background processing.
* Secure, independently deployable application architecture.
* Cost-conscious development and deployment.

### Decision status definitions

| Status           | Meaning                                                                    |
| ---------------- | -------------------------------------------------------------------------- |
| Accepted         | A technology or architectural direction has been selected.                 |
| Proposed         | A recommendation exists but requires confirmation before becoming binding. |
| Under evaluation | The decision remains open and requires further investigation.              |
| Planned          | The capability is intended for a later implementation stage.               |
| Deferred         | The decision or capability is intentionally postponed.                     |

An accepted technology does not necessarily imply that every associated feature must be implemented during the MVP.

---

## 2. Technology Selection Principles

Technology selection will follow these principles.

### 2.1 Production relevance

Prefer technologies that are relevant to real-world AI engineering, backend development, data systems, and cloud deployment.

### 2.2 Learning depth

Use established libraries without treating them as black boxes. Understand their underlying concepts, limitations, integration boundaries, and operational trade-offs.

### 2.3 Controlled complexity

Avoid introducing multiple technologies that solve the same problem unless a clear requirement justifies the additional complexity.

### 2.4 Independent business logic

PromptOps AI must own its core business logic, governance rules, evaluation orchestration, and diagnostic workflows rather than delegating these responsibilities entirely to third-party frameworks.

### 2.5 Governance and interpretability

Technology choices must support traceability, explainable evidence, reproducible evaluations, authorization, and controlled changes.

### 2.6 Incremental delivery

Implement the architecture in stages. Long-term architectural capabilities must not become mandatory MVP deliverables unless they are necessary for a coherent initial product.

### 2.7 Cost awareness

Prefer local development during early implementation. Provision cloud resources only after reviewing expected costs, deployment requirements, and operational responsibilities.

---

## 3. Backend

### 3.1 Programming language

**Technology:** Python
**Status:** Accepted

Python will be the primary backend language.

It supports the project's API layer, RAG workflows, evaluation engine, background workers, and agentic workflows.

### 3.2 API framework

**Technology:** FastAPI
**Status:** Accepted

FastAPI will expose the application's HTTP APIs.

Responsibilities include:

* Request validation.
* Prompt and project operations.
* Evaluation initiation and status retrieval.
* Governance and approval endpoints.
* Authentication integration.
* Authorization enforcement.
* Background job submission.
* Result and diagnostic report access.

FastAPI endpoints must not become the sole enforcement mechanism for governance. The underlying application services must enforce authorization and valid state transitions.

### 3.3 Application architecture

**Approach:** Modular backend architecture
**Status:** Accepted as an architectural direction

The backend should separate responsibilities into modules such as:

* Prompt registry and version management.
* Evaluation orchestration.
* Governance and authorization.
* Approval and promotion workflows.
* RAG runtime.
* Background job management.
* Observability and diagnostics.
* Audit and reporting.

Modules may initially reside within one deployable backend application. Separate microservices are not required simply because the responsibilities are distinct.

### 3.4 Database access

**Technology:** SQLAlchemy
**Status:** Proposed

SQLAlchemy is the proposed database access layer for PostgreSQL.

Its selection and configuration should remain consistent with the chosen database migration strategy.

### 3.5 Database migrations

**Technology:** Alembic
**Status:** Accepted

Alembic will manage version-controlled database schema changes.

Migration files will be committed to Git. Schema changes must be reproducible across development, testing, and deployment environments.

---

## 4. Frontend

### 4.1 Frontend language

**Technology:** TypeScript
**Status:** Accepted

TypeScript will provide the language foundation for the frontend.

### 4.2 UI framework

**Technology:** React
**Status:** Accepted

React will power the PromptOps AI dashboard.

The interface will support:

* Prompt registry and version history.
* Prompt diffs and change reviews.
* Evaluation runs and benchmark comparisons.
* Regression and diagnostic reports.
* Approval and promotion workflows.
* Trace and audit history.
* Cost, latency, and quality metrics.
* Governance configuration.

### 4.3 Build tool

**Technology:** Vite
**Status:** Accepted

Vite will support frontend development and production builds.

### 4.4 UI components and styling

**Technologies:** shadcn/ui and Tailwind CSS
**Status:** Accepted

shadcn/ui will provide reusable interface components, with Tailwind CSS supporting styling.

The project will use established components for common interface elements and implement custom components where specialized functionality is necessary.

Potential custom interfaces include prompt-version diffs, evaluation comparisons, diagnostic evidence, and governance workflows.

### 4.5 Frontend/backend boundary

The frontend will communicate with the FastAPI backend.

The frontend may improve usability by hiding unavailable actions, but it must never be treated as the authority for permissions, governance enforcement, or approval eligibility.

---

## 5. Identity, Authentication, and Authorization

### 5.1 Identity provider

**Technology:** Amazon Cognito
**Status:** Accepted

Amazon Cognito will provide the identity and authentication integration for the AWS deployment.

Configuration, pricing, and integration requirements must be reviewed before deployment.

### 5.2 Role-based access control

**Approach:** Application-level RBAC
**Status:** Accepted

PromptOps AI will enforce application-specific permissions through backend services.

Candidate roles include:

* Project Administrator.
* Prompt Engineer.
* Evaluator.
* Approver.
* Production Operator.
* Viewer/Auditor.

The final role definitions and permission matrix will be documented during governance implementation.

### 5.3 Governance enforcement

**Approach:** Deterministic backend enforcement
**Status:** Accepted

The application will enforce:

* Authorization checks.
* Governance policies.
* Approval requirements.
* Separation of duties.
* Prompt lifecycle transitions.
* Promotion and rollback conditions.
* Audit recording.

An engineer must not be allowed to approve their own change when independent approval is required by policy, even if they possess multiple permissions.

Human approval requirements will be configurable within the platform's supported governance policies. Essential authorization and audit controls cannot be bypassed by configuration.

---

## 6. LLM Integration

### 6.1 Initial LLM platform

**Technology:** Amazon Bedrock
**Status:** Accepted

Amazon Bedrock will be the initial managed platform for model access.

It will support the RAG runtime and agentic workflows, subject to the capabilities of the selected models.

### 6.2 Model selection

**Status:** Under evaluation

A specific foundation model has not yet been selected.

Model selection must consider:

* Output quality.
* Reasoning and diagnostic capabilities.
* Structured-output support.
* Tool-calling capabilities.
* Latency.
* Throughput.
* Cost.
* Reliability.
* Integration requirements.

The selected model must be evaluated against representative PromptOps AI workloads before it becomes the default.

### 6.3 Provider abstraction

**Approach:** Lightweight provider interface
**Status:** Proposed

A small abstraction should isolate essential application logic from provider-specific invocation details.

The abstraction must remain practical. A comprehensive multi-provider gateway is not required for the MVP.

### 6.4 Model and prompt lineage

Model configuration and prompt versions must be recorded sufficiently to support meaningful comparisons.

Evaluation reports should distinguish prompt changes from changes to the model, model configuration, retrieval configuration, and context construction.

Otherwise, a quality regression may be attributed to the wrong component.

### 6.5 Cost monitoring

Model usage, latency, and relevant invocation metadata should be captured where supported.

The platform should provide evidence that helps engineers understand the cost and quality implications of changing prompts or model configurations.

---

## 7. RAG and Retrieval

### 7.1 Document processing

**Technology:** Unstructured
**Status:** Accepted

Unstructured will handle document processing and extraction.

It will be integrated with the remaining RAG pipeline rather than treated as a complete retrieval solution.

### 7.2 RAG frameworks

**Technologies:** LangChain and LlamaIndex
**Status:** Both selected for learning; production allocation remains under evaluation

The project will cover both frameworks to develop practical knowledge of their abstractions, capabilities, and limitations.

The learning approach will be balanced:

* Understand the underlying RAG concepts.
* Use established framework capabilities where appropriate.
* Implement selected components and experiments to understand their internals.
* Retain ownership of PromptOps AI's business logic.

Both frameworks will not automatically become dependencies of every production workflow.

The production framework choice should follow implementation needs and architectural fit. Redundant dependencies should be avoided.

### 7.3 Agent orchestration

**Technology:** LangGraph
**Status:** Accepted

LangGraph will support stateful, multi-step agent workflows where explicit workflow state and orchestration are useful.

Its use does not imply that every platform operation must be agentic.

Deterministic services remain responsible for operations that require predictable, enforceable behavior, including authorization, governance checks, prompt lifecycle transitions, approval gates, and persistence.

### 7.4 Vector storage

**Technology:** Chroma
**Status:** Accepted

Chroma will provide vector storage for the initial RAG runtime.

It will manage vector-related retrieval data, including embeddings, document chunks, and associated metadata as supported by the selected configuration.

The production hosting, persistence, backup, and recovery model remains to be finalized.

### 7.5 Relational data versus vector data

PostgreSQL and Chroma will serve different purposes.

**PostgreSQL** will store structured application data, including:

* Prompt records and versions.
* Evaluation runs and results.
* Benchmark metadata.
* Governance policies.
* Approval history.
* Audit records.
* Job status and execution metadata.

**Chroma** will support vector retrieval for the RAG runtime.

The relationship between source documents, document chunks, retrieved context, prompt versions, and evaluation runs must remain traceable.

### 7.6 RAG pipeline responsibilities

The initial RAG runtime should support the following conceptual pipeline:

1. Document ingestion and processing.
2. Chunking and metadata preparation.
3. Embedding generation.
4. Vector indexing.
5. Retrieval and filtering.
6. Optional reranking where justified.
7. Context construction.
8. Prompt selection and assembly.
9. Model invocation.
10. Output validation.
11. Tracing and evaluation.

Not every stage requires a separate service. Responsibilities should be modular while the initial deployment remains manageable.

---

## 8. Evaluation and Regression Detection

### 8.1 Initial evaluation library

**Technology:** Ragas
**Status:** Accepted

Ragas will provide selected evaluation capabilities for the initial RAG-focused implementation.

Its metrics will be used where appropriate for the evaluation questions being investigated.

### 8.2 PromptOps-owned evaluation engine

**Approach:** Custom evaluation orchestration and governance integration
**Status:** Accepted

PromptOps AI will own:

* Evaluation run orchestration.
* Dataset and benchmark management.
* Evaluation configuration.
* Result persistence.
* Comparison between prompt versions.
* Regression detection.
* Configurable thresholds.
* Evaluation history.
* Reporting.
* Governance integration.

Ragas will not replace this platform-level functionality.

### 8.3 Business-driven evaluation

Evaluation criteria must be configurable according to the application and its requirements.

PromptOps AI should not force every application to optimize the same metrics.

Quality, relevance, faithfulness, latency, cost, reliability, and other criteria may be selected according to the use case.

### 8.4 Evaluation evidence and promotion

Evaluation results provide evidence; they do not independently authorize a production change.

Promotion workflows must consider configured requirements, which may include:

* Passing evaluation thresholds.
* Comparison with the current production version.
* Critical regression checks.
* Latency, cost, and reliability constraints.
* Security and governance checks.
* Independent human approval when required.

### 8.5 Future evaluation providers

**Status:** Deferred until justified

Additional evaluation libraries may be considered as the platform expands beyond RAG.

They will not be added merely to increase the number of dependencies.

---

## 9. Agentic Workflows

### 9.1 Orchestration technology

**Technology:** LangGraph
**Status:** Accepted

LangGraph will support stateful agent workflows.

### 9.2 Proposed agent responsibilities

The architecture identifies the following potential agent responsibilities:

1. Evaluation analysis.
2. Regression investigation.
3. Cross-component diagnostics.
4. Prompt optimization.
5. Context engineering analysis.
6. Harness engineering analysis.
7. Inference optimization analysis.
8. Cache engineering analysis.
9. Governance analysis.

These responsibilities do not require nine separate agents or deployable services.

The initial implementation should introduce only the workflows that provide clear value within the MVP.

### 9.3 Deterministic and agentic boundaries

Agents may investigate failures, synthesize evidence, rank hypotheses, explain trade-offs, and generate candidate improvements.

Deterministic services must retain responsibility for authorization, policy enforcement, lifecycle transitions, approvals, persistence, and other operations that require predictable outcomes.

The Prompt Optimization Agent must not approve or promote its own proposed changes.

### 9.4 Diagnostic evidence

Diagnostic workflows should distinguish:

* Observed facts.
* Inferred hypotheses.
* Verified root causes.
* Recommended investigation steps.
* Measured remediation outcomes.

Historical similarity must not be treated as proof of an identical root cause.

Where evidence is insufficient, the platform should acknowledge uncertainty and request further investigation rather than presenting speculation as established fact.

---

## 10. Database and Persistence

### 10.1 Primary database

**Technology:** PostgreSQL
**Status:** Accepted

PostgreSQL will serve as the primary relational database.

### 10.2 Local database

**Technology:** PostgreSQL via Docker Compose
**Status:** Accepted

Local development will use a containerized PostgreSQL instance.

The database will be configured with appropriate persistent storage for local development.

### 10.3 AWS database

**Technology:** Amazon RDS for PostgreSQL
**Status:** Accepted, subject to budget validation

RDS is the preferred production database deployment approach.

The final configuration must account for:

* Instance and storage costs.
* Network access.
* Credentials and secret handling.
* Backups and recovery.
* Monitoring.
* Database availability requirements.

### 10.4 Database migrations

**Technology:** Alembic
**Status:** Accepted

Schema changes will be version-controlled and applied through migrations.

### 10.5 Chroma persistence

**Status:** Under evaluation

The production hosting and persistence strategy for Chroma must be decided before deployment.

The selected approach must account for durable storage, backup, recovery, access control, and compatibility with the AWS deployment architecture.

Chroma persistence must not depend on an ephemeral application container filesystem.

---

## 11. Background Processing

### 11.1 Message queue

**Technology:** Amazon SQS
**Status:** Accepted

Amazon SQS will support asynchronous execution of longer-running workloads.

### 11.2 Workers

**Technology:** Dedicated Python workers
**Status:** Accepted

Workers will process jobs such as:

* Evaluation suites.
* Prompt-version comparisons.
* Regression analysis.
* Diagnostic workflows.
* Other resource-intensive operations justified by the product requirements.

The initial worker deployment model will be finalized during AWS implementation planning.

### 11.3 Job persistence

**Technology:** PostgreSQL
**Status:** Accepted

PostgreSQL will maintain durable job records, execution status, relevant timestamps, attempts, and associated results.

SQS is a messaging mechanism, not the authoritative record of the complete job lifecycle.

### 11.4 Failure handling

**Technologies:** Amazon SQS dead-letter queue and explicit retry handling
**Status:** Accepted

The background-processing design must account for:

* Duplicate message delivery.
* Idempotent job processing.
* Transient failures.
* Retry limits and backoff.
* Poison messages.
* Dead-letter queue inspection and recovery.
* Worker failures and job-state reconciliation.

The application must not assume that each queue message is delivered exactly once.

### 11.5 Queue and database coordination

**Status:** Under evaluation

The implementation must handle the possibility that a database record is created but its queue message is not successfully published, or vice versa.

A transactional outbox pattern is one candidate for reliable coordination.

The selected design must be justified by the job durability requirements.

---

## 12. Observability and Tracing

### 12.1 Instrumentation foundation

**Technology:** OpenTelemetry
**Status:** Accepted

OpenTelemetry will provide the standardized instrumentation foundation.

Where appropriate, instrumentation should capture:

* Request execution.
* Retrieval operations.
* Model invocations.
* Background job execution.
* Latency and failures.
* Relevant component boundaries.

### 12.2 LLM observability

**Technology:** LangSmith
**Status:** Accepted

LangSmith will be used for LLM tracing, debugging, and development-time observability.

It will help engineers inspect supported execution traces, intermediate outputs, model calls, and failures.

### 12.3 PromptOps-owned observability

PromptOps AI will own product-specific functionality, including:

* Prompt-version lineage.
* Evaluation history.
* Regression analysis.
* Governance audit trails.
* Diagnostic reports.
* Connections between execution evidence and engineering decisions.

These capabilities must not depend entirely on LangSmith.

### 12.4 Integration and data handling

**Status:** Under evaluation

The exact integration between OpenTelemetry and LangSmith must be established during implementation.

Sensitive prompts, retrieved documents, credentials, and other confidential data must not be transmitted to external observability systems without appropriate data-handling controls.

LangSmith pricing, retention settings, and applicable data-handling options must be reviewed before production use.

---

## 13. Governance and Security

### 13.1 Governance enforcement

**Approach:** Deterministic backend services
**Status:** Accepted

Governance rules will be enforced by application services rather than relying on UI restrictions or agent instructions.

### 13.2 Human approval

**Approach:** First-class human-in-the-loop capability with configurable policies
**Status:** Accepted

The platform will support workflows that require human approval as well as policy-driven automation.

Configurable automation must not bypass essential authorization, auditability, or security controls.

### 13.3 Separation of duties

**Approach:** Backend-enforced authorization and approval rules
**Status:** Accepted

Where independent approval is required, the person submitting a change must not be able to approve that same change.

### 13.4 Secrets management

The following approach is accepted:

| Environment or requirement  | Approach                             |
| --------------------------- | ------------------------------------ |
| Production secrets          | AWS Secrets Manager                  |
| AWS service access          | IAM roles                            |
| Local development secrets   | `.env` files excluded from Git       |
| Non-sensitive configuration | Environment variables                |
| Secret protection           | Never commit credentials or API keys |

AWS Secrets Manager usage and costs must be reviewed before production deployment.

### 13.5 Least privilege

AWS roles and application permissions should follow least-privilege principles.

The frontend must not be trusted to enforce authorization. The backend must validate access to projects, prompts, evaluations, and governance operations.

### 13.6 Auditability

Meaningful governance operations should produce durable audit records.

Records should support investigation of who performed an action, what changed, when it occurred, and which applicable approval or policy requirements were satisfied.

The final audit schema and retention policy remain to be finalized.

---

## 14. Testing and Quality

### 14.1 Testing strategy

**Approach:** Comprehensive testing strategy, implemented incrementally
**Status:** Accepted

Testing must cover application correctness, integration behavior, RAG quality, regression detection, security, and governance.

### 14.2 Proposed testing tools

| Testing responsibility              | Proposed tool or approach                               |
| ----------------------------------- | ------------------------------------------------------- |
| Python unit tests                   | pytest                                                  |
| FastAPI endpoint tests              | pytest and HTTPX                                        |
| Database integration tests          | pytest with suitable PostgreSQL test infrastructure     |
| Dependency-backed integration tests | Testcontainers where appropriate                        |
| Frontend unit and component tests   | Vitest and React Testing Library                        |
| Browser-level end-to-end tests      | Playwright                                              |
| RAG quality evaluation              | Ragas and PromptOps AI's evaluation engine              |
| Governance testing                  | Automated authorization and lifecycle tests             |
| Background job testing              | Automated retry, duplicate-delivery, and recovery tests |

The testing tools are proposed unless separately marked accepted. Exact dependencies and configurations will be finalized during implementation.

### 14.3 Required testing principles

1. Governance rules must have automated tests.
2. Authorization must be enforced by backend services.
3. Prompt changes must be evaluated against relevant baselines.
4. Background processing must be tested for duplicate delivery and failure recovery.
5. Evaluation datasets and configurations must be versioned where appropriate.
6. CI must run the relevant test suites before changes are merged or deployed.
7. Tests must be repeatable and distinguish application correctness from probabilistic model quality.

Expensive LLM evaluations should not run indiscriminately on every commit. CI should use appropriately scoped tests, with larger evaluations triggered deliberately.

---

## 15. DevOps and Deployment

### 15.1 Containerization

**Technology:** Docker
**Status:** Accepted

Docker will package application components into reproducible container images.

### 15.2 Local development

**Technology:** Docker Compose
**Status:** Accepted

Docker Compose will support local development and the integration of selected application dependencies.

The local environment should allow meaningful development and testing without requiring a continuously running AWS deployment.

### 15.3 CI/CD

**Technology:** GitHub Actions
**Status:** Accepted

GitHub Actions will support automated testing, quality checks, container builds, and deployment workflows.

The public repository allows standard GitHub-hosted Actions runner usage without runner-minute charges under GitHub's public-repository offering. Applicable storage, artifact, and other usage conditions must still be observed.

### 15.4 Container registry

**Technology:** Amazon ECR
**Status:** Accepted for the AWS deployment phase

Amazon ECR will store versioned container images used by the AWS deployment.

Repositories will be created when the project is ready for cloud deployment, not during initial local development.

### 15.5 Application deployment

**Technology:** Amazon ECS with AWS Fargate
**Status:** Accepted

ECS with Fargate is the selected deployment direction for the initial MVP.

This avoids making Kubernetes administration a prerequisite for delivering the initial product.

Kubernetes and Amazon EKS are deferred until after the MVP unless requirements change.

### 15.6 Infrastructure as code

**Technology:** Terraform
**Status:** Accepted

Terraform will manage infrastructure configuration in version-controlled files.

Infrastructure should be introduced incrementally, with changes reviewed before application.

Terraform state, access permissions, and state-storage security must be addressed during deployment planning.

### 15.7 AWS services

The proposed AWS deployment includes:

* Amazon ECS with Fargate.
* Amazon ECR.
* Amazon RDS for PostgreSQL.
* Amazon SQS and a dead-letter queue.
* AWS IAM.
* AWS Secrets Manager.
* Amazon CloudWatch.
* Amazon Cognito.
* Amazon Bedrock.

The inclusion of a service in this list does not authorize immediate provisioning. Each resource must be assessed for necessity, cost, security, and deployment dependencies.

---

## 16. Development Tools

### 16.1 Version control

**Technology:** Git and GitHub
**Status:** Accepted

Source code, documentation, architecture decisions, tests, and infrastructure configuration will be maintained in Git.

Meaningful milestones should be committed regularly.

### 16.2 Documentation

Markdown files under `docs/` will record architecture, technology decisions, workflows, and implementation guidance.

Architecture and technology documents must distinguish accepted decisions from unresolved questions.

### 16.3 Dependency management

**Status:** Under evaluation

The Python and frontend dependency-management approach must be selected during implementation.

Dependencies should be version-controlled and reproducible.

The project should avoid adding overlapping libraries without a clear architectural reason.

---

## 17. Cost Management

Cost management is an architectural requirement for PromptOps AI.

### 17.1 Monthly AWS budget target

**Target:** ₹1,000–₹2,500 per month during initial deployment
**Status:** Accepted as a target, subject to pricing validation

This is a budget target, not a guarantee that the complete architecture can operate within that range.

The cost of the full stack must be estimated before provisioning resources.

### 17.2 Cost controls

The deployment plan should include:

* AWS Budgets and spending alerts.
* Appropriate resource sizing.
* Monitoring of Amazon Bedrock usage.
* Monitoring of AWS infrastructure costs.
* Monitoring of LangSmith usage.
* Limits on background worker concurrency.
* Bounded retries.
* Controlled execution of expensive evaluation suites.
* Removal or shutdown of unnecessary resources where appropriate.

AWS Budgets alerts do not guarantee a hard spending cap. Resource controls and active cost monitoring are also necessary.

### 17.3 Development and deployment strategy

Local development is preferred during the early implementation stages.

Cloud deployment should occur when the application and its operational requirements justify it.

The complete AWS cost model must account for database hosting, compute, networking, storage, identity, secrets, monitoring, model usage, and external observability usage.

---

## 18. MVP Scope Boundaries

The technology stack supports the long-term architecture, but initial implementation must remain focused.

### 18.1 Initial product focus

The MVP should prioritize a coherent RAG-focused workflow that demonstrates:

* Prompt registration and versioning.
* RAG execution.
* Evaluation against versioned datasets.
* Comparison between prompt versions.
* Regression identification.
* Traceability and diagnostic evidence.
* Governance and approval enforcement.
* Durable background execution.
* A usable engineering dashboard.

### 18.2 Capabilities that should remain incremental

The following must not automatically become full MVP deliverables merely because the architecture supports them:

* Every proposed agent responsibility.
* A comprehensive multi-provider LLM gateway.
* Multiple production RAG frameworks in the same workflow.
* Advanced automatic prompt optimization.
* Autonomous promotion without configured safeguards.
* A sophisticated distributed microservice architecture.
* Kubernetes deployment.
* Extensive cross-application integration capabilities.

### 18.3 Implementation principle

Build a coherent product first.

Use the selected technologies where they solve real implementation problems. Preserve architectural boundaries that enable future growth, but avoid building abstractions for hypothetical requirements without sufficient justification.

---

## 19. Decisions Still to Be Finalized

The following items remain open and should be resolved when their implementation context is clear.

| Area                  | Open question                                                                                        |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| LLM                   | Which Amazon Bedrock model best fits quality, latency, cost, and tool-calling requirements?          |
| RAG                   | Which responsibilities should use LangChain versus LlamaIndex in the initial implementation?         |
| Chroma                | What production hosting and persistence model will be used on AWS?                                   |
| Database              | What RDS configuration fits the budget and reliability requirements?                                 |
| Background processing | What queue/database coordination pattern is required for durable job submission?                     |
| Observability         | What exact integration and data-handling configuration will be used for OpenTelemetry and LangSmith? |
| Testing               | Which exact tool versions and configurations should be pinned?                                       |
| Frontend              | What frontend test and linting configurations should be adopted?                                     |
| Dependencies          | Which Python and frontend dependency-management tools should be selected?                            |
| Infrastructure        | What Terraform state-management approach and deployment workflow will be used?                       |
| Cost                  | What is the estimated total cost of the intended AWS configuration before provisioning?              |

These questions should be resolved when they affect implementation. They should not become a reason to delay progress on decisions that are already sufficiently established.

---

## 20. Summary

PromptOps AI will use a Python and FastAPI backend, a React and TypeScript frontend, Amazon Bedrock for model access, Unstructured for document processing, Chroma for vector storage, and PostgreSQL for structured application data.

Ragas will provide selected evaluation capabilities, while PromptOps AI owns evaluation orchestration, regression detection, governance integration, and reporting.

LangGraph will support stateful agent workflows, while deterministic services retain responsibility for authorization, governance enforcement, and lifecycle transitions.

OpenTelemetry and LangSmith will support observability. Amazon SQS and dedicated Python workers will handle long-running jobs.

The deployment direction is Docker, Docker Compose, GitHub Actions, Amazon ECR, ECS with Fargate, Terraform, and Amazon RDS for PostgreSQL, subject to deployment and cost validation.

The architecture prioritizes governance, interpretability, evaluation, reliable execution, and controlled incremental delivery.

**Guiding principle:** Use established technologies to accelerate implementation, maintain ownership of PromptOps AI's differentiating business logic, and introduce complexity only when it serves a demonstrated requirement.
