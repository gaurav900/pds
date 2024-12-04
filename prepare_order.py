# Route: Prepare Order
@app.route('/prepare_order', methods=['GET', 'POST'])
def prepare_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        order_id = request.form['order_id']
        holding_location = 'Ready for Delivery'

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Update item locations to 'Ready for Delivery'
                sql = """
                    UPDATE item_locations
                    SET location_id = (
                        SELECT id FROM locations WHERE name = %s
                    )
                    WHERE item_id IN (
                        SELECT item_id FROM order_items WHERE order_id = %s
                    )
                """
                cursor.execute(sql, (holding_location, order_id))
                connection.commit()
                flash("Order prepared successfully!", 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()

    return render_template('prepare_order.html')
