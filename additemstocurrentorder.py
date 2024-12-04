# Route: Add Items to Current Order
@app.route('/add_to_order', methods=['GET', 'POST'])
def add_to_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'current_order_id' not in session:
        flash("No active order! Start an order first.", 'danger')
        return redirect(url_for('start_order'))

    order_id = session['current_order_id']
    connection = get_db_connection()
    available_items = []

    if request.method == 'POST':
        item_id = request.form['item_id']
        try:
            with connection.cursor() as cursor:
                # Add item to order
                cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (%s, %s)", (order_id, item_id))
                connection.commit()
                flash("Item added to order successfully!", 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')

    try:
        with connection.cursor() as cursor:
            # Get available items (not yet ordered)
            sql = """
                SELECT items.id, items.name
                FROM items
                WHERE items.id NOT IN (
                    SELECT item_id FROM order_items
                )
            """
            cursor.execute(sql)
            available_items = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", 'danger')
    finally:
        connection.close()

    return render_template('add_to_order.html', available_items=available_items)
