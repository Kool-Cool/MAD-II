# import pytest
# from app import app, celery ,db
# from tasks import send_daily_reminders, send_monthly_report, export_campaigns_as_csv
# from models import User, AdRequest, Sponsor, Campaign
# from flask_mail import Mail
# from flask import render_template
# import os
# from datetime import date  


# # Setup Flask app and Celery
# @pytest.fixture(scope='module')
# def test_app():
#     app.config.from_object('config_test.TestConfig')
#     with app.app_context():
#         db.create_all()  # Create tables
#         yield app
#         db.session.remove()
#         db.drop_all()  # Drop tables after test

# @pytest.fixture(scope='module')
# def test_celery():
#     celery.conf.update(app.config)
#     return celery

# # Ensure the reports directory exists
# def ensure_reports_directory():
#     if not os.path.exists('static/reports'):
#         os.makedirs('static/reports')

# # Testing send_daily_reminders
# def test_send_daily_reminders(test_app, test_celery):
#     # Add test data
#     user = User(
#         username='testuser',
#         email='test@example.com',
#         role='influencer',
#         password='testpassword'  # Provide a password
#     )
#     # Save user to database (mock or use test database)
#     db.session.add(user)
#     db.session.commit()
    
#     ad_request = AdRequest( campaign_id=1,influencer_id=user.user_id, status='pending')
#     db.session.add(ad_request)
#     db.session.commit()
    
#     # Call the task
#     result = send_daily_reminders.apply()
#     assert result.status == 'SUCCESS'

#     # Verify email sent
#     # This depends on how you want to verify email sending; you might use mock or check logs


# # Testing send_monthly_report
# def test_send_monthly_report(test_app, test_celery):
#     ensure_reports_directory()  # Ensure the directory exists

#     # Add test data
#     sponsor = Sponsor(
#         user_id=1,  # Assuming user_id is 1; adjust if needed
#         company_name='Test Sponsor Company',
#         industry='Technology',
#         budget=10000.00,
#         is_approved=True
#     )
#     db.session.add(sponsor)
#     db.session.commit()

#     campaign = Campaign(
#         sponsor_id=sponsor.sponsor_id,
#         name='Test Campaign',
#         description='A test campaign',
#         start_date=date(2024, 1, 1),
#         end_date=date(2024, 12, 31),
#         budget=5000.00,
#         visibility='public',
#         goals='Increase brand awareness',
#         niche='health'
#     )
#     db.session.add(campaign)
#     db.session.commit()

#     # Call the task
#     result = send_monthly_report.apply()
#     assert result.status == 'SUCCESS'

#     # Verify HTML report generated and email sent
#     report_path = os.path.join('static', 'reports', f'monthly_report_{sponsor.sponsor_id}.html')
#     assert os.path.exists(report_path)

#     # Cleanup
#     os.remove(report_path)


# # Testing export_campaigns_as_csv
# def test_export_campaigns_as_csv(test_app, test_celery):
#     # Add test data
#     # Ensure that the `Sponsor` instance is created correctly
#     sponsor = Sponsor(
#         user_id=1,  # Assuming user_id is 1; adjust if needed
#         company_name='Test Sponsor Company',
#         industry='Technology',
#         budget=10000.00,
#         is_approved=True
#     )
#     db.session.add(sponsor)
#     db.session.commit()
    
#     # The rest of your test code

    
#     # Call the task
#     result = export_campaigns_as_csv.apply(args=[sponsor.sponsor_id])
#     assert result.status == 'SUCCESS'

#     # Verify CSV file generated
#     csv_file_path = os.path.join('static', 'reports', f'campaigns_{sponsor.sponsor_id}.csv')
#     assert os.path.exists(csv_file_path)
    
#     # Cleanup
#     os.remove(csv_file_path)
