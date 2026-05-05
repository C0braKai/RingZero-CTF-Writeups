import requests
import re
import hashlib

# Challenge URL
URL = "http://challenges.ringzer0team.com:10013/"

def get_message(session):
    """Fetch page and extract the message"""
    response = session.get(URL)

    # Extract message between BEGIN and END
    match = re.search(
        r"----- BEGIN MESSAGE -----<br />\s*(.*?)\s*<br />\s*----- END MESSAGE -----",
        response.text,
        re.S
    )

    if not match:
        print("[-] Failed to extract message")
        return None

    # Clean message
    message = match.group(1).replace("<br />", "").strip()
    return message


def hash_message(message):
    """Generate SHA512 hash"""
    return hashlib.sha512(message.encode()).hexdigest()


def send_hash(session, hash_value):
    """Send hash and get response"""
    response = session.get(URL, params={"r": hash_value})
    return response.text


def main():
    session = requests.Session()

    message = get_message(session)
    if not message:
        return

    print(f"[+] Extracted Message:\n{message}\n")

    hash_value = hash_message(message)
    print(f"[+] SHA512 Hash:\n{hash_value}\n")

    result = send_hash(session, hash_value)
    print("[+] Server Response:\n")
    print(result)


if __name__ == "__main__":
    main()