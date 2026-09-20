import os
import re
import time
import pandas as pd

class DataSanitizerAndInterceptor:
    def __init__(self):
        self.cui_pattern = re.compile(r'(CUI|RESTRICTED|CONFIDENTIAL|CLASSIFIED|SECRET|TOP\s?SECRET)', re.IGNORECASE)
        self.ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        self.ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
        self.api_key_pattern = re.compile(r'(hf_[a-zA-Z0-9]{34}|sk-[a-zA-Z0-9]{32,})')

    def sanitize_stream(self, input_text, mask_ip=False):
        sanitized = self.api_key_pattern.sub('[REDACTED_API_KEY]', input_text)
        sanitized = self.ssn_pattern.sub('[REDACTED_PII_SSN]', sanitized)
        cui_matches = self.cui_pattern.findall(input_text)
        sanitized = self.cui_pattern.sub('[REDACTED_CUI_MARKER]', sanitized)
        if mask_ip:
            sanitized = self.ip_pattern.sub('XXX.XXX.XXX.XXX', sanitized)
        return {
            'original_length': len(input_text),
            'sanitized_length': len(sanitized),
            'cui_markers_detected': len(cui_matches),
            'sanitized_output': sanitized,
            'was_modified': len(cui_matches) > 0 or len(input_text) != len(sanitized)
        }

    def intercept_token_stream(self, prompt, user_clearance):
        sanitization = self.sanitize_stream(prompt)
        high_risk_terms = ['DAN', 'IGNORE PREVIOUS INSTRUCTIONS', 'ROOT', 'SUDO', 'BYPASS', 'JAILBREAK']
        has_prompt_injection = any(term in prompt.upper() for term in high_risk_terms)
        clearance_levels = {'UNCLASSIFIED': 0, 'CUI': 1, 'SECRET': 2, 'TOP SECRET': 3}
        current_clearance = clearance_levels.get(user_clearance.upper(), 0)
        required_clearance = 1 if sanitization['cui_markers_detected'] > 0 else 0
        is_allowed = (current_clearance >= required_clearance) and not has_prompt_injection
        return {
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'clearance_granted': is_allowed,
            'prompt_injection_flagged': has_prompt_injection,
            'required_clearance_level': required_clearance,
            'user_clearance_level': current_clearance,
            'processed_prompt': sanitization['sanitized_output'] if is_allowed else '[BLOCKED BY INTERCEPTOR]'
        }

sanitizer_interceptor = DataSanitizerAndInterceptor()

class DynamicAudienceReportSynthesizer:
    def __init__(self, vault_path=None):
        self.vault_path = vault_path or os.path.expanduser('~/Google Drive/My Drive/EDS_Research_Vault')

    def generate_custom_audience_report(self, audience_type, scenario_name, target_dir=None):
        out_dir = target_dir or self.vault_path
        os.makedirs(out_dir, exist_ok=True)
        filename = f"Report_{audience_type.replace(' ', '_')}_{scenario_name.replace(' ', '_')}_{int(time.time())}.md"
        out_path = os.path.join(out_dir, filename)
        content = f"# AUDIENCE BRIEFING: {scenario_name.upper()}\n**Target Audience:** {audience_type}\n**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}\n"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return out_path

report_synthesizer = DynamicAudienceReportSynthesizer()
