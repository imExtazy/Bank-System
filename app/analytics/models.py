from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class TransactionStats:
    period: datetime
    count: int
    total_amount: float
    avg_amount: float

@dataclass
class ClientSegment:
    segment: str  # 'VIP', 'Regular', 'New'
    client_count: int
    total_balance: float
    avg_transactions: float

@dataclass
class CreditAnalysis:
    client_id: int
    credit_score: float
    risk_category: str  # 'Low', 'Medium', 'High'
    recommended_limit: float

@dataclass
class BranchPerformance:
    branch_id: int
    transaction_volume: float
    new_clients: int
    loan_issuance: float