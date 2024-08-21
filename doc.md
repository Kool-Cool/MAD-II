## Influencer Engagement and Sponsorship Coordination Platform

ER diagram
![DBSchema]("DBSchema.png")

backend
    |───instance
        |─── test.db
    |───static
    |───templates
    |───admin.py            (admin controller)
    ├───api.py              (Handle all api routes)
    ├───app.py              
    ├───celerybeat-schedule.bak
    ├───celerybeat-schedule.dat
    ├───celerybeat-schedule.dir
    ├───config.py           
    ├───config_test.py
    ├───helper.py           (helper functions for database interaction)
    ├───influencer.py       (influencer controller)
    ├───models.py           (database models)
    ├───requirements.txt    
    ├───sponsor.py          (sponsor conteller)
    ├───tasks.py            
    ├───tasks_test.py
frontend
    ├───public
    └───src
        ├───assets
        ├───components
        │   ├───icons
        │   ├───Influencer
        │   ├───Modal
        │   └───Sponsor
        ├───router
        ├───store
        └───views
            ├───Admin
            ├───Logout
            └───NotFound