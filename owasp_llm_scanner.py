#!/usr/bin/env python3
"""
AWS CodePipeline OWASP Top 10 LLM Validation Engine
Parses orchestration fixtures to identify Prompt Injection flaws and structural misconfigurations.
"""

import json
import sys
from datetime import datetime, timezone

def audit_llm_code(file_path):
    print(f"[+] Reviewing model interaction file parameters: {file_path}")
    vulnerabilities = []
    
    with open(file_path, 'r') as f:
        code_content = f.read()

    # Rule 1: Evaluate dynamic hyperparameter risk configurations (LLM01/LLM02)
    if "temperature=1" in code_content.replace(" ", "") or "temperature=1.0" in code_content.replace(" ", ""):
        vulnerabilities.append({
            "OWASP_LLM_Mapping": "LLM02:2023 - Model Insecure Output Handling",
            "RiskDetails": "Model temperature set to absolute max (1.0). High threat of extreme hallucination/jailbreak injection vectors.",
            "Severity": "HIGH"
        })

    # Rule 2: Evaluate system prompt structures for lack of validation boundaries (LLM01)
    if "input_variables" in code_content and "SystemMessagePromptTemplate" in code_content:
        if "ignore previous instructions" not in code_content.lower() and "security guidelines" not in code_content.lower():
            vulnerabilities.append({
                "OWASP_LLM_Mapping": "LLM01:2023 - Prompt Injection Vulnerability",
                "RiskDetails": "System message template accepts raw user input variables without explicit defensive anchoring or formatting blocks.",
                "Severity": "MEDIUM"
            })

    return vulnerabilities

def main():
    target_fixture = "langchain_app_fixture.py"
    found_issues = audit_llm_code(target_fixture)
    
    report = {
        "ScanTimestamp": datetime.now(timezone.utc).isoformat(),
        "TargetValidated": target_fixture,
        "TotalVulnerabilitiesFound": len(found_issues),
        "FindingsLedger": found_issues
    }
    
    # Save architectural artifact log
    with open('owasp_llm_report.json', 'w') as out:
        json.dump(report, out, indent=4)
        
    if any(item['Severity'] == 'HIGH' for item in found_issues):
        print("[-] CRITICAL FAIL: Pipeline halted due to catastrophic OWASP LLM security violations.")
        sys.exit(1) # Break the AWS CodePipeline execution sequence
        
    print("[+] Success: Code pass finalized with no blocking pipeline failures.")

if __name__ == '__main__':
    main()
