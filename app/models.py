from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    habits = db.relationship(
        'Habit', backref='owner', lazy=True, cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    frequency = db.Column(db.String(20), default='daily')  # daily / weekly
    created_at = db.Column(db.Date, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logs = db.relationship(
        'HabitLog', backref='habit', lazy=True, cascade='all, delete-orphan'
    )

    @property
    def current_streak(self):
        """Count consecutive days checked in, ending today or yesterday."""
        sorted_dates = sorted([log.date for log in self.logs], reverse=True)
        if not sorted_dates:
            return 0

        today = date.today()
        # Streak is only "alive" if the most recent check-in was today or yesterday
        if (today - sorted_dates[0]).days > 1:
            return 0

        streak = 1
        for i in range(len(sorted_dates) - 1):
            gap = (sorted_dates[i] - sorted_dates[i + 1]).days
            if gap == 1:
                streak += 1
            elif gap == 0:
                continue  # duplicate safety, shouldn't happen due to unique constraint
            else:
                break
        return streak

    @property
    def total_checkins(self):
        return len(self.logs)

    def checked_in_on(self, day):
        return any(log.date == day for log in self.logs)

    def __repr__(self):
        return f'<Habit {self.name}>'


class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('date', 'habit_id', name='unique_daily_log'),
    )

    def __repr__(self):
        return f'<HabitLog {self.habit_id} on {self.date}>'
