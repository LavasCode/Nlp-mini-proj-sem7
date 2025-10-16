import re
from typing import Dict, Any, List
from rapidfuzz import process, fuzz


KNOWN_SKILLS = [
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'sql', 'r',
    # Frameworks & Libraries
    'react', 'vue', 'angular', 'node.js', 'django', 'flask', 'fastapi', 'spring', 'spring boot', 'dotnet', 'laravel', 'rails', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'matplotlib', 'seaborn', 'spark',
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'github actions', 'gitlab ci',
    # Databases & Messaging
    'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'kafka', 'rabbitmq',
]

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_REGEX = re.compile(r"(?:(?:\+?\d{1,3}[\s-]?)?(?:\(\d{2,4}\)[\s-]?)?\d{3,4}[\s-]?\d{3,4}(?:[\s-]?\d{3,4})?)")
NAME_HINTS = re.compile(r"^(?:name\s*[:\-]\s*)?([A-Z][A-Za-z'\-]+(?:\s+[A-Z][A-Za-z'\-]+)+)$")

SECTION_HEADERS = [
    'education', 'experience', 'work experience', 'professional experience', 'skills', 'projects', 'certifications', 'summary', 'objective'
]


def parse_resume_text(text: str) -> Dict[str, Any]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    lower_text = text.lower()

    email = _extract_email(text)
    phone = _extract_phone(text)
    name = _extract_name(lines, email, phone)
    skills = _extract_skills(lower_text)
    education = _extract_section(text, ['education'])
    experience = _extract_section(text, ['experience', 'work experience', 'professional experience'])

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'education': education,
        'experience': experience,
    }


def _extract_email(text: str) -> str:
    m = EMAIL_REGEX.search(text)
    return m.group(0) if m else None


def _extract_phone(text: str) -> str:
    # pick the most reasonable phone-like string by length
    candidates = [m.group(0) for m in PHONE_REGEX.finditer(text)]
    candidates = [c for c in candidates if len(re.sub(r"\D", "", c)) >= 7]
    if not candidates:
        return None
    # prefer +country formats
    candidates.sort(key=lambda c: (not c.strip().startswith('+'), len(re.sub(r"\D", "", c)) * -1))
    return candidates[0]


def _extract_name(lines: List[str], email: str, phone: str) -> str:
    # Heuristics: top few lines with 2-4 capitalized tokens, not containing email/phone
    header_candidates = lines[:8]
    best = None
    for line in header_candidates:
        if (email and email in line) or (phone and phone in line):
            continue
        words = re.findall(r"[A-Za-z][A-Za-z'\-]+", line)
        caps = [w for w in words if w[0].isupper()]
        if 2 <= len(caps) <= 4 and len(' '.join(words)) <= 60:
            if NAME_HINTS.match(line):
                return NAME_HINTS.match(line).group(1)
            best = ' '.join(caps)
            break
    return best


def _extract_skills(lower_text: str) -> List[str]:
    found = set()
    for skill in KNOWN_SKILLS:
        pattern = r"(?<![\w\-/])" + re.escape(skill) + r"(?![\w\-/])"
        if re.search(pattern, lower_text):
            found.add(skill)
    # fuzzy match fallbacks for near-misses
    tokens = re.findall(r"[a-zA-Z][a-zA-Z+.#\-]{1,30}", lower_text)
    unique_tokens = list(dict.fromkeys(tokens))
    for token in unique_tokens:
        match, score, _ = process.extractOne(token, KNOWN_SKILLS, scorer=fuzz.token_set_ratio)
        if score >= 92:
            found.add(match)
    ordered = sorted(found)
    return ordered


def _extract_section(text: str, headers: List[str]) -> str:
    lower = text.lower()
    # find header positions
    indices = []
    for h in headers:
        idx = lower.find(h)
        if idx != -1:
            indices.append((idx, h))
    if not indices:
        return None
    indices.sort()
    start = indices[0][0]
    # end at next section header
    next_indices = [lower.find(h, start + 1) for h in SECTION_HEADERS]
    next_indices = [i for i in next_indices if i != -1 and i > start]
    end = min(next_indices) if next_indices else len(text)
    section_text = text[start:end].strip()
    return section_text if section_text else None
