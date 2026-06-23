# TrustChain-Onco

> **A Safety-Critical, Blockchain-Verified Federated Learning Framework with Explainable AI and Conformal Risk Guarantees for High-Stakes Oncological Diagnosis**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Track](https://img.shields.io/badge/Track-Privacy--Preserving%20Clinical%20AI-blueviolet)](#)
[![Domain](https://img.shields.io/badge/Domain-Medical%20AI%20%7C%20Oncology%20%7C%20FL%20%7C%20Blockchain-green)](#)

---

## Core Safety Thesis

> *No prediction reaches a clinician or patient without passing through verifiable trust checks (blockchain + ZKP), statistically guaranteed confidence checks (conformal prediction), explainability checks (Grad-CAM), and human-in-the-loop review — because in this domain, a silent model error is a patient-safety failure, not a metric drop.*

---

## Project Structure

```
TrustChain-Onco/
├── docs/                        # Proposal, architecture diagrams, references
│   └── PROPOSAL.md
├── phase1_ml/                   # Phase 1 — ML Core (Google Colab, T4 GPU)
│   ├── notebooks/
│   │   ├── 01_env_data_setup.ipynb
│   │   ├── 02_baseline_resnet18.ipynb
│   │   ├── 03_ensemble_training.ipynb
│   │   ├── 04_gradcam_explainability.ipynb
│   │   ├── 05_conformal_prediction.ipynb
│   │   ├── 06_adversarial_robustness.ipynb
│   │   ├── 06b_cell_segmentation.ipynb
│   │   └── 07_escalation_logic.ipynb
│   ├── src/
│   │   ├── models/
│   │   │   ├── resnet18_classifier.py
│   │   │   ├── convnext_tiny.py
│   │   │   └── swin_tiny.py
│   │   ├── explainability/
│   │   │   └── gradcam_gate.py
│   │   ├── confidence/
│   │   │   └── conformal_prediction.py
│   │   ├── adversarial/
│   │   │   └── robustness_eval.py
│   │   ├── segmentation/
│   │   │   └── cellpose_morphometrics.py
│   │   └── escalation/
│   │       └── escalation_gate.py
│   └── checkpoints/             # .gitignore'd — store on Google Drive
├── phase2_federated/            # Phase 2 — Federated Learning (Flower/PySyft)
│   ├── server/
│   │   ├── aggregator.py        # Byzantine-robust aggregation (Krum / Trimmed Mean)
│   │   └── collusion_detector.py
│   ├── client/
│   │   └── hospital_client.py
│   └── simulation/
│       └── noniid_partition.py
├── phase3_blockchain/           # Phase 3 — Permissioned Chain (Fabric / PoA Ethereum)
│   ├── contracts/
│   │   └── UpdateRegistry.sol
│   ├── scripts/
│   │   └── deploy.py
│   └── audit/
│       └── lineage_query.py
├── phase4_ipfs/                 # Phase 4 — Artifact Storage
│   └── ipfs_manager.py
├── phase5_zkp/                  # Phase 5 — Zero-Knowledge Proofs (Circom + Groth16/PLONK)
│   ├── circuits/
│   │   └── update_validity.circom
│   └── verifier/
│       └── zkp_verifier.py
├── phase6_clinical_ui/          # Phase 6 — Clinical Gate UI + Disclosure Workflow
│   ├── frontend/
│   └── workflow/
│       └── disclosure_fsm.py
├── evaluation/                  # Evaluation scripts & result logs
│   ├── metrics/
│   ├── red_team/
│   │   └── attack_suite.py
│   └── forensic/
│       └── lineage_reconstruct.py
├── .gitignore
├── requirements.txt
└── LICENSE
```

---

## Phases at a Glance

| Phase | Focus | Key Tech |
|-------|-------|----------|
| 1 | ML Core — Classifier, Ensemble, Grad-CAM, Conformal, Adversarial, Segmentation | PyTorch, PathMNIST-224, Cellpose |
| 2 | Federated Learning Simulation + Byzantine Defenses | Flower, Krum/Trimmed Mean, FoolsGold |
| 3 | Blockchain Audit & Smart Contracts | Hyperledger Fabric / PoA Ethereum, Solidity |
| 4 | Decentralized Artifact Storage | IPFS, content-addressed pinning |
| 5 | Zero-Knowledge Proof Verification | Circom, Groth16 / PLONK / Halo2 |
| 6 | Clinical UI, Human-in-the-Loop Gate, Patient Disclosure FSM | Flask/React, Cryptographic sealing |

---

## Safety Gates (Hard Rejects — Never Soft Warnings)

| Gate | Trigger | System Response |
|------|---------|----------------|
| ZKP Verification | Proof fails or times out | Hard reject — update never enters aggregation |
| Blockchain Unreachable | Network failure | Pause aggregation — serve last verified model only |
| IPFS Artifact Missing | Node unreachable or hash mismatch | Reject round — alert operators |
| Conformal Set Size > 1 | Ambiguous diagnosis | Force specialist escalation |
| Grad-CAM Diffuse | High activation entropy | Suppress auto-display — route to human review |
| Clinician Gate Bypassed | UI/workflow bypass attempt | Result stays cryptographically sealed |

---

## Dataset

- **PathMNIST-224** — colorectal histopathology, 9-class patch classification  
- Source: [MedMNIST v2](https://medmnist.com/)  
- License: CC BY 4.0

---

## Quick Start (Phase 1 — Google Colab)

```bash
# 1. Clone
git clone https://github.com/SHARAN2517/TrustChain-Onco.git

# 2. Open phase1_ml/notebooks/01_env_data_setup.ipynb in Google Colab
# 3. Set Runtime → T4 GPU
# 4. Run cells sequentially
```

---

## Full Proposal

See [`docs/PROPOSAL.md`](docs/PROPOSAL.md) for the complete project proposal including:
- Problem Statement
- Core Safety Principle
- All 13 System Modules (Architecture)
- Failure Mode Analysis
- Evaluation Plan
- Build Roadmap

---

## License

MIT — see [LICENSE](LICENSE)
