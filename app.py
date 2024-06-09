from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db_operations import get_reviews_for_movie, add_review, get_user_by_username, add_user, get_user_by_id


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movieDetail/<int:movie_id>')
def movie_detail(movie_id):
    user_id = session.get('user_id')
    return render_template('movieDetail.html', movie_id=movie_id, user_id=user_id)

@app.route('/reviews', methods=['GET'])
def get_reviews():
    print("called get_reviews")
    movie_id = request.args.get('movie_id')
    if not movie_id:
        return jsonify({"error": "movie_id parameter is required"}), 400

    reviews = get_reviews_for_movie(movie_id)  # Fetch reviews from your database
    if reviews is None:
        return jsonify({"error": "No reviews found for this movie"}), 404
    print("converted get_reviews")
    return jsonify({"reviews": reviews}), 200

@app.route('/add_review', methods=['POST'])
def submit_review():
    print("called add_review")
    if 'user_id' not in session:
        return redirect(url_for('login'))

    request_data = request.json
    movie_id = request_data.get('movie_id')
    user_review = request_data.get('user_review')
    user_rating = request_data.get('user_rating')
    user_id = session['user_id']

    add_review(user_id, movie_id, user_review, user_rating)

    return jsonify({"message": "Review submitted successfully"}), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user_by_username(username):
            return "Username already exists", 400
        else:
            add_user(username, password)
            return redirect(url_for('login'))
    return render_template('register.html')

