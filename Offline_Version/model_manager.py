from prototype1_bart import (
    summarize_policy_bart, format_bart_summary,
    detect_risks as bart_detect_risks,
    extract_permissions_and_reasons as bart_extract_permissions_and_reasons,
    format_permissions as bart_format_permissions,
)
from prototype1_bert import (
    summarize_policy_bert, format_bert_summary,
    detect_risks as bert_detect_risks,
    extract_permissions_and_reasons as bert_extract_permissions_and_reasons,
    format_permissions as bert_format_permissions,
)
from prototype1_gpt import (
    summarize_policy_gpt,
    format_gpt_summary,  # Use GPT's bullet-point formatting
    detect_risks as gpt_detect_risks,
    extract_permissions_and_reasons as gpt_extract_permissions_and_reasons,
    format_permissions as gpt_format_permissions,
)

def analyze_text(model_name, text):
    """Analyze text using the specified model."""
    if model_name == "bart (moderate speed, moderate accuracy)":
        summary = summarize_policy_bart(text)
        formatted_summary = format_bart_summary(summary)
        risks = bart_detect_risks(summary)
        permissions = bart_extract_permissions_and_reasons(text)
        formatted_permissions = bart_format_permissions(permissions)
        return {
            "risks": risks,
            "permissions": formatted_permissions,
            "summary": formatted_summary,  # No bullet-point function exists for BART

        }
    elif model_name == "bert (fast, less accuracy)":
        summary = summarize_policy_bert(text)
        formatted_summary = format_bert_summary(summary)
        risks = bert_detect_risks(summary)
        permissions = bert_extract_permissions_and_reasons(text)
        formatted_permissions = bert_format_permissions(permissions)
        return {
            "risks": risks,
            "permissions": formatted_permissions,
            "summary": formatted_summary,  # No bullet-point function exists for BERT

        }
    elif model_name == "gpt (slow speed, best accuracy)":
        summary = summarize_policy_gpt(text)
        formatted_summary = format_gpt_summary(summary)  # Format as bullet points
        risks = gpt_detect_risks(summary)
        permissions = gpt_extract_permissions_and_reasons(text)
        formatted_permissions = gpt_format_permissions(permissions)
        return {
            "risks": risks,
            "permissions": formatted_permissions,
            "summary": formatted_summary,  # Return bullet-point summary

        }
    else:
        raise ValueError(f"Unknown model: {model_name}")
