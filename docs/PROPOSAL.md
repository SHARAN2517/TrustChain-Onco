# TrustChain-Onco — M.Tech Major Project Proposal

**A Safety-Critical, Blockchain-Verified Federated Learning Framework with Explainable AI and Conformal Risk Guarantees for High-Stakes Oncological Diagnosis**

- **Domain:** Medical AI · Oncology · Federated Learning · Blockchain · Explainable AI · Safety-Critical Systems  
- **Track:** Privacy-Preserving Clinical AI with Forensic Auditability

---

## Core Safety Thesis Statement

> No prediction reaches a clinician or patient without passing through verifiable trust checks (blockchain + ZKP), statistically guaranteed confidence checks (conformal prediction), explainability checks (Grad-CAM), and human-in-the-loop review — because in this domain, a silent model error is a patient-safety failure, not a metric drop.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Core Safety Principle](#2-core-safety-principle)
3. [System Architecture — Modules](#3-system-architecture--modules)
4. [Main Goals](#4-main-goals)
5. [Failure Mode Analysis](#5-failure-mode-analysis)
6. [Evaluation Plan](#6-evaluation-plan)
7. [Scope Boundaries](#7-scope-boundaries)
8. [Phase 1 Build Roadmap — ML Core](#8-step-by-step-build-roadmap--phase-1-machine-learning)
9. [Subsequent Phases Overview](#9-subsequent-phases-overview)

---

## 1. Problem Statement

Cancer diagnosis support systems operate in a domain where a missed malignancy (false negative) or a wrongly cleared scan can directly cost a patient's life, and a false positive can trigger unnecessary biopsies, treatment, and severe psychological harm. This elevates the system beyond a standard machine learning pipeline into a **safety-critical system**.

Centralized data pooling for training oncology models is restricted by privacy law (HIPAA in the US, the DPDP Act in India) and hospital data-governance policy, since raw histopathology slides and patient records cannot leave the originating institution. **Federated Learning (FL)** is the natural response: train locally at each hospital, transmit only model updates to a global aggregation server.

FL, however, introduces a new attack surface. A compromised or malicious hospital node can submit **poisoned updates** — corrupting or biasing the global model. In a cancer-diagnosis context, a single poisoned update degrading detection sensitivity is not a metric regression; it is a patient-safety incident. Existing defenses (basic bounds-checking, naive trust assumptions) are insufficient against colluding adversaries and offer no forensic trail for post-incident investigation.

Beyond the FL layer, three further problems compound the risk:

- **Opacity:** deep models offer no clinically interpretable justification for a prediction, so clinicians cannot verify whether the model looked at the right tissue regions.
- **False confidence:** standard softmax outputs are poorly calibrated, so a wrong prediction can be reported with deceptively high confidence.
- **Disclosure harm:** a cancer-positive result delivered without clinical mediation or psychological support is a documented risk factor for severe patient distress.

TrustChain-Onco is proposed to address all four problems jointly, within a single, formally gated system architecture, rather than as independent add-on features.

---

## 2. Core Safety Principle

### Central Thesis Claim

> No prediction reaches a clinician or patient without passing through verifiable trust checks (blockchain + ZKP), explainability checks (Grad-CAM + confidence), conformal-guaranteed risk bounds, and human-in-the-loop review — because in this domain, a silent model error is a patient-safety failure, not a metric drop.

This principle is operationalised as a sequence of **hard gates** rather than soft heuristics: any update or prediction that fails a gate is rejected or escalated, never passed through with a warning label. This distinction — hard reject vs. soft warning — is the architectural backbone the thesis defends.

---

## 3. System Architecture — Modules

### 3.1 Federated Learning Layer

Each participating hospital trains a local oncology classification model on-premise, on its own histopathology data. Only model weight updates — never raw patient data — are transmitted to the global aggregator.

> **Safety gate:** every local update must pass a pre-aggregation sanity check (gradient-norm bounds, statistical drift relative to the previous round) before entering the blockchain validation queue, catching grossly corrupted updates at the source.

### 3.2 Blockchain Trust & Audit Layer

A permissioned blockchain (e.g., Hyperledger Fabric, or a private Ethereum network using Proof-of-Authority) maintains an immutable log of every submitted update: submitting hospital ID, timestamp, content hash, and validation outcome. Smart contracts enforce update-acceptance rules before aggregation.

> **Safety role:** this layer is the system's black-box flight recorder. In the event of a misdiagnosis, the audit trail allows exact root-cause tracing — which model snapshot, which hospital's contribution, which round — a non-negotiable requirement for a clinical-deployment-track thesis.

### 3.3 IPFS Storage Layer

Full model update artifacts and checkpoints are too large for on-chain storage. They are stored on IPFS (InterPlanetary File System); only the content hash (CID) and metadata are anchored on-chain, preserving both auditability and scalability.

> **Safety addition:** redundant pinning across nodes plus integrity re-verification on every retrieval, so a corrupted or missing artifact can never silently fall back to an unverified model version.

### 3.4 Zero-Knowledge Proof (ZKP) Verification Layer

Each hospital generates a zero-knowledge proof demonstrating that its local update was computed correctly on valid, sufficient data — without revealing the underlying patient data or raw weights. The specific statement to be proven is precisely defined using a zk-SNARK circuit (implemented in Circom) proving: *local training ran for N epochs on at least K samples, with training loss reduction of at least X, without revealing the training data or exact gradient values.*

> **Safety rule:** failed ZKP verification is a hard reject. An update that cannot prove its own validity must never influence the global model — no exceptions, no override.

> **Design choice to defend:** Groth16 is faster to verify but requires a trusted setup per circuit; PLONK or Halo2 avoid per-circuit trusted setup at some verification-cost trade-off. State and justify the choice made.

### 3.5 Byzantine-Robust Aggregation Layer

Naive averaging of client updates is not acceptable when a poisoned update can affect cancer-detection accuracy. The aggregator uses a Byzantine-robust aggregation rule — **Krum, Trimmed Mean, or FLTrust** — so that a minority of malicious or faulty hospitals cannot statistically dominate the global model update.

> **Advanced addition:** clustering-based collusion detection (e.g., a FoolsGold-style cosine-similarity analysis of update directions across rounds) to catch correlated poisoning from multiple colluding hospitals, which simple per-update bounds-checking misses entirely.

### 3.6 Explainable AI + Confidence Gate Layer

Every prediction generates a **Grad-CAM heatmap** over the input histopathology image, highlighting the tissue regions driving the decision, together with a confidence measure and — where the ensemble architecture is used — an inter-model agreement signal.

> **Hard gate:** high confidence, high inter-model agreement, and a clinically plausible (spatially localized) Grad-CAM together permit display to the clinician as a supported finding. Low confidence, model disagreement, or a diffuse/implausible Grad-CAM forces escalation to mandatory specialist review; the prediction is suppressed from auto-display.

### 3.7 Conformal Prediction Layer *(Advanced — Statistical Safety Guarantee)*

Standard softmax confidence scores are known to be poorly calibrated. Conformal prediction is introduced to replace this with a mathematically guaranteed coverage property — constructing a prediction set such that the true diagnosis is contained in that set with at least **95% probability**, calibrated on a held-out dataset, regardless of the underlying model's calibration quality.

> **Escalation rule:** if the conformal prediction set contains more than one class, the case is automatically escalated to human review, since the model cannot statistically commit to a single diagnosis at the required confidence level.

### 3.8 Adversarial Robustness Testing Module *(Advanced)*

The oncology classifier is explicitly tested against adversarial perturbations (**FGSM, PGD**) on histopathology images, and robust accuracy is reported alongside clean accuracy.

### 3.9 On-Chain Model Versioning & Cryptographic Lineage *(Advanced)*

Every deployed global model version is hashed and logged on-chain, linked cryptographically to the exact set of validated client updates that produced it. Given any historical prediction, the system can reconstruct exactly which model version made it and which validated contributions shaped that model — **true forensic reproducibility**.

### 3.10 Human-in-the-Loop Clinical Gate

No diagnostic output — positive or negative — is ever shown directly to a patient. A clinician must review the AI output, its explanation, and its confidence before release. This gate is enforced **architecturally**: results are cryptographically sealed until a clinician's review action is logged, not merely a workflow policy that could be bypassed.

### 3.11 Patient Disclosure & Mental Health Safety Layer

A structured disclosure protocol governs how results reach the patient: plain-language explanation, clinician-mediated delivery, and immediate counselor or helpline routing for positive findings. This is modelled as a formal workflow with explicit states:

```
Result Generated → Clinician Reviewed → Disclosure Scheduled → Support Routed
```

### 3.12 Red-Team / Adversarial Evaluation Module *(Advanced)*

A dedicated module implements three attacker strategies against the system itself — **label-flipping poisoning, gradient-scaling poisoning, and colluding Sybil hospitals** — and quantitatively reports how the defense stack (blockchain logging, ZKP rejection, Byzantine-robust aggregation, collusion detection) performs against each.

### 3.13 Cell Segmentation & Morphometric Analysis Module *(Advanced)*

PathMNIST-224 provides pre-cropped, patch-level tissue classification labels. This module adds a parallel morphometric analysis layer on top of the same patches.

- **Tooling:** pretrained **Cellpose** (`'nuclei'` model) or StarDist as an alternative
- **Extracted features per patch:** cell/nucleus count, average nuclear area, nuclear size variance (pleomorphism proxy), cell density
- **Integration:** features displayed to clinician alongside Grad-CAM as supporting quantitative evidence; optionally feeds into the confidence/escalation gate (Module 3.6)
- **Scope discipline:** this module is additive and clearly separable — it can be de-scoped first if the timeline tightens

---

## 4. Main Goals

1. Design a federated, blockchain-verified diagnostic pipeline in which no single technical or human point of failure can silently cause a missed or wrong cancer diagnosis.
2. Defend against data-poisoning attacks using blockchain audit logs, ZKP verification, and Byzantine-robust aggregation, with measurable poisoning-resistance benchmarks.
3. Guarantee patient data privacy end-to-end: federated training plus zero-knowledge verification, with no raw patient data ever leaving hospital premises.
4. Enforce a mandatory explainability and statistically calibrated confidence gate (Grad-CAM plus conformal prediction) that suppresses unreliable predictions rather than presenting them with false confidence.
5. Architect human-in-the-loop clinical review as a hard system constraint, not a UI suggestion.
6. Embed a clinician-mediated, psychologically safe result-disclosure workflow as a core, formally modelled system module.
7. Provide full forensic traceability via on-chain model lineage, enabling post-incident root-cause analysis for any historical prediction.
8. Quantitatively demonstrate that the system degrades safely — escalating to human review — rather than failing silently, under both adversarial attack and low-confidence conditions.

---

## 5. Failure Mode Analysis

> A safety-critical system claim must be backed by an explicit failure-mode table. Each component failure must map to a defined fail-safe behaviour, never to silent fallback on an unverified state.

| Component Failure | Naive (Unsafe) Behaviour | Required Fail-Safe |
|---|---|---|
| Blockchain network unreachable | Skip validation, aggregate anyway | Pause aggregation; retain last validated global model |
| IPFS node unreachable / artifact missing | Fall back to local unverified copy | Reject the round; alert operators; never serve unverified artifact |
| ZKP verification timeout | Treat as valid by default | Treat as failed; hard reject the update |
| Conformal set size > 1 (ambiguous) | Display top-1 class with confidence | Force escalation to specialist review |
| Grad-CAM activation diffuse / non-localized | Display prediction with heatmap regardless | Suppress auto-display; route to human review |
| Clinician review step skipped/bypassed | Result auto-sent to patient | Architectural lock: result stays cryptographically sealed until reviewed |

### 5.1 False Negative vs. False Positive Cost Asymmetry

In oncology screening, a **false negative** (missed cancer) is typically far costlier than a false positive (unnecessary follow-up). The decision threshold for flagging a case as positive should be deliberately biased toward **sensitivity**, and this trade-off — along with its clinical justification and the resulting precision/recall operating point — should be explicitly reported and defended.

---

## 6. Evaluation Plan

Evaluation must go beyond overall accuracy and explicitly measure **safety behaviour** under adversarial and ambiguous conditions.

- Clean accuracy, F1-score, sensitivity and specificity of the oncology classifier on held-out PathMNIST-224 test data
- Poisoning attack success rate, measured **with and without** the blockchain + ZKP + Byzantine-robust aggregation defense stack, at increasing proportions of malicious clients (0%, 10%, 30%)
- Conformal prediction empirical coverage versus the target guarantee (observed coverage at a nominal 95% target)
- Percentage of low-confidence or disagreement cases correctly escalated (**true escalation rate**) and the false-escalation rate
- Robust accuracy under FGSM and PGD adversarial perturbation, compared against clean accuracy
- **Forensic traceability validation:** given a sample prediction, demonstrate full reconstruction of the model version and contributing updates from on-chain records
- System cost benchmarking: blockchain gas/transaction cost per update, IPFS pinning latency and cost at increasing client counts
- Cell segmentation quality: visual validation of Cellpose/StarDist boundaries and sanity check that morphometric features trend in the expected direction between benign and malignant classes

---

## 7. Scope Boundaries

> To keep the thesis achievable within a semester timeline on free-tier compute, the following are explicitly **out of scope** for the working prototype, noted as future work.

- Full multi-specialty deployment (radiology, pediatrics, cardiology) — prototype focuses on oncology / histopathology only
- Production-grade Hyperledger Fabric deployment across real hospital infrastructure — a local permissioned-chain simulation is sufficient
- Real ZK-SNARK circuit compilation at full hospital-scale data volumes — a representative smaller-scale circuit PoC is acceptable
- Live clinical trial or real patient deployment — evaluation on public benchmark datasets and simulated multi-hospital splits
- Per-cell-type segmentation training from scratch — Cellpose/StarDist pretrained weights are used (PathMNIST lacks pixel-level annotated masks)

---

## 8. Step-by-Step Build Roadmap — Phase 1: Machine Learning

> Everything in this phase runs on **Google Colab free T4 GPU**.

### Step 1 — Environment and Data Setup
- Set Runtime → T4 GPU
- Install: `torch`, `torchvision`, `medmnist`, `pytorch-grad-cam`, `scikit-learn`, `matplotlib`
- Download **PathMNIST-224** to Google Drive in an isolated cell (avoid re-downloading on session reset)
- Use **lazy DataLoader** access patterns (`__getitem__`-level decoding) to avoid RAM overflow

### Step 2 — Baseline Single-Model Training
- Train **ResNet18** first to validate full pipeline before ensemble complexity
- Self-contained, resumable training cells with Drive checkpointing every N steps
- `save_verified()` — reload-and-compare integrity check after every checkpoint save
- Handle PyTorch 2.6+ `weights_only` compatibility
- Establish baseline: accuracy, F1 per class, confusion matrix

### Step 3 — Three-Model Ensemble Training
- Train **ConvNeXt-Tiny** and **Swin-Tiny** on same data split
- Confirm architectural diversity via per-model confusion matrices and disagreement rate
- Compute **ensemble agreement state** (3/3, 2/3, 0/3) per test sample
- Test hypothesis: agreement state monotonically predicts error rate

### Step 4 — Explainability Layer (Grad-CAM)
- Integrate `pytorch-grad-cam` against final conv/attention layers of all three models
- Implement **activation-spread metric** (entropy of normalized Grad-CAM heatmap):
  - Low entropy → localized → clinically plausible
  - High entropy → diffuse → Explainability Gate triggers escalation
- Visual spot-check on held-out samples

### Step 5 — Conformal Prediction Calibration
- Hold out a **separate calibration set** (do not reuse test set — examiner-flagged mistake)
- Implement **split conformal prediction** with non-conformity score from softmax probabilities
- Target: 95% coverage guarantee
- Validate empirically on true test set; report prediction-set size distribution

### Step 6 — Adversarial Robustness Testing
- Implement **FGSM** and **PGD** attacks using `torchattacks`
- Report robust accuracy at multiple epsilon values vs. clean accuracy
- Visualize adversarial examples and Grad-CAM shift

### Step 6b — Cell Segmentation & Morphometric Features
- Install: `pip install cellpose`
- Run pretrained Cellpose `'nuclei'` model on sample PathMNIST patches; visually verify
- Extract per-patch: nucleus count, mean nuclear area, nuclear area std (pleomorphism), cell density
- Sanity-check: plot features grouped by PathMNIST class label; confirm malignant classes show expected trend (higher density, greater size variance)
- Store features alongside each patch's prediction for clinician view

### Step 7 — Escalation Logic Integration

Formal escalation rule combining three signals:

```python
escalate = (
    conformal_set_size > 1
    OR ensemble_agreement < 3/3
    OR gradcam_entropy > calibrated_threshold
)
```

- Evaluate on test set: report **true escalation rate** and **false escalation rate**

### Step 8 — Packaging for Federated Simulation
- Refactor training loop into a function that trains on arbitrary data subset and returns `state_dict` only
- Partition PathMNIST-224 into **5–10 non-IID client shards** for Phase 2

---

## 9. Subsequent Phases Overview

| Phase | Focus | Key Components |
|-------|-------|----------------|
| 2 | Federated Learning Simulation | Flower / PySyft, Krum, Trimmed Mean, FoolsGold, Red-Team poisoning |
| 3 | Blockchain Layer | Hyperledger Fabric testnet / PoA Ethereum, Solidity smart contracts, audit trail |
| 4 | IPFS Integration | Artifact storage, content-hash anchoring, redundant pinning |
| 5 | ZKP Circuit Design | Circom, Groth16 or PLONK/Halo2 choice justification, update-validity proofs |
| 6 | Clinical Gate UI & Disclosure FSM | Flask/React frontend, cryptographic sealing, disclosure state machine |

> Each phase is designed to be **independently defendable** — partial progress constitutes a coherent thesis checkpoint at every stage.

---

*Document maintained under version control. For architecture diagrams and bibliography, see the `docs/` directory.*
