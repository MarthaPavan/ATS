import re
from file_parser import extract_text

COMMON_SKILLS = ['python','java','c++','c#','javascript','react','angular','flask','django','sql','nosql','postgres','mysql','mongodb','aws','azure','gcp','docker','kubernetes','git','html','css','pandas','numpy','tensorflow','pytorch','nlp','machine learning']

EMAIL_RE = re.compile(r"[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}")

def parse_resume(filepath):
    text = extract_text(filepath) or ''
    text_lower = text.lower()
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    name = lines[0] if lines else ''

    emails = EMAIL_RE.findall(text)
    email = emails[0] if emails else ''

    skills_found = []
    for skill in COMMON_SKILLS:
        if skill in text_lower and skill not in skills_found:
            skills_found.append(skill)

    edu_lines = []
    for ln in lines:
        if any(k in ln.lower() for k in ['bachelor','master','b.sc','m.sc','mba','phd','university','college','institute','degree','diploma']):
            edu_lines.append(ln)

    exp_lines = [ln for ln in lines if 'year' in ln.lower() or 'experience' in ln.lower()]

    # Replace empty with 'Not Mentioned'
    def nm(val):
        return val if val else 'Not Mentioned'

    return {
        'name': nm(name),
        'email': nm(email),
        'education': nm('\n'.join(edu_lines)[:2000]),
        'skills': nm(', '.join(skills_found)),
        'experience': nm('\n'.join(exp_lines)[:2000]),
        'raw_text': text[:20000]
    }
