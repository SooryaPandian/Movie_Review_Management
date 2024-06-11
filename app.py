from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db_operations import get_reviews_for_movie, add_review, get_user_by_username, add_user, get_user_by_id, get_reviews_by_user, update_review, delete_review, update_rating

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
    movie_id = request.args.get('movie_id')
    if not movie_id:
        return jsonify({"error": "movie_id parameter is required"}), 400

    reviews = get_reviews_for_movie(movie_id)
    if reviews is None:
        return jsonify({"error": "No reviews found for this movie"}), 404
    return jsonify({"reviews": reviews}), 200

@app.route('/add_review', methods=['POST'])
def submit_review():
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

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    reviews = get_reviews_by_user(user_id)

    return render_template('profile.html', user=user, reviews=reviews)

@app.route('/edit_review/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    request_data = request.json
    comment = request_data.get('comment')
    rating = request_data.get('rating')

    if comment:
        if not update_review(review_id, comment=comment):
            return jsonify({"error": "Failed to update review comment"}), 500
    if rating:
        if not update_rating(review_id, rating=rating):
            return jsonify({"error": "Failed to update review rating"}), 500

    return jsonify({"comment": comment, "rating": rating}), 200

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review_route(review_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if delete_review(review_id):
        return redirect(url_for('profile'))
    return "Failed to delete review", 500

if __name__ == '__main__':
    app.run(debug=True)
