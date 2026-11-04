# PromptOps AI — Product Behaviour

**Document Type:** Product Behaviour Specification
**Status:** Initial Draft
**Last Updated:** November 4, 2026

---

## 1. Purpose

This document defines the expected behaviour of PromptOps AI from a product perspective.

It establishes how the platform should behave when users interact with its features, including prompt registration, version management, concurrent updates, evaluation, governance and observability.

This document serves as a reference for:

* Product behaviour and requirements.
* Architecture and implementation decisions.
* Functional and integration testing.
* Regression testing.
* Future product enhancements.

The implementation must satisfy the expected behaviours defined here.

---

## 2. Product Principles

PromptOps AI follows these principles:

1. **Version Integrity:** Every prompt version must be identifiable and independently traceable.
2. **Traceability:** Important user actions and system operations must have an auditable history.
3. **Governance:** Operations must respect configured policies and authorization rules.
4. **Evidence-Based Decisions:** Evaluation and promotion decisions must be supported by measurable evidence.
5. **Human Oversight:** Automated recommendations must not bypass required human approvals.
6. **Data Integrity:** Concurrent operations must not silently overwrite or corrupt existing data.
7. **Transparency:** The platform must communicate failures, conflicts and decisions clearly.

---

## 3. Prompt Registration

### 3.1 Expected Behaviour

An authenticated engineer must be able to register a new prompt in PromptOps AI.

The registration operation creates a new prompt resource and its initial version.

### 3.2 Registration Attributes

| Attribute      | Source           | Description                                   |
| -------------- | ---------------- | --------------------------------------------- |
| Prompt ID      | Server-generated | Unique identifier for the prompt resource.    |
| Prompt Name    | Client-provided  | Human-readable prompt name.                   |
| Description    | Client-provided  | Optional description of the prompt's purpose. |
| Prompt Content | Client-provided  | Actual prompt instructions or template.       |
| Registered By  | Server-derived   | Identity of the authenticated user.           |
| Version Number | Server-generated | Initial version number, starting at v1.       |
| Created At     | Server-generated | Timestamp of registration.                    |

### 3.3 Registration Rules

* Prompt IDs must be unique.
* The initial version must be assigned by the backend.
* Engineers must not independently assign version numbers.
* The registered prompt must be associated with its creator.
* Registration must respect authentication and authorization requirements.
* The system must retain the initial prompt version.

---

## 4. Prompt Version Management

### 4.1 Expected Behaviour

PromptOps AI must maintain a version history for every registered prompt.

Each modification that creates a new version must preserve the previous version.

### 4.2 Versioning Rules

* The first registered version is v1.
* Subsequent versions are assigned sequentially by the backend.
* The prompt ID remains unchanged across versions.
* Each version must have its own version identifier or version number.
* Previous versions must remain available for inspection and comparison.
* Existing versions must not be silently overwritten.
* Version history must be traceable.

### 4.3 Example

| Prompt ID | Version | Prompt Content                                         |
| --------- | ------- | ------------------------------------------------------ |
| P101      | v1      | Answer questions using the context.                    |
| P101      | v2      | Answer questions using the supplied context.           |
| P101      | v3      | Answer questions concisely using the supplied context. |

All three versions belong to the same prompt resource.

---

## 5. Concurrent Prompt Updates

### 5.1 Scenario

Two engineers attempt to modify the same prompt using the same existing version as their starting point.

For example:

* Engineer A retrieves v2.
* Engineer B retrieves v2.
* Engineer A successfully creates v3.
* Engineer B attempts to create another version based on the outdated v2.

### 5.2 Expected Behaviour

PromptOps AI must detect conflicting updates.

If the version on which an update is based is no longer the latest version, the system must reject the stale update.

### 5.3 Conflict Handling Rules

| Condition                          | Expected Behaviour                                         |
| ---------------------------------- | ---------------------------------------------------------- |
| Update based on the latest version | Allow the update, subject to other applicable validations. |
| Update based on a stale version    | Reject the update.                                         |
| Conflicting update                 | Return HTTP 409 Conflict.                                  |
| Automatic merging                  | Not permitted.                                             |
| Existing versions                  | Must remain unchanged.                                     |
| User action                        | Engineer must review the latest version before retrying.   |

### 5.4 Example

1. Engineer A and Engineer B both retrieve v2.
2. Engineer A submits an update.
3. The backend creates v3.
4. Engineer B submits an update based on v2.
5. The backend detects that v2 is no longer the latest version.
6. The backend rejects Engineer B's update with HTTP 409 Conflict.
7. Engineer B reviews v3 and decides whether to make another update.

### 5.5 Data Integrity Requirements

* Two concurrent updates must not create conflicting version numbers.
* Rejected updates must not modify existing prompt versions.
* Version creation must be atomic.
* The database must enforce uniqueness of the prompt ID and version number combination.
* Concurrency handling must be enforced by the backend and database, not solely by the frontend.

**Implementation Note:** The specific concurrency-control mechanism will be established during architecture and implementation.

---

## 6. API Behaviour

PromptOps AI will expose APIs for its core product operations.

Initial API examples:

| HTTP Method | Endpoint                         | Purpose                          |
| ----------- | -------------------------------- | -------------------------------- |
| POST        | /prompts                         | Register a new prompt.           |
| GET         | /prompts                         | Retrieve registered prompts.     |
| GET         | /prompts/{id}                    | Retrieve a specific prompt.      |
| GET         | /prompts/{id}/versions           | Retrieve prompt version history. |
| GET         | /prompts/{id}/versions/{version} | Retrieve a specific version.     |
| POST        | /prompts/{id}/versions           | Create a new prompt version.     |

API behaviour must include appropriate request validation, authorization, response handling and error handling.

The API must not trust client-provided values for server-managed attributes such as prompt IDs, version numbers or authenticated user identity.

---

## 7. Error Handling

The platform must communicate errors clearly and consistently.

Initial expected HTTP responses:

| Status Code | Meaning               | Example                                     |
| ----------- | --------------------- | ------------------------------------------- |
| 200         | Successful request    | Prompt retrieved successfully.              |
| 201         | Resource created      | Prompt registered successfully.             |
| 400         | Invalid request       | Malformed request data.                     |
| 401         | Unauthorized          | User is not authenticated.                  |
| 403         | Forbidden             | User does not have the required permission. |
| 404         | Resource not found    | Requested prompt does not exist.            |
| 409         | Conflict              | Update based on a stale prompt version.     |
| 422         | Validation error      | Request data fails validation.              |
| 500         | Internal server error | Unexpected backend failure.                 |

Actual API responses must provide meaningful error information without exposing sensitive internal details.

---

## 8. Initial Acceptance Criteria

The initial implementation must satisfy the following criteria.

### Prompt Registration

* [ ] An authenticated engineer can register a prompt.
* [ ] The backend generates a unique prompt ID.
* [ ] The backend assigns the initial version as v1.
* [ ] The backend derives the creator identity from authentication.
* [ ] The registration timestamp is generated by the backend.

### Prompt Versioning

* [ ] An engineer can create a new version of an existing prompt.
* [ ] The backend assigns the next version number.
* [ ] Previous versions remain available.
* [ ] Existing versions cannot be silently overwritten.

### Concurrent Updates

* [ ] The backend detects stale updates.
* [ ] A stale update returns HTTP 409 Conflict.
* [ ] Conflicting updates are not automatically merged.
* [ ] Rejected updates do not modify existing versions.
* [ ] Concurrent requests cannot create duplicate version numbers.

### API

* [ ] Request validation is implemented.
* [ ] Appropriate HTTP status codes are returned.
* [ ] Error responses are meaningful and consistent.
* [ ] Authorization is enforced on protected operations.

---

## 9. Open Product Decisions

The following decisions require further discussion before their implementation.

| Topic              | Open Question                                                                            |
| ------------------ | ---------------------------------------------------------------------------------------- |
| Prompt Templates   | What template formats and variable placeholders should be supported?                     |
| Prompt Lifecycle   | What lifecycle states should a prompt version have?                                      |
| Version Updates    | Should every edit create a new version, or should drafts be editable before publication? |
| Prompt Metadata    | What additional metadata should be associated with prompts?                              |
| Version Comparison | What information should be displayed when comparing two versions?                        |
| Access Control     | Which roles can register, modify, approve and promote prompts?                           |

These decisions should be documented as the relevant product capabilities are designed.

---

## 10. Document Maintenance


This document will evolve as PromptOps AI develops.

New product behaviours must be documented when relevant features are designed.

Changes to established behaviour must be reviewed and reflected in this document.

Implementation decisions belong in the architecture and project decision documents, while this document remains focused on expected product behaviour.
