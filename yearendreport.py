# Route: Year-End Report
@app.route('/year_end_report', methods=['GET'])
def year_end_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    report_data = {}
    try:
        with connection.cursor() as cursor:
            # Number of clients served
            cursor.execute("SELECT COUNT(DISTINCT client_id) AS clients_served FROM orders")
            report_data['clients_served'] = cursor.fetchone()['clients_served']

            # Items donated per category
            sql = """
                SELECT categories.name, COUNT(items.id) AS total_items
                FROM items
                JOIN categories ON items.category_id = categories.id
                GROUP BY categories.id
            """
            cursor.execute(sql)
            report_data['items_by_category'] = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", 'danger')
    finally:
        connection.close()

    return render_template('year_end_report.html', report_data=report_data)
