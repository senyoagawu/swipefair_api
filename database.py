from faker import Faker
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
load_dotenv()

fake = Faker()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import Jobseeker, Company, Chat, Experience, Opening, Swipe


with app.app_context():
    db.drop_all()
    db.create_all()

    for index in range(5):
        db.session.add(Jobseeker(name=fake.name(), email=fake.email(), hashed_password=generate_password_hash('password'), bio=fake.text()))
        
    demoJobseeker = Jobseeker(name='demoJobseeker', email='demoJobseeker@gmail.com', hashed_password=generate_password_hash('password'), bio='stuff about stuff')
    demoCompany = Company(company_name='demoCompany', email='demoCompany@gmail.com', hashed_password=generate_password_hash('password'), bio='stuff about stuff')
    
    db.session.add(demoJobseeker)
    db.session.add(demoCompany)
    
    for index in range(5):
        db.session.add(Company(company_name=fake.company(), email=fake.email(), hashed_password=generate_password_hash('password'), bio=fake.text()))
    


    db.session.add(Chat(jobseekers_id=1, companies_id=1))
    db.session.add(Chat(jobseekers_id=1, companies_id=3))
    db.session.add(Chat(jobseekers_id=2, companies_id=1))
    db.session.add(Chat(jobseekers_id=2, companies_id=3))
    db.session.add(Chat(jobseekers_id=3, companies_id=3))
    db.session.add(Chat(jobseekers_id=3, companies_id=4))
    db.session.add(Chat(jobseekers_id=4, companies_id=2))
    db.session.add(Chat(jobseekers_id=4, companies_id=4))
    db.session.add(Chat(jobseekers_id=5, companies_id=2))
    db.session.add(Chat(jobseekers_id=5, companies_id=5))

    jobs = [fake.job(), fake.job(), fake.job(), fake.job(), fake.job()]
    db.session.add(Experience(title=jobs[0], jobseekers_id=1, date_start='now', date_end='now', description=fake.text()))
    db.session.add(Experience(title=jobs[1], jobseekers_id=2, date_start='now', date_end='now', description=fake.text()))
    db.session.add(Experience(title=jobs[2], jobseekers_id=3, date_start='now', date_end='now', description=fake.text()))
    db.session.add(Experience(title=jobs[3], jobseekers_id=4, date_start='now', date_end='now', description=fake.text()))
    db.session.add(Experience(title=jobs[4], jobseekers_id=5, date_start='now', date_end='now', description=fake.text()))

    db.session.add(Opening(companies_id=1, title=jobs[0], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=1, title=jobs[1], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=2, title=jobs[3], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=2, title=jobs[4], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=3, title=jobs[0], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=3, title=jobs[1], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=3, title=jobs[2], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=4, title=jobs[3], description=fake.text(), created_at='now'))
    db.session.add(Opening(companies_id=5, title=jobs[4], description=fake.text(), created_at='now'))

    companies = Company.query.all()
    jobseekers = Jobseeker.query.all()
    openings = []
    # _ = [openings.extend(c.openings) for c in companies]
    # for opening in openings:
    #     for jobseeker in jobseekers:
    #         db.session.add(Swipe(jobseekers_id=jobseeker.id, openings_id=opening.id, created_at='now', swiped_right=False, super_swipe=True, role='company'))

    db.session.commit()
