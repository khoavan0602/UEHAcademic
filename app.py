from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime

app = Flask(__name__)
app.secret_key = 'ueh_academic_final_fix_v2026'
# ==========================================
# USERS GIẢ LẬP (LOGIN DEMO – CHO RENDER)
# ==========================================
users = {
    "student@ueh.edu.vn": {
        "email": "student@ueh.edu.vn",
        "password": "123456",
        "name": "Nguyễn Trọng N"
    }
}

# ==========================================
# 1. DỮ LIỆU CẤU TRÚC UEH (Dùng cho Documents & Register)
# ==========================================
ueh_structure = {
    "COB": {"name": "Trường Kinh Doanh (COB)", "majors": ["Tài chính", "Ngân hàng", "Kế toán", "Quản trị kinh doanh", "Marketing"]},
    "CELG": {"name": "Trường Kinh tế, Luật & Quản lý", "majors": ["Kinh tế học", "Luật kinh tế", "Quản lý công"]},
    "CTD": {"name": "Trường Công nghệ & Thiết kế", "majors": ["Công nghệ thông tin kinh doanh", "Khoa học dữ liệu", "Toán kinh tế"]}
}

# ==========================================
# 2. DỮ LIỆU CLB/ĐỘI/NHÓM (Dùng cho Forum & Units Page)
# ==========================================
# Dạng Dict cho Forum Sidebar
ueh_clubs = {
    "school_level": {
        "name": "Cấp Trường (Đoàn - Hội UEH)",
        "groups": ["CLB Guitar (UEHG)", "CLB Bóng chuyền (BC)", "CLB Dân ca UEH", "CLB Sinh viên khởi nghiệp (DYNAMIC)", "CLB Anh văn (BELL)"]
    },
    "academic_clubs": {
        "name": "CLB Học thuật - Chuyên ngành",
        "groups": ["CLB Công nghệ kinh tế (ET)", "CLB Nhân sự (HUREA)", "Margroup", "Travelgroup", "SCUE - Securities Club"]
    },
    "faculty_union": {
        "name": "Đoàn Khoa / Viện",
        "groups": ["Đoàn Khoa Kinh tế", "Đoàn Khoa Quản trị", "Đoàn Khoa Tài chính", "Đoàn Khoa Ngân hàng", "Đoàn Khoa Kế toán", "Đoàn Khoa CNTT"]
    }
}

# Dạng List cho trang "Về chúng tôi" (Units)
academic_units_list = [
    {"id": "bank", "name": "Đoàn khoa Ngân hàng", "type": "Khoa", "image": "https://placehold.co/100x100/blue/white?text=BANK", "description": "Đơn vị đi đầu trong phong trào học thuật lĩnh vực Ngân hàng - Fintech."},
    {"id": "tour", "name": "Đoàn khoa Du lịch", "type": "Khoa", "image": "https://placehold.co/100x100/green/white?text=TOUR", "description": "Năng động, sáng tạo với các cuộc thi về hướng dẫn viên."},
    {"id": "scue", "name": "SCUE - Securities Club", "type": "CLB", "image": "https://placehold.co/100x100/red/white?text=SCUE", "description": "Câu lạc bộ học thuật về chứng khoán lâu đời nhất."},
    {"id": "margroup", "name": "Margroup", "type": "Nhóm", "image": "https://placehold.co/100x100/orange/white?text=MAR", "description": "Nhóm sinh viên nghiên cứu Marketing."}
]

# Danh mục cho Diễn đàn Trao đổi
exchange_topics = ["Trao đổi điểm rèn luyện", "Review Giảng viên", "Kinh nghiệm thi cử", "Tìm trọ / Roommate", "Góc pass đồ"]

# ==========================================
# 3. DỮ LIỆU TÀI LIỆU
# ==========================================
doc_types = ["Slide bài giảng", "Tài liệu ôn tập", "Quiz / Trắc nghiệm", "Hướng dẫn học / Giải bài tập", "Đề thi cũ", "Giáo trình"]

documents = [
    {"id": 101, "title": "Giáo trình Triết học Mác-Lênin", "author": "Khoa LLCT", "unit_id": "CELG", "major": "Kinh tế học", "subject": "Triết học", "doc_type": "Giáo trình", "is_premium": False, "rating": 4.8, "views": "15.4K", "image": "https://placehold.co/300x400/aa0000/white?text=Giao+Trinh", "description": "Tài liệu học tập chính thức.", "content_preview": ["Chương 1", "Chương 2"], "year": "2025"},
    {"id": 102, "title": "Slide Quản trị Tài chính", "author": "GV. Khat CDN", "unit_id": "COB", "major": "Tài chính", "subject": "Quản trị Tài chính", "doc_type": "Slide bài giảng", "is_premium": True, "rating": 5.0, "views": "12.5K", "image": "https://placehold.co/300x400/005f69/white?text=Slide+QTTC", "description": "Bài giảng gốc.", "content_preview": ["Chương 1", "Chương 10"], "year": "2024"},
    {"id": 103, "title": "Quiz Toán Kinh tế (500 câu)", "author": "CLB Toán", "unit_id": "CTD", "major": "Toán kinh tế", "subject": "Toán Kinh tế", "doc_type": "Quiz / Trắc nghiệm", "is_premium": True, "rating": 4.9, "views": "6.8K", "image": "https://placehold.co/300x400/4c1d95/white?text=Quiz", "description": "Trắc nghiệm ôn tập.", "content_preview": ["Chương 1", "Đáp án"], "year": "2025"}
]

# Môn học phổ biến cho trang chủ
popular_courses = [
    {"code": "ECO501", "name": "Kinh tế Vi mô", "color": "text-green-600", "bg": "bg-green-50", "icon": "fa-chart-line"},
    {"code": "FIN501", "name": "Quản trị Tài chính", "color": "text-blue-600", "bg": "bg-blue-50", "icon": "fa-coins"},
    {"code": "MAT501", "name": "Toán Kinh tế", "color": "text-purple-600", "bg": "bg-purple-50", "icon": "fa-square-root-variable"},
    {"code": "ACC501", "name": "Nguyên lý Kế toán", "color": "text-orange-600", "bg": "bg-orange-50", "icon": "fa-calculator"}
]

# ==========================================
# 4. DỮ LIỆU CUỘC THI
# ==========================================
competitions = [
    {"id": 1, "name": "Giải thưởng NCKH UEH500", "organizer": "Phòng QLKH", "status": "Đang diễn ra", "date": "30/03/2026", "image": "https://placehold.co/600x300/blue/white?text=UEH500", "description": "Cuộc thi NCKH lớn nhất.", "recommend_keywords": ["NCKH", "Kinh tế"]},
    {"id": 2, "name": "Olympic Kinh tế lượng", "organizer": "Đoàn khoa Toán - Thống kê", "status": "Sắp diễn ra", "date": "15/04/2026", "image": "https://placehold.co/600x300/green/white?text=Olympic", "description": "Mô hình định lượng.", "recommend_keywords": ["Toán", "Kinh tế lượng"]}
]

# ==========================================
# 5. DỮ LIỆU FORUM (Đã phân loại)
# ==========================================
forum_posts = [
    {
        "id": 1, "forum_type": "exchange", "topic": "Review Giảng viên", 
        "author": "Minh Tú", "bg": "bg-pink-500", "initial": "T", 
        "title": "Review thầy cô dạy Vi mô?", 
        "content": "Cho em xin review thầy cô dễ tính với ạ. Em nghe nói thầy X khó lắm phải không?", 
        "likes": 145, "time": "2 giờ trước", "tags": ["K50", "Vi mô"],
        "comments": [
            {"user": "Hoàng Nam", "avatar": "H", "bg": "bg-blue-500", "content": "Thầy X dạy hay nhưng thi khó nha. Nên học cô Y nếu muốn điểm cao.", "time": "1 giờ trước"},
            {"user": "Lan Anh", "avatar": "L", "bg": "bg-green-500", "content": "Đồng quan điểm, né thầy X ra nếu yếu toán.", "time": "30 phút trước"}
        ]
    },
    {
        "id": 2, "forum_type": "academic", "club": "SCUE - Securities Club", 
        "author": "Ban Học Thuật SCUE", "bg": "bg-green-600", "initial": "S", 
        "title": "Nhận định thị trường tuần 20/10", 
        "content": "Phân tích kỹ thuật VN-Index: Khả năng cao sẽ có nhịp điều chỉnh về vùng 1250.", 
        "likes": 230, "time": "1 ngày trước", "tags": ["Chứng khoán"],
        "comments": [
            {"user": "Thành Đạt", "avatar": "D", "bg": "bg-gray-500", "content": "Bài phân tích rất chi tiết. Cảm ơn Ad.", "time": "5 giờ trước"},
            {"user": "Ngọc Mai", "avatar": "M", "bg": "bg-purple-500", "content": "Mình nghĩ tuần sau xanh chứ nhỉ?", "time": "2 giờ trước"},
            {"user": "Admin SCUE", "avatar": "S", "bg": "bg-green-600", "content": "Tùy thuộc vào tin tức CPI tối nay bạn nhé.", "time": "1 giờ trước"}
        ]
    },
    {
        "id": 3, "forum_type": "exchange", "topic": "Trao đổi điểm rèn luyện", 
        "author": "Nam K49", "bg": "bg-blue-500", "initial": "N", 
        "title": "Tìm hoạt động bù ĐRL mục 3", 
        "content": "Kỳ này mình thiếu điểm mục tham gia hoạt động chính trị xã hội. Có chương trình nào sắp tới không ạ?", 
        "likes": 56, "time": "5 giờ trước", "tags": ["ĐRL"],
        "comments": [
            {"user": "Thư Ký Đoàn", "avatar": "T", "bg": "bg-red-500", "content": "Sắp có Mùa hè xanh, bạn đăng ký là full điểm nhé.", "time": "Vừa xong"}
        ]
    },
    {
        "id": 4, "forum_type": "unit", "ref_id": "fin", 
        "author": "Admin Tài Chính", "bg": "bg-red-600", "initial": "A", 
        "title": "[Thảo luận] Tỷ giá USD/VND cuối năm", 
        "content": "Theo các bạn, tỷ giá có vượt mốc 25.500 không?", 
        "likes": 89, "time": "3 giờ trước", "tags": ["Vĩ mô"],
        "comments": []
    }
]

# --- ROUTES ---

@app.route('/')
def home():
    user = session.get('user')
    return render_template('home.html', user=user, documents=documents[:4], competitions=competitions, popular_courses=popular_courses, posts=forum_posts[:2])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check thiếu dữ liệu
        if not email or not password:
            flash("Vui lòng nhập email và mật khẩu", "error")
            return redirect(url_for('login'))

        user = users.get(email)

        # Check login
        if user and user['password'] == password:
            session['user'] = user
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('home'))
        else:
            flash("Email hoặc mật khẩu không đúng", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', ueh_structure=ueh_structure)

# --- ĐÂY LÀ ROUTE BỊ THIẾU GÂY RA LỖI ---
@app.route('/documents')
def document_list():
    user = session.get('user')
    # Nhận tham số từ URL
    search_query = request.args.get('q')
    school_filter = request.args.get('school')
    major_filter = request.args.get('major')
    type_filter = request.args.get('type')
    cost_filter = request.args.get('cost')
    
    filtered = documents
    # Logic lọc
    if search_query: filtered = [d for d in filtered if search_query.lower() in d['title'].lower()]
    if school_filter and school_filter != "all": filtered = [d for d in filtered if d.get('unit_id') == school_filter]
    if major_filter and major_filter != "all": filtered = [d for d in filtered if d.get('major') == major_filter]
    if type_filter and type_filter != "all": filtered = [d for d in filtered if d.get('doc_type') == type_filter]
    if cost_filter == 'free': filtered = [d for d in filtered if not d.get('is_premium')]
    elif cost_filter == 'premium': filtered = [d for d in filtered if d.get('is_premium')]
            
    return render_template('documents.html', user=user, documents=filtered, ueh_structure=ueh_structure, doc_types=doc_types)
# ----------------------------------------

@app.route('/document/<int:id>')
def document_detail(id):
    user = session.get('user')
    doc = next((d for d in documents if d['id'] == id), None)
    if not doc: return "404", 404
    return render_template('detail.html', user=user, doc=doc, related_docs=[])

@app.route('/competitions')
def competition_list():
    user = session.get('user')
    # Filter logic đơn giản
    return render_template('competitions.html', user=user, competitions=competitions, organizers=["Phòng QLKH", "Đoàn Khoa"])

@app.route('/competition/<int:id>')
def competition_detail(id):
    user = session.get('user')
    comp = next((c for c in competitions if c['id'] == id), None)
    if not comp: return "404", 404
    # Gợi ý tài liệu
    rec_docs = []
    if 'recommend_keywords' in comp:
        for key in comp['recommend_keywords']:
            rec_docs.extend([d for d in documents if key.lower() in d['title'].lower() or key.lower() in d['subject'].lower()])
    return render_template('competition_detail.html', user=user, comp=comp, recommended_docs=list({d['id']:d for d in rec_docs}.values()))

@app.route('/units')
def units_list():
    user = session.get('user')
    return render_template('units.html', user=user, units=academic_units_list)

@app.route('/unit/<string:unit_id>')
def unit_detail(unit_id):
    user = session.get('user')
    unit = next((u for u in academic_units_list if u['id'] == unit_id), None)
    if not unit: return "404", 404
    return render_template('unit_detail.html', user=user, unit=unit, docs=[], posts=[])

@app.route('/forum')
def forum():
    user = session.get('user')
    current_tab = request.args.get('tab', 'exchange')
    topic_filter = request.args.get('topic')
    club_filter = request.args.get('club')
    
    filtered_posts = [p for p in forum_posts if p.get('forum_type') == current_tab]
    
    if current_tab == 'exchange' and topic_filter and topic_filter != 'all':
        filtered_posts = [p for p in filtered_posts if p.get('topic') == topic_filter]
    if current_tab == 'academic' and club_filter and club_filter != 'all':
        filtered_posts = [p for p in filtered_posts if p.get('club') == club_filter]

    return render_template('forum.html', user=user, posts=filtered_posts, current_tab=current_tab, exchange_topics=exchange_topics, ueh_clubs=ueh_clubs, selected_topic=topic_filter, selected_club=club_filter)

@app.route('/forum/<int:id>')
def forum_detail(id):
    user = session.get('user')
    post = next((p for p in forum_posts if p['id'] == id), None)
    return render_template('forum_detail.html', user=user, post=post) if post else ("404", 404)

@app.route('/profile')
def profile():
    user = session.get('user')
    if not user: return redirect(url_for('login'))
    activity = {'saved_docs': [documents[0]], 'my_uploads': [documents[1]], 'forum_questions': [forum_posts[0]]}
    return render_template('profile.html', user=user, activity=activity)

@app.route('/upload')
def upload():
    return render_template('upload.html', user=session.get('user'), ueh_structure=ueh_structure)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)