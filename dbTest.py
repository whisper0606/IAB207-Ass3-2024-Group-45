from website import db, create_app
from website.models import User, Event, Comment, Order
from datetime import datetime 

app = create_app()
with app.app_context():
    user = User(name='Alice', emailid='alice@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()

    # 2. Create an Event
    event = Event(
        name='Rock Concert',
        description='A night of rock music!',
        date=datetime(2024, 11, 1).date(),
        start_time=datetime.strptime('19:00', '%H:%M').time(),
        end_time=datetime.strptime('22:00', '%H:%M').time(),
        venue='Stadium',
        genre=Event.Genre.ROCK_ALT,
        image='concert.jpg',
        creator_id=user.id
    )
    db.session.add(event)
    db.session.commit()

    # 3. Create a Comment
    comment = Comment(text='Can\'t wait for this concert!', user_id=user.id, event_id=event.id)
    db.session.add(comment)
    db.session.commit()

    users = User.query.all()
    for user in users:
        print(user)

    events = Event.query.all()
    for event in events:
        print(event)

    comments = Comment.query.all()
    for comment in comments:
        print(comment)
