# Route: Start an Order
@app.route('/start_order', methods=['GET', 'POST'])
def start_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        client_username = request.form['client_username']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Check if client exists
                cursor.execute("SELECT id FROM users WHERE username = %s AND role = 'client'", (client_username,))
                client = cursor.fetchone()
                if not client:
                    flash("Client does not exist!", 'danger')
                    return redirect(url_for('start_order'))

                # Create new order
                cursor.execute("INSERT INTO orders (client_id) VALUES (%s)", (client['id'],))
                order_id = connection.insert_id()
                session['current_order_id'] = order_id
                connection.commit()

                flash(f"Order started successfully! Order ID: {order_id}", 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()

    return render_template('start_order.html')
