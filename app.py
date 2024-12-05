from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # When the form is submitted, handle the POST request
        name = request.form['name']
        email = request.form['email']
        
        # Call the function to save data to the database
        save_to_db(name, email)
        
        # After saving, show a success message
        return 'Form submitted successfully!'

    # When the page is first loaded (GET request), render the form
    return render_template('form.html')

def save_to_db(name, email):
    # Connect to CockroachDB
    #coonection string- postgresql://akanksha:<ENTER-SQL-USER-PASSWORD>@wobbly-parrot-5792.j77.aws-ap-south-1.cockroachlabs.cloud:26257/testdb?sslmode=verify-full
    conn = psycopg2.connect(
        host="wobbly-parrot-5792.j77.aws-ap-south-1.cockroachlabs.cloud",
        port="26257",
        user="akanksha",
        password="qeTM73BW6GlTsYbud1bQbw",
        database="testdb"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/view')
def view_users():
    # Connect to CockroachDB
    #coonection string- postgresql://akanksha:<ENTER-SQL-USER-PASSWORD>@wobbly-parrot-5792.j77.aws-ap-south-1.cockroachlabs.cloud:26257/testdb?sslmode=verify-full
    conn = psycopg2.connect(
        host="wobbly-parrot-5792.j77.aws-ap-south-1.cockroachlabs.cloud",
        port="26257",
        user="akanksha",
        password="qeTM73BW6GlTsYbud1bQbw",
        database="testdb"
    )
    cursor = conn.cursor()
    # Query to fetch all users
    cursor.execute("SELECT name, email FROM users")
    users = cursor.fetchall()  # Fetch all the results
    
    # Close the connection
    cursor.close()
    conn.close()
    
    # Pass the users data to the HTML template
    return render_template('view_users.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)
