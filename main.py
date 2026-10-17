import datetime

class SpendingPolicyManager:
    """
    Manages spending policies for AI agents.
    This class demonstrates the distinction between an agent's technical ability
    to 'execute' a payment and the 'policy' that governs *when* and *how much*
    it is allowed to spend. It acts as the 'autonomous spending control mechanism'.
    """
    def __init__(self, daily_limit: float, transaction_limit: float, approved_vendors: list):
        self.daily_limit = daily_limit
        self.transaction_limit = transaction_limit
        self.approved_vendors = [v.lower() for v in approved_vendors]
        self.daily_spent = {} # Stores { 'YYYY-MM-DD': amount_spent } to track daily limits

    def _get_today_str(self):
        return datetime.date.today().isoformat()

    def check_and_approve_payment(self, agent_id: str, amount: float, vendor: str, purpose: str) -> bool:
        """
        Evaluates a payment request against defined spending policies.
        Returns True if approved, False otherwise.
        """
        print(f"\n--- Agent {agent_id} requesting payment ---")
        print(f"  Amount: ${amount:.2f}, Vendor: {vendor}, Purpose: {purpose}")

        # Policy 1: Check single transaction limit
        if amount > self.transaction_limit:
            print(f"  DENIED: Amount ${amount:.2f} exceeds single transaction limit of ${self.transaction_limit:.2f}.")
            return False

        # Policy 2: Check daily spending limit
        today_str = self._get_today_str()
        current_daily_spent = self.daily_spent.get(today_str, 0.0)
        if (current_daily_spent + amount) > self.daily_limit:
            print(f"  DENIED: Daily spending limit of ${self.daily_limit:.2f} would be exceeded. Already spent ${current_daily_spent:.2f}.")
            return False

        # Policy 3: Check approved vendors
        if vendor.lower() not in self.approved_vendors:
            print(f"  DENIED: Vendor '{vendor}' is not in the list of approved vendors.")
            return False

        # Policy 4: Example for purpose-based restriction
        if "unauthorized_research" in purpose.lower():
            print(f"  DENIED: Purpose '{purpose}' is restricted by policy.")
            return False

        # If all checks pass, approve and update daily spent
        self.daily_spent[today_str] = current_daily_spent + amount
        print(f"  APPROVED: Payment of ${amount:.2f} for '{purpose}' to '{vendor}'.")
        print(f"  Current daily spent for today: ${self.daily_spent[today_str]:.2f} (out of ${self.daily_limit:.2f})")
        return True

# --- Simulation of AI Agent Payment Attempts ---

def simulate_agent_payment(policy_manager: SpendingPolicyManager, agent_id: str, amount: float, vendor: str, purpose: str):
    """
    Simulates an AI agent attempting to make a payment.
    The actual payment execution (e.g., via x402, AP2, crypto wallet) is abstracted away;
    this function focuses on the *policy decision* before execution.
    """
    if policy_manager.check_and_approve_payment(agent_id, amount, vendor, purpose):
        # This block represents the 'execution' phase. If approved by policy,
        # the agent would proceed to interact with a payment gateway or API.
        print(f"  [Agent {agent_id}] Policy approved. Proceeding with payment execution...")
    else:
        # If denied, the agent aborts the payment attempt.
        print(f"  [Agent {agent_id}] Payment denied by policy. Aborting execution.")

if __name__ == "__main__":
    # Initialize the spending policy manager with company rules.
    # This represents the crucial 'spending policy' that governs AI agents.
    company_policy = SpendingPolicyManager(
        daily_limit=100.00, # Max total spending per day
        transaction_limit=30.00, # Max amount for a single transaction
        approved_vendors=["OpenAI", "Anthropic", "AWS", "Google Cloud", "DataServiceCo"]
    )

    print("--- Simulating AI Agent Spending Scenarios ---")

    # Scenario 1: Approved payment
    simulate_agent_payment(company_policy, "Agent-A", 15.00, "OpenAI", "API access for text generation")

    # Scenario 2: Another approved payment, getting closer to daily limit
    simulate_agent_payment(company_policy, "Agent-A", 25.00, "Anthropic", "Claude API call")

    # Scenario 3: Denied - Exceeds single transaction limit
    simulate_agent_payment(company_policy, "Agent-B", 35.00, "AWS", "Serverless function execution")

    # Scenario 4: Denied - Exceeds daily limit (Agent-A has spent 15+25=40, trying to spend 65 more -> 105 > 100)
    simulate_agent_payment(company_policy, "Agent-A", 65.00, "Google Cloud", "Data processing service")

    # Scenario 5: Denied - Unapproved vendor
    simulate_agent_payment(company_policy, "Agent-C", 10.00, "UnknownVendor", "New data source subscription")

    # Scenario 6: Denied - Restricted purpose
    simulate_agent_payment(company_policy, "Agent-D", 20.00, "DataServiceCo", "Unauthorized_Research data acquisition")

    # Scenario 7: Another approved payment for a different agent
    simulate_agent_payment(company_policy, "Agent-E", 20.00, "AWS", "Storage service")
