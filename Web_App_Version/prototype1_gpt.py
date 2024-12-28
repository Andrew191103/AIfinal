import spacy
import re
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2")
gpt_model = AutoModelForCausalLM.from_pretrained("gpt2")

# keyword buat risks
risk_keywords = [
    "personal information", "personal data", "sensitive information",
    "location", "IP address", "geolocation",
    "camera",
    "microphone", 
    "third-party",
    "data sharing",
    "advertising",
    "cookies",
    "analytics",
    "biometric data", 
    "user activity",
    "payment information",
    "behavioral data", "data breach",
    "unauthorized access", 
    "marketing purposes", "profiling", "data retention", "data processing",
    "device information", "financial information",
    "loss", "tampering", "leakage", "security management",
    "identity confirmation", 
    "after-sales services", "questionnaire surveys", "marketing surveys", 
    "improper use",
    "customer credit decisions", "recovering debts",
    "third-party services", "data portability", "cross-border data transfer",
    "health data", "genetic information",
    "face recognition", "fingerprint data", "voice recognition",
    "smart device tracking", "wifi tracking", "geolocation tracking",
    "digital fingerprinting", "app usage data", "social media activity", "clickstream data",
    "online profiling", "data aggregation", "user behavior analysis", "mobile app permissions",
    "data leaks", "cloud data storage", "data misuse", "unauthorized sharing",
    "user consent revocation", "data anonymization", "data pseudonymization"
]

# keywords buat permission
permission_keywords = list(set([
    "cookies", "cookie",
    "tracking technology", "tracking technologies",
    "share information", "share your data", "sharing information", "share data",
    "provision of personal information", "provide personal information", "disclose personal information",
    "provision of personal data", "provide personal data", "disclose personal data",
    "store instagram id", "store Instagram ID",
    "track ip address", "track ip addresses", "tracking ip addresses",
    "third-party services", "third-party service",
    "user consent",
    "data collection",
    "location tracking", "location trackings",
    "login notification",
    "stay logged in",
    "delete cookies",
    "control advertisements", "advertising tailored",
    "user interactions",
    "browser type", "operating system", "usage patterns",
    "response to inquiries",
    "after-sales services",
    "billing and settling charges",
    "identity confirmation",
    "fraud prevention",
    "deleting personal information",
    "data subject rights",
    "data security",
    "distribution of information",
    "commitment to data security",
    "opt out",
    "customize the site",
    "governmental agencies",
    "investigation",
    "privacy settings",
    "advertising preferences",
    "marketing emails",
    "data portability",
    "access to personal data",
    "deletion of data",
    "data correction",
    "usage data",
    "user preferences",
    "account information",
    "contact details",
    "demographic information",
    "browser history",
    "purchase history",
    "billing and settling",
    "notifications",
    "questionnaire surveys",
    "marketing analysis",
    "displaying advertisements",
    "improving services",
    "preventing improper use",
    "customer credit decisions",
    "recovering debts",
    "making contact",
    "revisions",
    "terms and conditions",
    "face recognition", "biometric data processing", "user consent withdrawal",
    "data sharing for advertising", "geolocation tracking", "fingerprint scanning",
    "voice recognition consent", "data transfer to third parties", "data retention period"
]))

def clean_markdown(text):
    text = re.sub(r'[#\*\-]', '', text)
    text = re.sub(r'\[(.?)\]\(.?\)', r'\1', text) 
    text = re.sub(r'!\[.\]\(.?\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def summarize_text_with_gpt(text, max_chunk_length=1024, max_new_tokens=100):
    if gpt_tokenizer.pad_token is None:
        gpt_tokenizer.pad_token = gpt_tokenizer.eos_token

    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = []

    for chunk in chunks:
        inputs = gpt_tokenizer(chunk, return_tensors="pt", truncation=True, max_length=max_chunk_length, padding=True)
        attention_mask = inputs['attention_mask']
        input_ids = inputs['input_ids']

        summary_ids = gpt_model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            num_beams=4,
            early_stopping=True,
            pad_token_id=gpt_tokenizer.pad_token_id
        )
        summary = gpt_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    return " ".join(summaries)

def summarize_policy_gpt(cleaned_text):
    return summarize_text_with_gpt(cleaned_text)

def format_gpt_summary(summary):
    sentences = re.split(r'(?<=[.!?]) +', summary)  # Split by sentence end
    seen = set()
    formatted_summary = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in seen:
            seen.add(sentence)
            concise_sentence = " ".join(sentence.split()[:15]) + ("..." if len(sentence.split()) > 15 else "")
            formatted_summary.append(f"\u2022 {concise_sentence}")
    return "\n".join(formatted_summary)


def detect_risks(summarized_text):
    detected_risks = []
    for keyword in risk_keywords:
        if keyword.lower() in summarized_text.lower():
            detected_risks.append(keyword.capitalize())
    return detected_risks

def extract_permissions_and_reasons(cleaned_text):
    permissions_with_reasons = []

    # buat allowance
    for keyword in permission_keywords:
        if keyword in cleaned_text.lower():
            if "cookies" in keyword or "tracking technology" in keyword:
                permissions_with_reasons.append((
                    "Allow the site to use cookies and tracking technology.",
                    "To gather information such as browser type, operating system, and usage patterns."
                ))
            elif "share information" in keyword or "third-party services" in keyword:
                permissions_with_reasons.append((
                    "Permit sharing of your information with third parties.",
                    "To assist with fraud prevention, investigations, or third-party services."
                ))
            elif "data security" in keyword or "commitment to data security" in keyword:
                permissions_with_reasons.append((
                    "Ensure data security.",
                    "To protect personally identifiable information and maintain confidentiality."
                ))
            elif "opt out" in keyword or "privacy settings" in keyword:
                permissions_with_reasons.append((
                    "Allow users to opt out of communications.",
                    "To provide users with control over receiving emails, newsletters, and other communications."
                ))
            elif "location tracking" in keyword:
                permissions_with_reasons.append((
                    "Allow the site to track location data.",
                    "To provide location-based services or advertisements."
                ))
            elif "advertising preferences" in keyword:
                permissions_with_reasons.append((
                    "Allow users to customize their advertising preferences.",
                    "To deliver tailored ads and improve user experience."
                ))
            elif "marketing emails" in keyword:
                permissions_with_reasons.append((
                    "Send marketing emails to users.",
                    "To inform users about new products, services, and campaigns."
                ))
            elif "data portability" in keyword:
                permissions_with_reasons.append((
                    "Enable data portability for users.",
                    "To allow users to transfer their data to other services or platforms."
                ))
            elif "notifications" in keyword or "notification" in keyword:
                permissions_with_reasons.append((
                    "Send important notifications to users.",
                    "To inform users about updates, maintenance, or changes in terms."
                ))
            elif "demographic information" in keyword:
                permissions_with_reasons.append((
                    "Collect demographic information from users.",
                    "To improve service offerings and tailor marketing strategies."
                ))
            elif "account information" in keyword:
                permissions_with_reasons.append((
                    "Access and update account information.",
                    "To ensure accurate billing and communication with users."
                ))
            elif "browser history" in keyword:
                permissions_with_reasons.append((
                    "Track user browser history.",
                    "To provide personalized recommendations and improve user experience."
                ))
            elif "purchase history" in keyword:
                permissions_with_reasons.append((
                    "Access user purchase history.",
                    "To offer tailored promotions and improve inventory management."
                ))
            elif "storing email addresses" in keyword:
                permissions_with_reasons.append((
                    "Store email addresses for newsletter subscriptions.",
                    "To send updates and communication to users who have opted in."
                ))
            elif "temporary storage of user data" in keyword:
                permissions_with_reasons.append((
                    "Temporarily store user data during visits.",
                    "To ensure website functionality and enhance browsing experience."
                ))
            elif "analytics and performance cookies" in keyword:
                permissions_with_reasons.append((
                    "Use analytics and performance cookies.",
                    "To collect data about user interactions for improving site operations."
                ))
            elif "Stay Logged In" in keyword:
                permissions_with_reasons.append((
                    "Allow the site to keep you logged in"
                    "To provide a seamless and continuous experience without frequent login"
                ))
            elif "User Consent" in keyword:
                permissions_with_reasons.append((
                    "Allow the site to obtain and manage your consent for data processing"
                    "To ensure that your personal data is handled in accordance with your preferences and legal requirements"
                ))
            elif "data collection" in keyword:
                permission_keywords.append((
                    "Allow the site to collect your personal data"
                    "To provide and improve services, fulfill contractual obligations, and perform necessary business operations"
                ))
            elif "Demographic Information" in keyword:
                permission_keywords.append((
                    "Allow the site to collect demographic information"
                    "To improve service offerings and tailor marketing strategies"
                ))
            elif "Terms and Conditions" in keyword:
                permission_keywords.append((
                    "Allow the site to enforce terms and conditions"
                    "To ensure compliance service usage guidelines and legal requirements"
                ))
            elif "Making Contact" in keyword or "Make Contact" in keyword:
                permission_keywords.append((
                    "Allow the site to make contact with you"
                    "To facilitate communication for service updates, support and notification"
                ))

    #nyari same words
    unique_permissions = []
    for permission, reason in permissions_with_reasons:
        if permission not in [p[0] for p in unique_permissions]:
            unique_permissions.append((permission, reason))

    return unique_permissions

def format_permissions(permissions_with_reasons):
    if not permissions_with_reasons:
        return "Permissions/Allowances and Reasons:\nThis privacy policy does not explicitly mention any permissions or allowances."
    output = []
    for permission, reason in permissions_with_reasons:
        output.append(f"\u2022 {permission}\n  - Reason: {reason}")
    return "\n".join(output)

def load_text(filepath):
    if filepath.lower().endswith('.pdf'):
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

# Main program
def main():
    time_count = time.time()
    # mama file 
    filepath = 'r18.com.md' 

    try:
        privacy_text = load_text(filepath)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    cleaned_text = clean_markdown(privacy_text)
    print("\nCleaned Text:\n", cleaned_text)

    policy_summary = summarize_policy_gpt(cleaned_text)
    formatted_summary = format_gpt_summary(policy_summary)
    print("\nFormatted GPT Summary:\n", formatted_summary)

    detected_risks = detect_risks(policy_summary)
    print("\nDetected Risks:\n")
    print("\n".join(f"\u2022 Potential risk detected related to: {risk}" for risk in detected_risks))

    permissions_with_reasons = extract_permissions_and_reasons(cleaned_text)
    print("\n" + format_permissions(permissions_with_reasons))

    time_counter_stop = time.time()
    print(f"\nTotal Runtime: {time_count - time_counter_stop:.2f} seconds")


if __name__ == "__main__":
    main()