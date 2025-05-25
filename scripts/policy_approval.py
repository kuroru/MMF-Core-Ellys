import json
from datetime import datetime

def approve_policy(policy_path, approver):
    with open(policy_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['approved_by'] = approver
    data['approved_at'] = datetime.now().isoformat()
    data['status'] = 'approved'
    with open(policy_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[승인] {policy_path} 승인자: {approver}")

if __name__ == "__main__":
    approve_policy("policies/mmf_policy.json", "admin001")
