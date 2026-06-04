import os
from rag_pipeline import MutualFundRAGPipeline
from guardrails import GuardrailSystem

def main():
    print("Initializing pipeline...")
    pipeline = MutualFundRAGPipeline()
    guard = GuardrailSystem()

    funds = [
        "Tata Small Cap Fund Direct Growth",
        "Tata Gold ETF FOF Direct Growth",
        "Tata Digital India Fund Direct Growth",
        "Tata Silver ETF FOF Direct Growth",
        "Tata Arbitrage Fund Direct Growth"
    ]

    fund_specific_questions = [
        "What is the expense ratio of {fund}?",
        "What are the exit load details for {fund}?",
        "What is the minimum SIP amount for {fund}?",
        "What is the ELSS lock-in period for {fund}?",
        "What is the riskometer classification for {fund}?",
        "What is the benchmark index for {fund}?"
    ]

    general_questions = [
        "What is the process to download statements or capital gains reports for Tata Mutual Funds?"
    ]

    output_file = "faq_answers.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Tata Mutual Funds FAQ Answers\n\n")

        for fund in funds:
            f.write(f"## {fund}\n\n")
            for q_template in fund_specific_questions:
                query = q_template.format(fund=fund)
                f.write(f"**Q: {query}**\n\n")
                print(f"Querying: {query}")
                
                if guard.is_advisory_query(query):
                    answer = guard.get_refusal_response()
                else:
                    answer = pipeline.generate_answer(query)
                    
                    if "I cannot find this information" not in answer:
                        is_valid, error_msg = guard.validate_llm_response(answer)
                        if not is_valid:
                            answer = f"An error occurred during response validation: {error_msg}. Original answer: {answer}"
                
                f.write(f"**A:** {answer}\n\n")

        f.write("## General Questions\n\n")
        for query in general_questions:
            f.write(f"**Q: {query}**\n\n")
            print(f"Querying: {query}")
            
            if guard.is_advisory_query(query):
                answer = guard.get_refusal_response()
            else:
                answer = pipeline.generate_answer(query)
                
                if "I cannot find this information" not in answer:
                    is_valid, error_msg = guard.validate_llm_response(answer)
                    if not is_valid:
                        answer = f"An error occurred during response validation: {error_msg}. Original answer: {answer}"
            
            f.write(f"**A:** {answer}\n\n")

    print(f"Done! Answers written to {output_file}")

if __name__ == '__main__':
    main()
