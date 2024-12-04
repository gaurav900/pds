# Route: Rank System (Popular Categories)
@app.route('/rank_categories', methods=['GET'])
def rank_categories():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    category_ranks = []
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT categories.name, COUNT(order_items.item_id) AS total_orders
                FROM order_items
                JOIN items ON order_items.item_id = items.id
                JOIN categories ON items.category_id = categories.id
                GROUP BY categories.id
                ORDER BY total_orders DESC
                LIMIT 10
            """
            cursor.execute(sql)
            category_ranks = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", 'danger')
    finally:
        connection.close()

    return render_template('rank_categories.html', category_ranks=category_ranks)
