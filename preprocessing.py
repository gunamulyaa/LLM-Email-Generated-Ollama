import pandas as pd
import re
from bs4 import BeautifulSoup

df = pd.read_csv("Dataset/SharedMailbox_Export.csv")

def clean_subject(subject):
    subject = str(subject)
    subject = re.sub(r"^(re:|fw:|fwd:)\s*", "", subject, flags=re.IGNORECASE)
    subject = re.sub(r"\s+", " ", subject)
    return subject.strip()

def clean_body(html, max_len=1500):
    if pd.isna(html):
        return ""

    # Batasi panjang awal (CEGAH HANG)
    html = str(html)[:5000]

    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "meta", "head"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Normalisasi whitespace TANPA regex berat
    text = " ".join(text.split())

    return text[:max_len]


def detect_error(subject, body):
    subject_l = subject.lower()
    body_l = body.lower()

    # SUBJECT PRIORITY
    if "certificate error" in subject_l:
        return "CERTIFICATE_ERROR"
    if "cannot connect" in subject_l or "connection" in subject_l:
        return "AGENT_CONNECTION_ERROR"
    if "malicious file" in subject_l:
        return "MALWARE_DETECTED"
    if subject_l.startswith("success"):
        return "BACKUP_SUCCESS"

    # BODY FALLBACK
    if "tls" in body_l or "ssl" in body_l:
        return "CERTIFICATE_ERROR"
    if "user unknown" in body_l:
        return "SMTP_550"

    return "OTHER"

def detect_source(email):
    email = str(email).lower()
    if "kaseya" in email:
        return "kaseya"
    if "robustabackup" in email:
        return "robustabackup"
    if "arsllc" in email:
        return "arsllc"
    return "unknown"

rows = []
total = len(df)

for i, r in df.iterrows():
    # 🔹 PROGRESS INDICATOR
    if i % 50 == 0:
        print(f"Processing row {i}/{total}")

    subject = clean_subject(r["Subject"])
    body = clean_body(r["BodyContent"])

    rows.append({
        "error_type": detect_error(subject, body),
        "subject_clean": subject,
        "body_clean": body,
        "source": detect_source(r["FromEmail"])
    })


clean_df = pd.DataFrame(rows)

# Optional: drop noise
clean_df = clean_df[clean_df["error_type"] != "OTHER"]

clean_df.to_csv("Dataset/clean_emails.csv", index=False)
print("✅ Preprocessing selesai (subject-centric)")
