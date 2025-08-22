from models import Resume

def search(session, skills=None, education=None):
    q = session.query(Resume)
    if skills:
        for s in [x.strip().lower() for x in skills.split(',') if x.strip()]:
            q = q.filter(Resume.skills.ilike(f'%{s}%'))
    if education:
        q = q.filter(Resume.education.ilike(f'%{education}%'))
    return q.all()
