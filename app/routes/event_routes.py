from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.event import Event
from app.models.registration import Registration

# 定義路由的 Blueprint
bp = Blueprint('event_routes', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    顯示所有活動的列表 (首頁)。
    """
    events = Event.get_all()
    return render_template('index.html', events=events)

@bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    """
    處理活動的建立。
    """
    if request.method == 'POST':
        name = request.form.get('name')
        event_date = request.form.get('event_date')
        description = request.form.get('description')
        
        # 基本驗證
        if not name or not event_date:
            flash('活動名稱與活動日期為必填欄位。', 'danger')
            return render_template('create_event.html')
            
        event_id = Event.create(name, event_date, description)
        if event_id:
            flash('活動建立成功！', 'success')
            return redirect(url_for('event_routes.event_detail', id=event_id))
        else:
            flash('活動建立失敗，請稍後再試。', 'danger')
            return render_template('create_event.html')
            
    return render_template('create_event.html')

@bp.route('/events/<int:id>', methods=['GET', 'POST'])
def event_detail(id):
    """
    顯示活動詳情與處理報名。
    """
    event = Event.get_by_id(id)
    if not event:
        flash('找不到該活動', 'danger')
        return redirect(url_for('event_routes.index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        contact_info = request.form.get('contact_info')
        
        # 驗證報名資料
        if not name or not gender:
            flash('姓名與性別為必填欄位。', 'danger')
            stats = Registration.get_stats_by_event(id)
            registrations = Registration.get_by_event(id)
            return render_template('event_detail.html', event=event, stats=stats, registrations=registrations)
            
        reg_id = Registration.create(id, name, gender, contact_info)
        if reg_id:
            flash('報名成功！', 'success')
            return redirect(url_for('event_routes.register_success', id=id))
        else:
            flash('報名失敗，請稍後再試。', 'danger')
            
    # GET 請求，或是 POST 失敗時準備畫面資料
    stats = Registration.get_stats_by_event(id)
    registrations = Registration.get_by_event(id)
    return render_template('event_detail.html', event=event, stats=stats, registrations=registrations)

@bp.route('/events/<int:id>/success', methods=['GET'])
def register_success(id):
    """
    顯示報名成功的感謝頁面。
    """
    event = Event.get_by_id(id)
    if not event:
        flash('找不到該活動', 'danger')
        return redirect(url_for('event_routes.index'))
        
    return render_template('register_success.html', event=event)
