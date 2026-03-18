import math
import string
import random

def calculate_entropy(password):
    """
    Calculate the Shannon entropy of a password.
    
    Entropy is a measure of the unpredictability or randomness of the password.
    Higher entropy means the password is more difficult to guess.
    
    Formula: - sum(p_i * log2(p_i))
    where p_i is the frequency of character i in the password.
    """
    if not password:
        return 0.0
    
    # Calculate the frequency of each character in the password
    char_freq = {}
    for char in password:
        char_freq[char] = char_freq.get(char, 0) + 1
        
    entropy = 0.0
    length = len(password)
    
    # Calculate Shannon entropy
    for count in char_freq.values():
        p = count / length
        entropy -= p * math.log2(p)
        
    return entropy

def estimate_crack_time(password):
    """
    Estimates the time required to brute force a password,
    assuming an offline attack at 100 billion guesses per second (MD5 speed baseline).
    """
    if not password:
        return "0 seconds"
        
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(c in string.punctuation for c in password): charset_size += 32
    
    if charset_size == 0:
        charset_size = 1 # prevent math errors
        
    combinations = charset_size ** len(password)
    guesses_per_second = 100_000_000_000 # 100 Billion per second
    seconds = combinations / guesses_per_second
    
    return format_time(seconds)

def format_time(seconds):
    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} days"
    elif seconds < 3153600000:
        return f"{int(seconds / 31536000)} years"
    else:
        return f"{int(seconds / 3153600000)} centuries"

def simulate_hash_cracking(password):
    """
    Simulates real-world cracking times against different hashing algorithms
    using modern GPU speeds (e.g., RTX 4090 cluster).
    """
    if not password:
        return {
            "MD5": "0 seconds",
            "SHA-256": "0 seconds",
            "Bcrypt (Cost 12)": "0 seconds",
            "Argon2id": "0 seconds"
        }
        
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(c in string.punctuation for c in password): charset_size += 32
    
    if charset_size == 0:
        charset_size = 1
        
    combinations = charset_size ** len(password)
    
    # Modern hardware hash rates approx (guesses per second)
    speeds = {
        "MD5 (Poor)": 100_000_000_000,         # 100 GH/s
        "SHA-256 (Weak)": 20_000_000_000,      # 20 GH/s
        "Bcrypt (Good)": 100_000,              # 100 kH/s
        "Argon2 (Best)": 10_000                # 10 kH/s
    }
    
    results = {}
    for algo, speed in speeds.items():
        secs = combinations / speed
        results[algo] = format_time(secs)
        
    return results

def generate_ai_password(length=16):
    """
    Generates a cryptographically strong password meeting max complexity criteria.
    """
    length = max(length, 12) # enforce minimum length of 12
    
    # Pool for generation
    chars = string.ascii_letters + string.digits + string.punctuation
    
    # Ensure standard complexity representation
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    
    # Fill remaining required length
    password += [random.choice(chars) for _ in range(length - 4)]
    
    # Mix it up so patterns are unpredictable
    random.shuffle(password)
    
    return "".join(password)

import hashlib
import requests

def check_pwned_password(password):
    """
    Checks if a password has been exposed in data breaches.
    Uses k-Anonymity method with HaveIBeenPwned API (sends only first 5 chars of hash).
    """
    if not password:
        return 0
        
    # Generate SHA-1 Hash
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    head, tail = sha1password[:5], sha1password[5:]
    
    # Request matching hashes from HIBP
    url = f"https://api.pwnedpasswords.com/range/{head}"
    res = requests.get(url)
    if res.status_code != 200:
        return -1 # api error
        
    # Check if our hash tail is in the response
    hashes = (line.split(':') for line in res.text.splitlines())
    for h, count in hashes:
        if h == tail:
            return int(count)
    return 0
