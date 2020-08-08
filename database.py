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
from app.models import Jobseeker, Company, Chat, Experience, Opening


with app.app_context():
    db.drop_all()
    db.create_all()

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

    for index in range(5):
        db.session.add(Jobseeker(name=fake.name(), email=fake.email(), hashed_password=fake.password(), bio=fake.text()))
    demouser = Jobseeker(name='demouser', email='demo@gmail.com', hashed_password=generate_password_hash('password'), bio='stuff about stuff')
    db.session.add(demouser)
    
    for index in range(5):
        db.session.add(Company(company_name=fake.company(), email=fake.email(), hashed_password=fake.password(), bio=fake.text()))
    
    db.session.commit()
