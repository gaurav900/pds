# Route: Accept Donation
@app.route('/accept_donation', methods=['GET', 'POST'])
def accept_donation():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        donor_id = request.form['donor_id']
        item_name = request.form['item_name']
        location_name = request.form['location_name']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verify donor exists
                cursor.execute("SELECT id FROM donors WHERE id = %s", (donor_id,))
                donor = cursor.fetchone()
                if not donor:
                    flash("Donor does not exist!", 'danger')
                    return redirect(url_for('accept_donation'))

                # Insert new item
                cursor.execute("INSERT INTO items (name) VALUES (%s)", (item_name,))
                item_id = connection.insert_id()

                # Find or insert location
                cursor.execute("SELECT id FROM locations WHERE name = %s", (location_name,))
                location = cursor.fetchone()
                if not location:
                    cursor.execute("INSERT INTO locations (name) VALUES (%s)", (location_name,))
                    location_id = connection.insert_id()
                else:
                    location_id = location['id']

                # Associate item with location
                cursor.execute("INSERT INTO item_locations (item_id, location_id) VALUES (%s, %s)",
                               (item_id, location_id))

                connection.commit()
                flash("Donation accepted successfully!", 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()

    return render_template('accept_donation.html')
