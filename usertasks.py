# Route: User's Tasks
@app.route('/user_tasks', methods=['GET'])
def user_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    connection = get_db_connection()
    tasks = []
    try:
        with connection.cursor() as cursor:
            # Get user's tasks
            sql = """
                SELECT orders.id AS order_id, orders.status, users.username AS client_username
                FROM orders
                LEFT JOIN users ON orders.client_id = users.id
                WHERE orders.staff_id = %s OR orders.client_id = %s
            """
            cursor.execute(sql, (user_id, user_id))
            tasks = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", 'danger')
    finally:
        connection.close()

    return render_template('user_tasks.html', tasks=tasks)
