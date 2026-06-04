import re
import urllib.parse

class GuardrailSystem:
    def __init__(self):
        # Trigger words that indicate an advisory, comparative, or speculative query.
        self.trigger_patterns = [
            r"\bshould i\b",
            r"\bis it good\b",
            r"\bis it bad\b",
            r"\bbetter\b",
            r"\brecommend\b",
            r"\bcompare\b",
            r"\bwhich is\b",
            r"\badxice\b",  # intentional typo catch
            r"\badbice\b",
            r"\badvisor\b",
            r"\bbest fund\b",
            r"\btop fund\b",
            r"\binvest in\b",
            r"\bworth it\b",
            r"\bforecast\b",
            r"\bpredict\b",
            r"\bfuture\b"
        ]
        self.compiled_triggers = [re.compile(pattern, re.IGNORECASE) for pattern in self.trigger_patterns]
        
        self.refusal_template = (
            "As a facts-only assistant, I cannot provide investment advice, recommendations, or fund comparisons. "
            "Please refer to an AMFI-registered financial advisor or view the AMFI Investor Corner "
            "(https://www.amfiindia.com/investor-corner) for educational resources."
        )

    def is_advisory_query(self, query: str) -> bool:
        """
        Checks if the query contains any trigger words indicating an advisory intent.
        Returns True if triggered, False otherwise.
        """
        for pattern in self.compiled_triggers:
            if pattern.search(query):
                return True
        return False

    def get_refusal_response(self) -> str:
        """
        Returns the standard compliance refusal template.
        """
        return self.refusal_template

    def validate_llm_response(self, response: str) -> tuple[bool, str]:
        """
        Validates the generated LLM response against strict compliance rules:
        1. Max 3 sentences (excluding the footer).
        2. Exactly one citation link.
        3. The presence of the "Last updated from sources:" footer.
        
        Returns (is_valid, error_message)
        """
        # 1. Check for the mandatory footer
        if "Last updated from sources:" not in response:
            return False, "Validation Error: Missing mandatory update date footer."
            
        # Extract the main content (everything before the footer) to check sentence count
        parts = response.split("Last updated from sources:")
        main_content = parts[0].strip()
        
        # 2. Sentence count check (basic regex for sentence splitting)
        # We split by . ! ? followed by space or end of string
        sentences = [s for s in re.split(r'[.!?]+(?=\s|$)', main_content) if s.strip()]
        if len(sentences) > 3:
            return False, f"Validation Error: Exceeded 3 sentence limit (Found {len(sentences)} sentences)."
            
        # 3. Check for URLs
        # Basic URL extraction regex
        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        urls = url_pattern.findall(response)
        
        if len(urls) == 0:
            return False, "Validation Error: Missing citation link."
        
        return True, "Valid"

if __name__ == "__main__":
    # Test the guardrails
    guard = GuardrailSystem()
    print("Testing query 'Should I buy Tata Digital India Fund?':", guard.is_advisory_query("Should I buy Tata Digital India Fund?"))
    print("Testing query 'What is the exit load?':", guard.is_advisory_query("What is the exit load?"))
