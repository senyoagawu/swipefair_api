from faker import Faker
from dotenv import load_dotenv
load_dotenv()

fake = Faker()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import Jobseeker, Company


with app.app_context():
    db.drop_all()
    db.create_all()

    # employee = Employee(name="Margot", employee_number=1234, password="password")
    for index in range(10):
        db.session.add(Jobseeker(name=fake.name(), email=fake.email(), hashed_password=fake.password(), bio=fake.text()))

    for index in range(10):
        db.session.add(Company(company_name=fake.company(), email=fake.email(), hashed_password=fake.password(), bio=fake.text()))
    
    # db.session.add(employee)
    db.session.commit()
