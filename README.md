# AWS CodePipeline LLM OWASP Top 10 Validation Scanner

[![Pipeline](https://img.shields.io/badge/Pipeline-AWS%20CodePipeline-orange.svg)](https://aws.amazon.com/codepipeline/)
[![Compliance](https://img.shields.io/badge/Standards-OWASP%20Top%2010%20LLM-red.svg)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
[![Language](https://img.shields.io/badge/Engine-Python-blue.svg)](https://www.python.org/)

## Operational Overview

This repository features an automated continuous delivery security stage built for **AWS CodePipeline** (leveraging an internal AWS CodeBuild runtime engine). 

It is specifically built to evaluate application orchestration files utilizing LangChain, LlamaIndex, or raw Bedrock Python SDK calls against the **OWASP Top 10 for Large Language Model Applications** framework. The script scans orchestration logic for deep security vulnerabilities, including un-sanitized system prompt injections (LLM01), loose model parameters (such as excessively high model temperatures causing unpredictability), and insecure output handling vulnerabilities (LLM02).

---

### Core Security Control Gates Deployed

* **System Prompt Injection Verification:** Parses prompt-template structures to flag missing user input validation constraints.
* **Model Configuration Auditing:** Flags dynamic hyperparameter thresholds (e.g., Temperature, Top-P) that expose systems to hallucinations or jailbreaks.
* **Automated Pipeline Block Enforcer:** Systematically halts the AWS CodePipeline execution stage if high-risk structural flaws fail validation.

---

## Repository Structural Mapping

```text
aws-codepipeline-llm-owasp-validator/
├── README.md                      # Pipeline architectural layout
├── buildspec.yml                  # AWS CodeBuild task operational pipeline
├── owasp_llm_scanner.py           # Core validation engine execution script
└── langchain_app_fixture.py       # Test asset representing vulnerable code
