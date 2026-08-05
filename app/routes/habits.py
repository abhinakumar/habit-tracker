from datetime import date, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Habit, HabitLog
from app.forms import HabitForm

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')


@habits_bp.route('/')
@login_required
def dashboard():
    habits = Habit.query.filter_by(user_id=current_user.id).order_by(Habit.created_at.desc()).all()
    return render_template('habits/dashboard.html', habits=habits, today=date.today())


@habits_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_habit():
    form = HabitForm()
    if form.validate_on_submit():
        habit = Habit(
            name=form.name.data,
            description=form.description.data,
            frequency=form.frequency.data,
            user_id=current_user.id
        )
        db.session.add(habit)
        db.session.commit()
        flash('Habit created!', 'success')
        return redirect(url_for('habits.dashboard'))
    return render_template('habits/new_habit.html', form=form)


@habits_bp.route('/<int:habit_id>/checkin', methods=['POST'])
@login_required
def checkin(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('habits.dashboard'))

    today = date.today()
    already_logged = HabitLog.query.filter_by(habit_id=habit.id, date=today).first()
    if not already_logged:
        db.session.add(HabitLog(habit_id=habit.id, date=today))
        db.session.commit()
        flash(f'Checked in "{habit.name}"! 🔥', 'success')
    else:
        flash('Already checked in today.', 'info')

    return redirect(url_for('habits.dashboard'))


@habits_bp.route('/<int:habit_id>')
@login_required
def habit_detail(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        flash('Not authorized.', 'danger')
        return redirect(url_for('habits.dashboard'))

    # Build last 30 days for a simple heatmap
    today = date.today()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    heatmap_data = [
        {'date': day.isoformat(), 'checked_in': habit.checked_in_on(day)}
        for day in last_30_days
    ]

    return render_template('habits/habit_detail.html', habit=habit, heatmap_data=heatmap_data)


@habits_bp.route('/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id == current_user.id:
        db.session.delete(habit)
        db.session.commit()
        flash('Habit deleted.', 'info')
    else:
        flash('Not authorized.', 'danger')
    return redirect(url_for('habits.dashboard'))
