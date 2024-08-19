from app import celery, mail, app
from flask_mail import Message
from models import User, AdRequest, Sponsor, Campaign
from datetime import datetime, timedelta, timezone
from flask import render_template
import os
import csv

@celery.task
def send_daily_reminders():
    with app.app_context():
        current_time = datetime.now(timezone(timedelta(hours=5, minutes=30))).date()
        users = User.query.filter(
            User.role == 'influencer',
            (User.login_date == None) | (User.login_date < current_time)
        ).all()

        for user in users:
            pending_ad_requests = AdRequest.query.filter_by(influencer_id=user.user_id, status='pending').all()
            if pending_ad_requests:
                msg = Message(
                    subject="Daily Reminder: Visit the App",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[user.email],
                    body=f"Dear {user.username}, please visit the app to manage your pending ad requests."
                )
                mail.send(msg)

@celery.task
def send_monthly_report():
    with app.app_context():
        sponsors = Sponsor.query.all()
        for sponsor in sponsors:
            campaigns = Campaign.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
            report_data = [{'campaign': campaign.to_dict(),
                            'ad_requests': [ad.to_dict() for ad in AdRequest.query.filter_by(campaign_id=campaign.campaign_id).all()]
                           } for campaign in campaigns]

            # Render the HTML report
            html_content = render_template('monthly_report.html', sponsor=sponsor, report_data=report_data)
            report_path = os.path.join('static', 'reports', f'monthly_report_{sponsor.sponsor_id}.html')
            with open(report_path, 'w') as f:
                f.write(html_content)
            
            # Send the report via email
            msg = Message(
                subject="Monthly Activity Report",
                sender=app.config['MAIL_USERNAME'],
                recipients=[sponsor.user.email],
                html=html_content
            )
            mail.send(msg)

@celery.task
def export_campaigns_as_csv(sponsor_id):
    with app.app_context():
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return {"message": "Sponsor not found"}, 404
        
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
        csv_file_path = os.path.join('static', 'reports', f'campaigns_{sponsor_id}.csv')
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Campaign Name', 'Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for campaign in campaigns:
                writer.writerow({
                    'Campaign Name': campaign.name,
                    'Description': campaign.description,
                    'Start Date': campaign.start_date,
                    'End Date': campaign.end_date,
                    'Budget': campaign.budget,
                    'Visibility': campaign.visibility,
                    'Goals': campaign.goals
                })

        # Notify sponsor via email
        msg = Message(
            subject="Campaign Export Completed",
            sender=app.config['MAIL_USERNAME'],
            recipients=[sponsor.user.email],
            body=f"Your campaign data has been exported. Download it here: {csv_file_path}"
        )
        mail.send(msg)