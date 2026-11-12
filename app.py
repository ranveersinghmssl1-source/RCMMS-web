
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash
from turtle import pd

from flask import Flask, render_template, request, redirect, send_file
import pandas
import pandas as pd
import pymysql
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, send_file, session
import pandas as pd
import pymysql

app = Flask(__name__)
app.secret_key = "RCMMS_maintenance_2026"

# ==========================
# AIVEN ONLINE DATABASE CONNECTION
# ==========================
db = pymysql.connect(
    host="ranveer-server-ranveersinghmssl1-9ed1.d.aivencloud.com",
    port=18259,
    user="avnadmin",
    password="AVNS_a3yItpgbsMKerc7-T36",  # अपना Aiven पासवर्ड यहाँ डालें
    database="defaultdb",
    autocommit=True
)

cursor = db.cursor()

# ==========================
# AUTO CREATE TABLES IN AIVEN
# ==========================
def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_master (
        id INT AUTO_INCREMENT PRIMARY KEY,
        emp_id VARCHAR(50),
        full_name VARCHAR(100),
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        department VARCHAR(50),
        role VARCHAR(50),
        mobile VARCHAR(20),
        status VARCHAR(20) DEFAULT 'ACTIVE',
        quality_access VARCHAR(10) DEFAULT 'NO',
        store_access VARCHAR(10) DEFAULT 'NO',
        maintenance_access VARCHAR(10) DEFAULT 'NO',
        lpc_access VARCHAR(10) DEFAULT 'NO',
        assy_access VARCHAR(10) DEFAULT 'NO',
        admin_access VARCHAR(10) DEFAULT 'NO'
    )
    """)

    cursor.execute("SELECT * FROM user_master WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO user_master (emp_id, full_name, username, password, department, role, status, admin_access)
        VALUES ('EMP001', 'Ranveer Singh', 'admin', '1234', 'Admin', 'Administrator', 'ACTIVE', 'YES')
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS machine_master (
        id INT AUTO_INCREMENT PRIMARY KEY,
        machine_code VARCHAR(50) UNIQUE NOT NULL,
        machine_name VARCHAR(100) NOT NULL,
        line_name VARCHAR(50),
        department VARCHAR(50),
        manufacturer VARCHAR(100),
        status VARCHAR(20) DEFAULT 'ACTIVE'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operator_master (
        id INT AUTO_INCREMENT PRIMARY KEY,
        operator_id VARCHAR(50) UNIQUE NOT NULL,
        operator_name VARCHAR(100) NOT NULL,
        department VARCHAR(50),
        shift VARCHAR(20),
        status VARCHAR(20) DEFAULT 'ACTIVE'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technician_master (
        id INT AUTO_INCREMENT PRIMARY KEY,
        technician_id VARCHAR(50) UNIQUE NOT NULL,
        technician_name VARCHAR(100) NOT NULL,
        department VARCHAR(50),
        skill VARCHAR(100),
        mobile_no VARCHAR(20),
        email VARCHAR(100),
        shift_name VARCHAR(50),
        status VARCHAR(20) DEFAULT 'ACTIVE'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spare_parts_master (
        id INT AUTO_INCREMENT PRIMARY KEY,
        part_code VARCHAR(50) UNIQUE NOT NULL,
        part_name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        current_stock INT DEFAULT 0,
        min_stock INT DEFAULT 5,
        location VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS breakdown_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        section VARCHAR(20) NOT NULL,
        machine_code VARCHAR(50) NOT NULL,
        operator_name VARCHAR(100),
        problem_description TEXT,
        breakdown_start DATETIME DEFAULT CURRENT_TIMESTAMP,
        breakdown_end DATETIME NULL,
        downtime_minutes INT DEFAULT 0,
        technician_name VARCHAR(100),
        action_taken TEXT,
        root_cause TEXT,
        spare_used VARCHAR(255),
        status VARCHAR(20) DEFAULT 'OPEN'
    )
    """)
    print("Aiven Database connected & tables ready!")

init_db()

# ==========================
# TECHNICIAN ROUTES
# ==========================
@app.route("/update_technician/<int:id>", methods=["POST"])
def update_technician(id):
    technician_id = request.form.get("technician_id")
    technician_name = request.form.get("technician_name")
    department = request.form.get("department")
    skill = request.form.get("skill")
    mobile_no = request.form.get("mobile_no")
    email = request.form.get("email")
    shift_name = request.form.get("shift_name")
    status = request.form.get("status")

    cursor.execute("""
        UPDATE technician_master
        SET technician_id=%s, technician_name=%s, department=%s, skill=%s,
            mobile_no=%s, email=%s, shift_name=%s, status=%s
        WHERE id=%s
    """, (technician_id, technician_name, department, skill, mobile_no, email, shift_name, status, id))

    flash("Technician Updated Successfully", "success")
    return redirect("/technician_master")

@app.route("/delete_technician/<int:id>")
def delete_technician(id):
    cursor.execute("DELETE FROM technician_master WHERE id=%s", (id,))
    return redirect("/technician_master")


app = Flask(__name__)

app.secret_key = "RCMMS_maintenance_2026"

@app.route("/update_technician/<int:id>", methods=["POST"])
def update_technician(id):

    technician_id = request.form.get("technician_id")
    technician_name = request.form.get("technician_name")
    department = request.form.get("department")
    skill = request.form.get("skill")
    mobile_no = request.form.get("mobile_no")
    email = request.form.get("email")
    shift_name = request.form.get("shift_name")
    status = request.form.get("status")

    cursor.execute("""
        UPDATE technician_master
        SET
            technician_id=%s,
            technician_name=%s,
            department=%s,
            skill=%s,
            mobile_no=%s,
            email=%s,
            shift_name=%s,
            status=%s
        WHERE id=%s
    """, (
        technician_id,
        technician_name,
        department,
        skill,
        mobile_no,
        email,
        shift_name,
        status,
        id
    ))

    db.commit()

    flash("Technician Updated Successfully", "success")

    return redirect("/technician_master")

@app.route("/delete_technician/<int:id>")
def delete_technician(id):

    cursor.execute(
        "DELETE FROM technician_master WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/technician_master")


# ==========================
# DATABASE CONNECTION
# ==========================

db = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="maintenance_system"
)

cursor = db.cursor()

# ==========================
# LOGIN PAGE
# ==========================
from flask import session
@app.route("/")
def home():
    return render_template("login.html")

# ==========================
# LOGIN VALIDATION
# ==========================

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("""

        SELECT *

        FROM user_master

        WHERE username=%s
        AND password=%s
        AND status='ACTIVE'

    """,(username,password))

    user = cursor.fetchone()

    if user:

        session["quality_access"] = user[9]
        session["store_access"] = user[10]
        session["maintenance_access"] = user[11]
        session["lpc_access"] = user[12]
        session["assy_access"] = user[13]
        session["admin_access"] = user[14]

        # AUTO REDIRECT BY ACCESS

        if session["admin_access"] == "YES":

            return redirect("/admin")

        elif session["quality_access"] == "YES":

            return redirect("/quality_dashboard")

        elif session["store_access"] == "YES":

            return redirect("/store_dashboard")

        elif session["maintenance_access"] == "YES":

            return redirect("/maintenance")

        elif session["lpc_access"] == "YES":

            return redirect("/lpc")

        elif session["assy_access"] == "YES":

            return redirect("/assy")

        else:

            return """
            <h2>No Module Assigned</h2>
            <a href='/'>Back To Login</a>
            """

    return """
    <h2 style='color:red;'>

    Invalid User Name Or Password

    </h2>

    <br>

    <a href='/'>
    Back To Login
    </a>

    """
# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route("/admin")
def admin():

    # Total Machines
    cursor.execute("SELECT COUNT(*) FROM machine_master")
    total_machine = cursor.fetchone()[0]

    # Total Operators
    cursor.execute("SELECT COUNT(*) FROM operator_master")
    total_operator = cursor.fetchone()[0]

    # Total Technicians
    cursor.execute("SELECT COUNT(*) FROM technician_master")
    total_technician = cursor.fetchone()[0]

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM user_master")
    total_user = cursor.fetchone()[0]

    # Total Breakdown
    cursor.execute("SELECT COUNT(*) FROM lpc_breakdown")
    total_breakdown = cursor.fetchone()[0]

    # Open Breakdown
    cursor.execute(
        "SELECT COUNT(*) FROM lpc_breakdown WHERE status='OPEN'"
    )
    open_breakdown = cursor.fetchone()[0]

    # Closed Breakdown
    cursor.execute(
        "SELECT COUNT(*) FROM maintenance_action WHERE status='CLOSED'"
    )
    closed_breakdown = cursor.fetchone()[0]

    # Low Stock Alert
    cursor.execute("""
    SELECT
        part_no,
        part_name,
        current_stock,
        minimum_stock
    FROM spare_master
    WHERE current_stock <= minimum_stock
    """)

    low_stock_items = cursor.fetchall()

    low_stock_count = len(low_stock_items)

    return render_template(
        "admin_dashboard.html",

        total_machine=total_machine,
        total_operator=total_operator,
        total_technician=total_technician,
        total_user=total_user,

        total_breakdown=total_breakdown,
        open_breakdown=open_breakdown,
        closed_breakdown=closed_breakdown,

        low_stock_count=low_stock_count,
        low_stock_items=low_stock_items
    )
# ==========================
# MAINTENANCE DASHBOARD
# ==========================

@app.route("/maintenance")
def maintenance():

    return render_template(
        "Assy_Dashboard.html"
    )
# ==========================
# MAINTENANCE DASHBOARD
# ==========================

@app.route("/maintenance_dashboard")
def maintenance_dashboard():

    # Total LPC Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM lpc_breakdown
    """)
    total_lpc = cursor.fetchone()[0]

    # Total ASSY Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_breakdown
    """)
    total_assy = cursor.fetchone()[0]

    # Open Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM lpc_breakdown
    WHERE status='OPEN'
    """)
    open_breakdown = cursor.fetchone()[0]

    # Closed Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM lpc_breakdown
    WHERE status='CLOSED'
    """)
    closed_breakdown = cursor.fetchone()[0]

    # Spare Issue

    cursor.execute("""
    SELECT COUNT(*)
    FROM spare_issue
    """)
    total_issue = cursor.fetchone()[0]

    # Spare Receive

    cursor.execute("""
    SELECT COUNT(*)
    FROM spare_receive
    """)
    total_receive = cursor.fetchone()[0]

    # Total Spares

    total_spares = total_issue + total_receive

    # Low Stock

    cursor.execute("""
    SELECT COUNT(*)
    FROM spare_master
    WHERE current_stock <= minimum_stock
    """)
    low_stock = cursor.fetchone()[0]

    # Total Breakdown

    total_breakdown = total_lpc

    # =====================
    # CLOSURE RATE
    # =====================

    if total_breakdown > 0:

        closure_rate = round(
            (closed_breakdown / total_breakdown) * 100,
            2
        )

    else:

        closure_rate = 0

    # =====================
    # MTTR
    # =====================

    cursor.execute("""
    SELECT IFNULL(SUM(down_time),0)
    FROM maintenance_action
    """)

    total_downtime = cursor.fetchone()[0]

    if total_breakdown > 0:

        mttr = round(
            total_downtime / total_breakdown,
            2
        )

    else:

        mttr = 0

    # =====================
    # MTBF
    # =====================

    running_hours = 720

    if total_breakdown > 0:

        mtbf = round(
            running_hours / total_breakdown,
            2
        )

    else:

        mtbf = 0

    # =====================
    # TOP TECHNICIAN
    # =====================

    cursor.execute("""
    SELECT
        technician_name,
        COUNT(*) as total_jobs
    FROM maintenance_action
    GROUP BY technician_name
    ORDER BY total_jobs DESC
    LIMIT 1
    """)

    top_tech = cursor.fetchone()

    if top_tech is None:
        top_tech = ("N/A", 0)

    # =====================
    # CRITICAL MACHINE
    # =====================

    cursor.execute("""
    SELECT
        machine_name,
        COUNT(*) as total_bd
    FROM lpc_breakdown
    GROUP BY machine_name
    ORDER BY total_bd DESC
    LIMIT 1
    """)

    critical_machine = cursor.fetchone()

    if critical_machine is None:
        critical_machine = ("N/A", 0)

    # =====================
    # RECENT BREAKDOWN
    # =====================

    cursor.execute("""
    SELECT
        ticket_no,
        machine_name,
        problem_type,
        status
    FROM lpc_breakdown
    ORDER BY ticket_no DESC
    LIMIT 10
    """)

    recent_breakdown = cursor.fetchall()

    # =====================
    # BREAKDOWN TRACKING
    # =====================

    cursor.execute("""
    SELECT
        machine_name,
        ticket_no,
        status,
        breakdown_time,
        problem_type,
        operator_name
    FROM lpc_breakdown
    WHERE status='OPEN'
    ORDER BY ticket_no DESC
    LIMIT 20
    """)

    breakdown_tracking = cursor.fetchall()

    # =====================
    # RCA COUNT
    # =====================

    total_rca = 0

    return render_template(

        "maintenance_dashboard.html",

        total_lpc=total_lpc,
        total_assy=total_assy,

        open_breakdown=open_breakdown,
        closed_breakdown=closed_breakdown,

        total_breakdown=total_breakdown,

        low_stock=low_stock,

        mttr=mttr,
        mtbf=mtbf,

        closure_rate=closure_rate,

        total_rca=total_rca,

        top_tech=top_tech,

        critical_machine=critical_machine,

        total_spares=total_spares,

        recent_breakdown=recent_breakdown,

        breakdown_tracking=breakdown_tracking

    )
# ==========================
# MACHINE MASTER
# ==========================

@app.route("/machine_master")
def machine_master():

    search_text = request.args.get("search_text", "")

    if search_text:

        cursor.execute("""
        SELECT
        machine_code,
        machine_name,
        department,
        line_name,
        machine_type,
        make_name,
        status
        FROM machine_master
        WHERE machine_code LIKE %s
        OR machine_name LIKE %s
        OR department LIKE %s
        OR machine_type LIKE %s
        ORDER BY machine_code
        """,
        (
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%"
        ))

    else:

        cursor.execute("""
        SELECT
        machine_code,
        machine_name,
        department,
        line_name,
        machine_type,
        make_name,
        status
        FROM machine_master
        ORDER BY machine_code
        """)

    machine_data = cursor.fetchall()

    return render_template(
        "machine_master.html",
        machine_data=machine_data
    )
@app.route("/save_machine", methods=["POST"])
def save_machine():

    machine_code = request.form["machine_code"]
    machine_name = request.form["machine_name"]
    department = request.form["department"]
    line_name = request.form["line_name"]
    machine_type = request.form["machine_type"]
    make_name = request.form["make_name"]
    model_no = request.form["model_no"]
    serial_no = request.form["serial_no"]
    installation_date = request.form["installation_date"]
    status = request.form["status"]

    cursor.execute("""
    INSERT INTO machine_master
    (
        machine_code,
        machine_name,
        machine_type,
        department,
        line_name,
        make_name,
        model_no,
        serial_no,
        installation_date,
        status
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        machine_code,
        machine_name,
        machine_type,
        department,
        line_name,
        make_name,
        model_no,
        serial_no,
        installation_date,
        status
    ))

    db.commit()

    return redirect("/machine_master")

# ==========================
# EDIT MACHINE
# ==========================

@app.route("/edit_technician/<int:id>")
def edit_technician(id):

    cursor.execute(
        "SELECT * FROM technician_master WHERE id=%s",
        (id,)
    )

    technician = cursor.fetchone()

    return render_template(
        "edit_technician.html",
        technician=technician
    )
    machine_data = cursor.fetchone()

    return render_template(
        "edit_machine.html",
        machine_data=machine_data
    )

# ==========================
# UPDATE MACHINE
# ==========================

@app.route("/update_machine", methods=["POST"])
def update_machine():

    machine_code = request.form["machine_code"]
    machine_name = request.form["machine_name"]
    department = request.form["department"]
    line_name = request.form["line_name"]
    machine_type = request.form["machine_type"]
    make_name = request.form["make_name"]
    status = request.form["status"]

    cursor.execute("""
    UPDATE machine_master
    SET
    machine_name=%s,
    department=%s,
    line_name=%s,
    machine_type=%s,
    make_name=%s,
    status=%s
    WHERE machine_code=%s
    """,
    (
        machine_name,
        department,
        line_name,
        machine_type,
        make_name,
        status,
        machine_code
    ))

    db.commit()

    return redirect("/machine_master")

# ==========================
# DELETE MACHINE
# ==========================

@app.route("/delete_machine/<machine_code>")
def delete_machine(machine_code):

    cursor.execute("""
    DELETE FROM machine_master
    WHERE machine_code=%s
    """, (machine_code,))

    db.commit()

    return redirect("/machine_master")

@app.route("/technician_master")
def technician_master():

    search = request.args.get("search", "")

    if search:
        cursor.execute("""
            SELECT *
            FROM technician_master
            WHERE technician_id LIKE %s
            OR technician_name LIKE %s
            OR department LIKE %s
        """,
        ('%' + search + '%',
         '%' + search + '%',
         '%' + search + '%'))
    else:
        cursor.execute("""
            SELECT * FROM technician_master
            ORDER BY id DESC
        """)

    technicians = cursor.fetchall()

    return render_template(
        "technician_master.html",
        technicians=technicians
    )


@app.route("/save_technician", methods=["POST"])
def save_technician():

    technician_id = request.form["technician_id"].strip()
    technician_name = request.form["technician_name"].strip()
    department = request.form["department"].strip()
    skill = request.form["skill"].strip()

    if not technician_id or not technician_name:
        flash("Technician ID and Name Required!", "danger")
        return redirect("/technician_master")

    cursor.execute("""
        INSERT INTO technician_master
        (technician_id, technician_name, department,
         skill, mobile_no, email, shift_name, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        technician_id,
        technician_name,
        department,
        skill,
        request.form["mobile_no"],
        request.form["email"],
        request.form["shift_name"],
        request.form["status"]
    ))

    db.commit()

    flash("Technician Saved Successfully", "success")

    return redirect("/technician_master")
# ==========================
# PROBLEM MASTER
# ==========================

@app.route("/problem_master")
def problem_master():

    search_text = request.args.get("search_text", "")

    if search_text:

        cursor.execute("""
        SELECT
        problem_code,
        problem_name,
        department,
        category,
        priority,
        status
        FROM problem_master
        WHERE problem_code LIKE %s
        OR problem_name LIKE %s
        ORDER BY problem_code
        """,
        (
            "%" + search_text + "%",
            "%" + search_text + "%"
        ))

    else:

        cursor.execute("""
        SELECT
        problem_code,
        problem_name,
        department,
        category,
        priority,
        status
        FROM problem_master
        ORDER BY problem_code
        """)

    problem_data = cursor.fetchall()

    return render_template(
        "problem_master.html",
        problem_data=problem_data
    )
@app.route("/save_problem", methods=["POST"])
def save_problem():

    problem_code = request.form["problem_code"]
    problem_name = request.form["problem_name"]
    department = request.form["department"]
    category = request.form["category"]
    priority = request.form["priority"]
    description = request.form["description"]
    status = request.form["status"]

    cursor.execute("""
    INSERT INTO problem_master
    (
        problem_code,
        problem_name,
        department,
        category,
        priority,
        description,
        status
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        problem_code,
        problem_name,
        department,
        category,
        priority,
        description,
        status
    ))

    db.commit()

    return redirect("/problem_master")

# ==========================
# EDIT PROBLEM
# ==========================

@app.route("/edit_problem/<problem_code>")
def edit_problem(problem_code):

    cursor.execute("""
    SELECT
    problem_code,
    problem_name,
    department,
    category,
    priority,
    description,
    status
    FROM problem_master
    WHERE problem_code=%s
    """, (problem_code,))

    problem_data = cursor.fetchone()

    return render_template(
        "edit_problem.html",
        problem_data=problem_data
    )
# ==========================
# Update Problem
# ==========================
@app.route("/update_problem", methods=["POST"])
def update_problem():

    problem_code = request.form["problem_code"]
    problem_name = request.form["problem_name"]

    cursor.execute("""
    UPDATE problem_master
    SET
    problem_name=%s
    WHERE problem_code=%s
    """,
    (
        problem_name,
        problem_code
    ))

    db.commit()

    return redirect("/problem_master")
# ==========================
# Delete Problem
# ==========================
@app.route("/delete_problem/<problem_code>")
def delete_problem(problem_code):

    cursor.execute("""
    DELETE FROM problem_master
    WHERE problem_code=%s
    """,
    (problem_code,))

    db.commit()

    return redirect("/problem_master")

# ==========================
# APPLICATOR MASTER
# ==========================

@app.route("/applicator_master")
def applicator_master():

    search = request.args.get("search", "")

    if search:

        cursor.execute("""
            SELECT *
            FROM applicator_master
            WHERE applicator_no LIKE %s
            OR applicator_name LIKE %s
            OR machine_name LIKE %s
            OR terminal_part_no LIKE %s
            ORDER BY id DESC
        """, (
            '%' + search + '%',
            '%' + search + '%',
            '%' + search + '%',
            '%' + search + '%'
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM applicator_master
            ORDER BY id DESC
        """)

    applicators = cursor.fetchall()

    return render_template(
        "applicator_master.html",
        applicators=applicators
    )


@app.route("/save_applicator", methods=["POST"])
def save_applicator():

    applicator_no = request.form["applicator_no"].strip()
    applicator_name = request.form["applicator_name"].strip()

    if not applicator_no or not applicator_name:

        flash(
            "Applicator No and Name Required",
            "danger"
        )

        return redirect("/applicator_master")

    cursor.execute("""
        INSERT INTO applicator_master
        (
            applicator_no,
            applicator_name,
            machine_name,
            terminal_part_no,
            store_location,
            rack_no,
            bin_no,
            last_maintenance_date,
            applicator_life,
            status
        )
        VALUES
        (
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s
        )
    """, (

        request.form["applicator_no"],
        request.form["applicator_name"],
        request.form["machine_name"],
        request.form["terminal_part_no"],
        request.form["store_location"],
        request.form["rack_no"],
        request.form["bin_no"],
        request.form["last_maintenance_date"],
        request.form["applicator_life"],
        request.form["status"]

    ))

    db.commit()

    flash(
        "Applicator Saved Successfully",
        "success"
    )

    return redirect("/applicator_master")

@app.route("/edit_applicator/<int:id>")
def edit_applicator(id):

    cursor.execute(
        "SELECT * FROM applicator_master WHERE id=%s",
        (id,)
    )

    applicator = cursor.fetchone()

    return render_template(
        "edit_applicator.html",
        applicator=applicator
    )

@app.route("/update_applicator/<int:id>", methods=["POST"])
def update_applicator(id):

    cursor.execute("""
        UPDATE applicator_master
        SET
            applicator_no=%s,
            applicator_name=%s,
            machine_name=%s,
            terminal_part_no=%s,
            store_location=%s,
            rack_no=%s,
            bin_no=%s,
            last_maintenance_date=%s,
            applicator_life=%s,
            status=%s
        WHERE id=%s""", (

        request.form["applicator_no"],
        request.form["applicator_name"],
        request.form["machine_name"],
        request.form["terminal_part_no"],
        request.form["store_location"],
        request.form["rack_no"],
        request.form["bin_no"],
        request.form["last_maintenance_date"],
        request.form["applicator_life"],
        request.form["status"],
        id
    ))

    db.commit()

    flash(
        "Applicator Updated Successfully",
        "success"
    )

    return redirect("/applicator_master")

@app.route("/upload_applicator_excel", methods=["POST"])
def upload_applicator_excel():

    file = request.files["excel_file"]

    if file.filename != "":

        df = pd.read_excel(file)

        df = df.fillna("")

        for index, row in df.iterrows():

            cursor.execute("""
                INSERT INTO applicator_master
                (
                    applicator_no,
                    applicator_name,
                    machine_name,
                    terminal_part_no,
                    store_location,
                    rack_no,
                    bin_no,
                    last_maintenance_date,
                    applicator_life,
                    status
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (

                row["Applicator No"],
                row["Applicator Name"],
                row["Machine Name"],
                row["Terminal Part No"],
                row["Store Location"],
                row["Rack No"],
                row["Bin No"],
                None,
                row["Applicator Life"],
                row["Status"]

            ))

        db.commit()

    flash("Excel Uploaded Successfully", "success")

    return redirect("/applicator_master")

@app.route("/export_applicator_excel")
def export_applicator_excel():

    cursor.execute("""
        SELECT
            applicator_no,
            applicator_name,
            machine_name,
            terminal_part_no,
            store_location,
            rack_no,
            bin_no,
            last_maintenance_date,
            applicator_life,
            status
        FROM applicator_master
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[
        "Applicator No",
        "Applicator Name",
        "Machine Name",
        "Terminal Part No",
        "Store Location",
        "Rack No",
        "Bin No",
        "Last Maintenance Date",
        "Applicator Life",
        "Status"
    ])

    file_name = "Applicator_Master.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
@app.route("/download_applicator_template")
def download_applicator_template():

    df = pd.DataFrame(columns=[
        "Applicator No",
        "Applicator Name",
        "Machine Name",
        "Terminal Part No",
        "Store Location",
        "Rack No",
        "Bin No",
        "Last Maintenance Date",
        "Applicator Life",
        "Status"
    ])

    file_name = "Applicator_Template.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
@app.route("/delete_applicator/<int:id>")
def delete_applicator(id):

    cursor.execute(
        "DELETE FROM applicator_master WHERE id=%s",
        (id,)
    )

    db.commit()

    flash(
        "Applicator Deleted Successfully",
        "success"
    )

    return redirect("/applicator_master")

# ==========================
# TERMINAL MASTER
# ==========================

@app.route("/terminal_master")
def terminal_master():

    search = request.args.get("search", "")

    if search:

        cursor.execute("""
            SELECT *
            FROM terminal_master
            WHERE terminal_part_no LIKE %s
            OR terminal_name LIKE %s
            OR supplier LIKE %s
            OR machine_name LIKE %s
            ORDER BY id DESC
        """,(

            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"

        ))

    else:

        cursor.execute("""
            SELECT *
            FROM terminal_master
            ORDER BY id DESC
        """)

    terminals = cursor.fetchall()

    return render_template(
        "terminal_master.html",
        terminals=terminals
    )


@app.route("/save_terminal", methods=["POST"])
def save_terminal():

    cursor.execute("""
        INSERT INTO terminal_master
        (
            terminal_part_no,
            terminal_name,
            supplier,
            machine_name,
            store_location,
            rack_no,
            bin_no,
            current_stock,
            minimum_stock,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,(

        request.form["terminal_part_no"],
        request.form["terminal_name"],
        request.form["supplier"],
        request.form["machine_name"],
        request.form["store_location"],
        request.form["rack_no"],
        request.form["bin_no"],
        request.form["current_stock"],
        request.form["minimum_stock"],
        request.form["status"]

    ))

    db.commit()

    flash(
        "Terminal Saved Successfully",
        "success"
    )

    return redirect("/terminal_master")


@app.route("/edit_terminal/<int:id>")
def edit_terminal(id):

    cursor.execute(
        "SELECT * FROM terminal_master WHERE id=%s",
        (id,)
    )

    terminal = cursor.fetchone()

    return render_template(
        "edit_terminal.html",
        terminal=terminal
    )


@app.route("/update_terminal/<int:id>", methods=["POST"])
def update_terminal(id):

    cursor.execute("""
        UPDATE terminal_master
        SET
            terminal_part_no=%s,
            terminal_name=%s,
            supplier=%s,
            machine_name=%s,
            store_location=%s,
            rack_no=%s,
            bin_no=%s,
            current_stock=%s,
            minimum_stock=%s,
            status=%s
        WHERE id=%s
    """,(

        request.form["terminal_part_no"],
        request.form["terminal_name"],
        request.form["supplier"],
        request.form["machine_name"],
        request.form["store_location"],
        request.form["rack_no"],
        request.form["bin_no"],
        request.form["current_stock"],
        request.form["minimum_stock"],
        request.form["status"],
        id

    ))

    db.commit()

    flash(
        "Terminal Updated Successfully",
        "success"
    )

    return redirect("/terminal_master")


@app.route("/delete_terminal/<int:id>")
def delete_terminal(id):

    cursor.execute(
        "DELETE FROM terminal_master WHERE id=%s",
        (id,)
    )

    db.commit()

    flash(
        "Terminal Deleted Successfully",
        "success"
    )

    return redirect("/terminal_master")


@app.route("/download_terminal_template")
def download_terminal_template():

    df = pd.DataFrame(columns=[

        "Terminal Part No",
        "Terminal Name",
        "Supplier",
        "Machine Name",
        "Store Location",
        "Rack No",
        "Bin No",
        "Current Stock",
        "Minimum Stock",
        "Status"

    ])

    file_name = "Terminal_Template.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )


@app.route("/upload_terminal_excel", methods=["POST"])
def upload_terminal_excel():

    file = request.files["excel_file"]

    if file.filename != "":

        df = pd.read_excel(file)

        df = df.fillna("")

        for index, row in df.iterrows():

            cursor.execute("""
                INSERT INTO terminal_master
                (
                    terminal_part_no,
                    terminal_name,
                    supplier,
                    machine_name,
                    store_location,
                    rack_no,
                    bin_no,
                    current_stock,
                    minimum_stock,
                    status
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                row["Terminal Part No"],
                row["Terminal Name"],
                row["Supplier"],
                row["Machine Name"],
                row["Store Location"],
                row["Rack No"],
                row["Bin No"],
                row["Current Stock"],
                row["Minimum Stock"],
                row["Status"]
            ))

        db.commit()

        flash(
            "Terminals Uploaded Successfully",
            "success"
        )

    return redirect("/terminal_master")

@app.route("/export_terminal_excel")
def export_terminal_excel():

    cursor.execute("""
        SELECT
            terminal_part_no,
            terminal_name,
            supplier,
            machine_name,
            store_location,
            rack_no,
            bin_no,
            current_stock,
            minimum_stock,
            status
        FROM terminal_master
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[
        "Terminal Part No",
        "Terminal Name",
        "Supplier",
        "Machine Name",
        "Store Location",
        "Rack No",
        "Bin No",
        "Current Stock",
        "Minimum Stock",
        "Status"
    ])

    file_name = "Terminal_Master.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
# ==========================
# LPC BREAKDOWN
# ==========================

# ==========================
# LPC FORM
# ==========================

@app.route("/lpc")
def lpc():
    from datetime import datetime

    today = datetime.now().strftime("%Y%m%d")

    cursor.execute("""
SELECT MAX(ticket_no)
FROM lpc_breakdown
WHERE ticket_no LIKE %s
""", (f"LPC-{today}-%",))

    last_ticket = cursor.fetchone()[0]

    if last_ticket:

        last_no = int(last_ticket.split("-")[-1])

        new_no = last_no + 1

    else:

        new_no = 1

    ticket_no = f"LPC-{today}-{new_no:03d}"
    return render_template(
        "lpc_FORM.html",
        ticket_no=ticket_no
    )


@app.route("/save_lpc", methods=["POST"])
def save_lpc():

    try:

        ticket_no = request.form.get("ticket_no")
        breakdown_date = request.form.get("breakdown_date")
        shift_name = request.form.get("shift_name")
        operator_name = request.form.get("operator_name")
        employee_id = request.form.get("employee_id")
        line_name = request.form.get("line_name")
        machine_name = request.form.get("machine_name")

        breakdown_time = request.form.get("breakdown_time")

        applicator_no = request.form.get("applicator_no")
        terminal_part_no = request.form.get("terminal_part_no")
        problem_type = request.form.get("problem_type")
        description = request.form.get("description")

        status = "OPEN"

        sql = """
        INSERT INTO lpc_breakdown
        (
            ticket_no,
            breakdown_date,
            shift_name,
            operator_name,
            employee_id,
            line_name,
            machine_name,
            breakdown_time,
            applicator_no,
            terminal_part_no,
            problem_type,
            description,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                ticket_no,
                breakdown_date,
                shift_name,
                operator_name,
                employee_id,
                line_name,
                machine_name,
                breakdown_time,
                applicator_no,
                terminal_part_no,
                problem_type,
                description,
                status
            )
        )

        db.commit()

        return """
        <h2>LPC Breakdown Saved Successfully</h2>

        <br>

        <a href="/lpc">
        Back To LPC Form
        </a>

        <br><br>

        <a href="/admin">
        Back To Dashboard
        </a>
        """

    except Exception as e:

        return f"ERROR : {e}"
# ==========================
# MATERIAL REQUEST FORM
# ==========================

from datetime import datetime
from flask import render_template, request, redirect, flash

@app.route("/material_request", methods=["GET", "POST"])
def material_request():

    # ==========================
    # AUTO REQUEST NUMBER
    # ==========================

    request_date = datetime.now().strftime("%Y-%m-%d")

    request_time = datetime.now().strftime("%H:%M:%S")

    today = datetime.now().strftime("%Y%m%d")

    cursor.execute("""
        SELECT COUNT(*)
        FROM material_request
        WHERE request_date = CURDATE()
    """)

    today_count = cursor.fetchone()[0] + 1

    request_no = f"LPC-MR-{today}-{today_count:04d}"

    # ==========================
    # SAVE REQUEST
    # ==========================

    if request.method == "POST":

        request_no = request.form["request_no"]

        request_date = request.form["request_date"]

        request_time = request.form["request_time"]

        shift_name = request.form["shift_name"]

        machine_name = request.form["machine_name"]

        operator_name = request.form["operator_name"]

        line_name = request.form["line_name"]

        priority = request.form["priority"]

        material_type = request.form["material_type"]

        part_no = request.form["part_no"]

        required_qty = request.form["required_qty"]

        urgency = request.form["urgency"]

        reason = request.form["reason"]

        cursor.execute("""

            INSERT INTO material_request(

                request_no,

                request_date,

                request_time,

                shift_name,

                machine_name,

                operator_name,

                line_name,

                priority,

                material_type,

                part_no,

                required_qty,

                urgency,

                reason,

                status

            )

            VALUES(

                %s,%s,%s,%s,%s,%s,%s,%s,

                %s,%s,%s,%s,%s,

                'OPEN'

            )

        """,

        (

            request_no,

            request_date,

            request_time,

            shift_name,

            machine_name,

            operator_name,

            line_name,

            priority,

            material_type,

            part_no,

            required_qty,

            urgency,

            reason

        ))

        db.commit()

        flash("✅ Material Request Sent Successfully")

        return redirect("/material_request")

    # ==========================
    # REQUEST HISTORY
    # ==========================

    cursor.execute("""

        SELECT

            request_no,

            machine_name,

            material_type,

            part_no,

            required_qty,

            priority,

            status

        FROM material_request

        ORDER BY id DESC

        LIMIT 20

    """)

    material_requests = cursor.fetchall()

    # ==========================
    # OPEN PAGE
    # ==========================

    return render_template(

        "material_request.html",

        request_no=request_no,

        request_date=request_date,

        request_time=request_time,

        material_requests=material_requests

    )
# ==========================
# STORE DASHBOARD
# ==========================

@app.route("/store_dashboard")
def store_dashboard():

    cursor.execute("""
    SELECT COUNT(*)
    FROM material_request
    WHERE status='OPEN'
    """)
    open_request = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM material_request
    WHERE status='APPROVED'
    """)
    approved_request = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM material_request
    WHERE status='ISSUED'
    """)
    issued_request = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM material_request
    WHERE status='REJECTED'
    """)
    rejected_request = cursor.fetchone()[0]

    cursor.execute("""
    SELECT
        id,
        request_no,
        request_date,
        machine_name,
        material_type,
        part_no,
        required_qty,
        priority,
        status
    FROM material_request
    ORDER BY id DESC
    """)

    requests = cursor.fetchall()

    return render_template(
        "store_dashboard.html",
        requests=requests,
        open_request=open_request,
        approved_request=approved_request,
        issued_request=issued_request,
        rejected_request=rejected_request
    )
@app.route("/approve_request/<int:id>")
def approve_request(id):

    cursor.execute("""
    UPDATE material_request
    SET status='APPROVED'
    WHERE id=%s
    """,(id,))

    db.commit()

    flash("Request Approved Successfully")

    return redirect("/store_dashboard")
@app.route("/issue_request/<int:id>")
def issue_request(id):

    cursor.execute("""

    UPDATE material_request

    SET status='ISSUED'

    WHERE id=%s

    """,(id,))

    db.commit()

    return redirect("/store_dashboard")

@app.route("/material_issue", methods=["GET","POST"])
def material_issue():

    issue_date = datetime.now().strftime("%Y-%m-%d")

    today = datetime.now().strftime("%Y%m%d")

    cursor.execute("""
    SELECT COUNT(*)
    FROM material_issue
    WHERE issue_date = CURDATE()
    """)

    issue_count = cursor.fetchone()[0] + 1

    issue_no = f"ISS-{today}-{issue_count:03d}"

    if request.method == "POST":

        request_no = request.form["request_no"]

        machine_name = request.form["machine_name"]

        material_type = request.form["material_type"]

        part_no = request.form["part_no"]

        requested_qty = request.form["requested_qty"]

        issue_qty = request.form["issue_qty"]

        issued_by = request.form["issued_by"]

        remarks = request.form["remarks"]

        cursor.execute("""

        INSERT INTO material_issue(

        issue_no,
        issue_date,
        request_no,
        machine_name,
        material_type,
        part_no,
        requested_qty,
        issue_qty,
        issued_by,
        remarks

        )

        VALUES(

        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s

        )

        """,

        (

        issue_no,
        issue_date,
        request_no,
        machine_name,
        material_type,
        part_no,
        requested_qty,
        issue_qty,
        issued_by,
        remarks

        ))

        db.commit()

        flash("Material Issued Successfully")

        return redirect("/material_issue")

    return render_template(

        "material_issue.html",

        issue_no=issue_no,

        issue_date=issue_date

    )
    
# ==========================
# ASSY FORM
# ==========================

@app.route("/assy")
def assy():
    from datetime import datetime

    today = datetime.now().strftime("%Y%m%d")

    cursor.execute("""
SELECT COUNT(*)
FROM assy_breakdown
WHERE DATE(breakdown_date)=CURDATE()
""")

    count = cursor.fetchone()[0] + 1

    ticket_no = f"ASSY-{today}-{count:03d}"

    return render_template("assy_form.html", ticket_no=ticket_no)

@app.route("/save_assy", methods=["POST"])
def save_assy():

    try:

        ticket_no = request.form["ticket_no"]
        breakdown_date = request.form["breakdown_date"]
        shift_name = request.form["shift_name"]
        operator_name = request.form["operator_name"]
        employee_id = request.form["employee_id"]
        line_name = request.form["line_name"]
        machine_name = request.form["machine_name"]
        breakdown_time = request.form["breakdown_time"]
        problem_type = request.form["problem_type"]
        description = request.form["description"]
        status = request.form["status"]

        sql = """
        INSERT INTO assy_breakdown
        (
            ticket_no,
            breakdown_date,
            shift_name,
            operator_name,
            employee_id,
            line_name,
            machine_name,
            breakdown_time,
            problem_type,
            description,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                ticket_no,
                breakdown_date,
                shift_name,
                operator_name,
                employee_id,
                line_name,
                machine_name,
                breakdown_time,
                problem_type,
                description,
                status
            )
        )

        db.commit()

        return """
        <h2>✅ ASSY Breakdown Saved Successfully</h2>

        <a href="/assy">
        Back To ASSY Form
        </a>
        """

    except Exception as e:

        return f"ERROR : {e}"
# ==========================
# MAINTENANCE ACTION
# ==========================

@app.route("/maintenance_action")
def maintenance_action():

    cursor.execute("""
    SELECT
    ticket_no,
    machine_name,
    problem_type,
    breakdown_date,
    breakdown_time
    FROM lpc_breakdown
    WHERE status='OPEN'
    """)

    open_breakdowns = cursor.fetchall()

    return render_template(
        "maintenance_action.html",
        open_breakdowns=open_breakdowns
    )

# ==========================
# SAVE MAINTENANCE ACTION
# ==========================

@app.route("/save_maintenance", methods=["POST"])
def save_maintenance():

    try:

        ticket_no = request.form.get("ticket_no")
        machine_name = request.form.get("machine_name")
        problem_type = request.form.get("problem_type")

        root_cause = request.form.get("root_cause")
        action_taken = request.form.get("action_taken")

        technician_name = request.form.get("technician_name")

        part_used = request.form.get("part_used")

        qty_used = request.form.get("qty_used", "0")

        if qty_used == "":
         qty_used = 0

        down_time = request.form.get("down_time", "0")

        if down_time == "":
         down_time = 0

        remarks = request.form.get("remarks")

        status = request.form.get("status")

        sql = """
        INSERT INTO maintenance_action
        (
            ticket_no,
            machine_name,
            problem_type,
            root_cause,
            action_taken,
            technician_name,
            part_used,
            qty_used,
            down_time,
            remarks,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                ticket_no,
                machine_name,
                problem_type,
                root_cause,
                action_taken,
                technician_name,
                part_used,
                qty_used,
                down_time,
                remarks,
                status
            )
        )

        # CLOSE BREAKDOWN

        cursor.execute("""
        UPDATE lpc_breakdown
        SET status='CLOSED'
        WHERE ticket_no=%s
        """, (ticket_no,))

        db.commit()

        return """
        <h2>✅ Maintenance Action Saved Successfully</h2>

        <br>

        <a href="/maintenance_action">
        Back To Maintenance Action
        </a>

        <br><br>

        <a href="/maintenance">
        Back To Dashboard
        </a>
        """

    except Exception as e:

        return f"ERROR : {e}"

    # ==========================
# MAINTENANCE HISTORY
# ==========================

@app.route("/maintenance_history")
def maintenance_history():

    cursor.execute("""
    SELECT
    ticket_no,
    machine_name,
    problem_type,
    technician_name,
    down_time,
    status
    FROM maintenance_action
    ORDER BY ticket_no DESC
    """)

    history_data = cursor.fetchall()

    return render_template(
        "maintenance_history.html",
        history_data=history_data
    )
# ==========================
# RCA
# ==========================

@app.route("/rca")
def rca():
    return render_template("rca_form.html")

@app.route("/save_rca", methods=["POST"])
def save_rca():

    try:

        ticket_no = request.form["ticket_no"]
        machine_name = request.form["machine_name"]
        problem_type = request.form["problem_type"]
        root_cause = request.form["root_cause"]
        corrective_action = request.form["corrective_action"]
        countermeasure = request.form["countermeasure"]
        responsible_person = request.form["responsible_person"]
        part_used = request.form["part_used"]
        part_number = request.form["part_number"]

        qty_used = request.form.get("qty_used", "0")
        if qty_used == "":
            qty_used = 0

        down_time = request.form.get("down_time", "0")
        if down_time == "":
            down_time = 0

        remarks = request.form["remarks"]
        status = request.form["status"]

        sql = """
        INSERT INTO rca_master
        (
            ticket_no,
            machine_name,
            problem_type,
            root_cause,
            corrective_action,
            countermeasure,
            responsible_person,
            part_used,
            part_number,
            qty_used,
            down_time,
            remarks,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                ticket_no,
                machine_name,
                problem_type,
                root_cause,
                corrective_action,
                countermeasure,
                responsible_person,
                part_used,
                part_number,
                qty_used,
                down_time,
                remarks,
                status
            )
        )

        db.commit()

        return """
        <h2>✅ RCA Saved Successfully</h2>

        <a href="/rca">
        Back To RCA Form
        </a>
        """

    except Exception as e:

        return f"ERROR : {e}"
    

# ==========================
# REPORTS
# ==========================

@app.route("/reports", methods=["GET","POST"])
def reports():

    if request.method == "POST":

        from_date = request.form["from_date"]
        to_date = request.form["to_date"]

        cursor.execute("""
        SELECT
        ticket_no,
        breakdown_date,
        machine_name,
        problem_type,
        status
        FROM lpc_breakdown
        WHERE breakdown_date
        BETWEEN %s AND %s
        ORDER BY breakdown_date DESC
        """,
        (
            from_date,
            to_date
        ))

        report_data = cursor.fetchall()

    else:

        cursor.execute("""
        SELECT
        ticket_no,
        breakdown_date,
        machine_name,
        problem_type,
        status
        FROM lpc_breakdown
        ORDER BY breakdown_date DESC
        """)

        report_data = cursor.fetchall()

    # Daily Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM lpc_breakdown
    WHERE breakdown_date = CURDATE()
    """)

    daily_count = cursor.fetchone()[0]

    # Weekly Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM lpc_breakdown
    WHERE YEARWEEK(
        breakdown_date,1
    )
    =
    YEARWEEK(
        CURDATE(),1
    )
    """)

    weekly_count = cursor.fetchone()[0]

    # Monthly Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM lpc_breakdown
    WHERE MONTH(breakdown_date)
    =
    MONTH(CURDATE())
    AND YEAR(breakdown_date)
    =
    YEAR(CURDATE())
    """)

    monthly_count = cursor.fetchone()[0]

    return render_template(
        "reports.html",

        report_data=report_data,

        daily_count=daily_count,

        weekly_count=weekly_count,

        monthly_count=monthly_count
    )
# ==========================
# EXPORT BREAKDOWN EXCEL
# ==========================

@app.route("/export_breakdown_excel")
def export_breakdown_excel():

    cursor.execute("""
    SELECT
    ticket_no,
    breakdown_date,
    machine_name,
    problem_type,
    status
    FROM lpc_breakdown
    ORDER BY breakdown_date DESC
    """)

    data = cursor.fetchall()

    df =pandas.DataFrame(
        data,
        columns=[
            "Ticket No",
            "Breakdown Date",
            "Machine Name",
            "Problem Type",
            "Status"
        ]
    )

    file_name = "Breakdown_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )

@app.route("/export_rca_excel")
def export_rca_excel():

    cursor.execute("""
    SELECT *
    FROM rca
    """)

    data = cursor.fetchall()

    df = pandas.DataFrame(data)

    file_name = "RCA_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )

@app.route("/export_inventory_excel")
def export_inventory_excel():

    cursor.execute("""
    SELECT
    part_no,
    part_name,
    machine_name,
    current_stock,
    minimum_stock,
    status
    FROM spare_master
    """)

    data = cursor.fetchall()

    df = pandas.DataFrame(
        data,
        columns=[
            "Part No",
            "Part Name",
            "Machine",
            "Current Stock",
            "Minimum Stock",
            "Status"
        ]
    )

    file_name = "Inventory_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )

# ==========================
# EXPORT MONTHLY REPORT
# ==========================

@app.route("/export_monthly_report")
def export_monthly_report():

    cursor.execute("""
    SELECT
    ticket_no,
    breakdown_date,
    machine_name,
    problem_type,
    status
    FROM lpc_breakdown
    WHERE MONTH(breakdown_date)=MONTH(CURDATE())
    AND YEAR(breakdown_date)=YEAR(CURDATE())
    """)

    data = cursor.fetchall()

    df = pandas.DataFrame(
        data,
        columns=[
            "Ticket No",
            "Date",
            "Machine",
            "Problem",
            "Status"
        ]
    )

    file_name = "Monthly_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )
    file_name = "Monthly_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )

# ==========================
# DAILY REPORT
# ==========================

@app.route("/daily_report")
def daily_report():

    cursor.execute("""
    SELECT
        ticket_no,
        breakdown_date,
        machine_name,
        problem_type,
        status
    FROM lpc_breakdown
    WHERE breakdown_date = CURDATE()
    ORDER BY ticket_no DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "daily_report.html",
        report_data=report_data
    )

# ==========================
# MACHINE WISE REPORT
# ==========================

@app.route("/machine_wise_report", methods=["GET","POST"])
def machine_wise_report():

    if request.method == "POST":

        machine_name = request.form.get("machine_name")

        cursor.execute("""
        SELECT
        machine_name,
        COUNT(*) AS total_breakdown
        FROM lpc_breakdown
        WHERE machine_name LIKE %s
        GROUP BY machine_name
        ORDER BY total_breakdown DESC
        """,
        ("%" + machine_name + "%",))

    else:

        cursor.execute("""
        SELECT
        machine_name,
        COUNT(*) AS total_breakdown
        FROM lpc_breakdown
        GROUP BY machine_name
        ORDER BY total_breakdown DESC
        """)

    report_data = cursor.fetchall()

    return render_template(
        "machine_wise_report.html",
        report_data=report_data
    )

# ==========================
# MACHINE DETAILS REPORT
# ==========================

@app.route("/machine_details/<machine_name>")
def machine_details(machine_name):

    cursor.execute("""
    SELECT
    ticket_no,
    breakdown_date,
    problem_type,
    status
    FROM lpc_breakdown
    WHERE machine_name=%s
    ORDER BY breakdown_date DESC
    """, (machine_name,))

    report_data = cursor.fetchall()

    return render_template(
        "machine_details.html",
        report_data=report_data,
        machine_name=machine_name
    )

# ==========================
# DOWNTIME REPORT
# ==========================

@app.route("/downtime_report")
def downtime_report():

    cursor.execute("""
    SELECT
    ticket_no,
    machine_name,
    down_time
    FROM maintenance_action
    ORDER BY down_time DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "downtime_report.html",
        report_data=report_data
    )


# ==========================
# TECHNICIAN PERFORMANCE REPORT
# ==========================

@app.route("/technician_report")
def technician_report():

    cursor.execute("""
    SELECT
    technician_name,
    COUNT(*) AS total_jobs
    FROM maintenance_action
    GROUP BY technician_name
    ORDER BY total_jobs DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "technician_report.html",
        report_data=report_data
    )

# ==========================
# RCA REPORT
# ==========================

@app.route("/rca_report")
def rca_report():

    cursor.execute("""
    SELECT
    ticket_no,
    root_cause,
    corrective_action,
    preventive_action
    FROM rca
    """)

    report_data = cursor.fetchall()

    return render_template(
        "rca_report.html",
        report_data=report_data
    )

# ==========================
# SPARE CONSUMPTION REPORT
# ==========================

@app.route("/spare_consumption_report")
def spare_consumption_report():

    cursor.execute("""
    SELECT
    ticket_no,
    part_used,
    qty_used,
    technician_name
    FROM maintenance_action
    ORDER BY qty_used DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "spare_consumption_report.html",
        report_data=report_data
    )

# ==========================
# MONTHLY REPORT
# ==========================

@app.route("/monthly_report", methods=["GET","POST"])
def monthly_report():

    if request.method == "POST":

        report_month = request.form["report_month"]

        year = report_month.split("-")[0]

        month = report_month.split("-")[1]

        cursor.execute("""
        SELECT
        ticket_no,
        breakdown_date,
        machine_name,
        problem_type,
        status
        FROM lpc_breakdown
        WHERE MONTH(breakdown_date)=%s
        AND YEAR(breakdown_date)=%s
        ORDER BY breakdown_date DESC
        """,
        (
            month,
            year
        ))

        report_data = cursor.fetchall()

    else:

        cursor.execute("""
        SELECT
        ticket_no,
        breakdown_date,
        machine_name,
        problem_type,
        status
        FROM lpc_breakdown
        ORDER BY breakdown_date DESC
        """)

        report_data = cursor.fetchall()

    return render_template(
        "monthly_report.html",
        report_data=report_data
    )

# ==========================
# PROBLEM WISE REPORT
# ==========================

@app.route("/problem_wise_report")
def problem_wise_report():

    cursor.execute("""
    SELECT
    problem_type,
    COUNT(*) AS total_breakdown
    FROM lpc_breakdown
    GROUP BY problem_type
    ORDER BY total_breakdown DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "problem_wise_report.html",
        report_data=report_data
    )

# ==========================
# PROBLEM DETAILS REPORT
# ==========================

@app.route("/problem_details/<problem_type>")
def problem_details(problem_type):

    cursor.execute("""
    SELECT
    ticket_no,
    machine_name,
    breakdown_date,
    status
    FROM lpc_breakdown
    WHERE problem_type=%s
    ORDER BY breakdown_date DESC
    """,(problem_type,))

    report_data = cursor.fetchall()

    return render_template(
        "problem_details.html",
        report_data=report_data,
        problem_type=problem_type
    )

# ==========================
# WEEKLY REPORT
# ==========================

@app.route("/weekly_report")
def weekly_report():

    cursor.execute("""
    SELECT
        ticket_no,
        breakdown_date,
        machine_name,
        problem_type,
        status
    FROM lpc_breakdown
    WHERE YEARWEEK(breakdown_date,1)
    =
    YEARWEEK(CURDATE(),1)
    ORDER BY breakdown_date DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "weekly_report.html",
        report_data=report_data
    )
    
# ==========================
# DATABASE TEST
# ==========================

@app.route("/test_db")
def test_db():

    cursor.execute(
        "SELECT * FROM machine_master"
    )

    data = cursor.fetchall()

    return str(data)

# ==========================
# OPERATOR MASTER
# ==========================

@app.route("/operator_master")
def operator_master():

    search_text = request.args.get("search_text", "")

    if search_text:

        cursor.execute("""
        SELECT
        employee_id,
        operator_name,
        department,
        line_name,
        username,
        shift_name,
        status
        FROM operator_master
        WHERE employee_id LIKE %s
        OR operator_name LIKE %s
        OR department LIKE %s
        OR line_name LIKE %s
        ORDER BY employee_id
        """,
        (
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%"
        ))

    else:

        cursor.execute("""
        SELECT
        employee_id,
        operator_name,
        department,
        line_name,
        username,
        shift_name,
        status
        FROM operator_master
        ORDER BY employee_id
        """)

    operator_data = cursor.fetchall()

    return render_template(
        "operator_master.html",
        operator_data=operator_data
    )
@app.route("/save_operator", methods=["POST"])
def save_operator():

    employee_id = request.form["employee_id"]
    operator_name = request.form["operator_name"]
    department = request.form["department"]
    line_name = request.form["line_name"]
    username = request.form["username"]
    password = request.form["password"]
    shift_name = request.form["shift_name"]
    status = request.form["status"]

    employee_id = employee_id.strip()
    operator_name = operator_name.strip()
    username = username.strip()

    if employee_id == "" or operator_name == "" or username == "":

        return """
        <h2 style='color:red'>
        Employee ID, Operator Name and Username Required
        </h2>

        <a href='/operator_master'>
        Back
        </a>
        """
        cursor.execute("""
    SELECT employee_id
    FROM operator_master
    WHERE employee_id=%s
    """, (employee_id,))

    check = cursor.fetchone()

    if check:

        return """
        <h2 style='color:red'>
        Employee ID Already Exists
        </h2>

        <a href='/operator_master'>
        Back
        </a>
        """

    cursor.execute("""
    INSERT INTO operator_master
    (
        employee_id,
        operator_name,
        department,
        line_name,
        username,
        password,
        shift_name,
        status
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        employee_id,
        operator_name,
        department,
        line_name,
        username,
        password,
        shift_name,
        status
    ))

    db.commit()

    return redirect("/operator_master")
# ==========================
# EDIT OPERATOR
# ==========================
@app.route("/edit_operator/<employee_id>")
def edit_operator(employee_id):

    cursor.execute("""
    SELECT
    employee_id,
    operator_name,
    department,
    line_name,
    username,
    password,
    shift_name,
    status
    FROM operator_master
    WHERE employee_id=%s
    """,(employee_id,))

    operator_data = cursor.fetchone()

    return render_template(
        "edit_operator.html",
        operator_data=operator_data
    )

@app.route("/delete_operator/<employee_id>")
def delete_operator(employee_id):

    cursor.execute("""
    DELETE FROM operator_master
    WHERE employee_id=%s
    """, (employee_id,))

    db.commit()

    return redirect("/operator_master")

# ==========================
# Update Route
# ==========================
@app.route("/update_operator", methods=["POST"])
def update_operator():

    employee_id = request.form["employee_id"]
    operator_name = request.form["operator_name"]
    department = request.form["department"]
    line_name = request.form["line_name"]
    username = request.form["username"]
    password = request.form["password"]
    shift_name = request.form["shift_name"]
    status = request.form["status"]

    cursor.execute("""
    UPDATE operator_master
    SET
    operator_name=%s,
    department=%s,
    line_name=%s,
    username=%s,
    password=%s,
    shift_name=%s,
    status=%s
    WHERE employee_id=%s
    """,
    (
        operator_name,
        department,
        line_name,
        username,
        password,
        shift_name,
        status,
        employee_id
    ))

    db.commit()

    return redirect("/operator_master")
# ==========================
# USER MASTER
# ==========================

@app.route("/user_master")
def user_master():

    search = request.args.get("search", "")

    if search:

        cursor.execute("""
            SELECT *
            FROM user_master
            WHERE employee_id LIKE %s
            OR employee_name LIKE %s
            OR username LIKE %s
            OR department LIKE %s
            OR role LIKE %s
            ORDER BY id DESC
        """,(

            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"

        ))

    else:

        cursor.execute("""
            SELECT *
            FROM user_master
            ORDER BY id DESC
        """)

    users = cursor.fetchall()

    return render_template(
        "user_master.html",
        users=users
    )

# ==========================
# SAVE USER MASTER
# ==========================

@app.route("/save_user", methods=["POST"])
def save_user():

    try:

        employee_id = request.form["employee_id"]
        employee_name = request.form["employee_name"]
        username = request.form["username"]
        password = request.form["password"]
        department = request.form["department"]
        role = request.form["role"]
        email = request.form["email"]
        status = request.form["status"]

        # MODULE ACCESS

        quality_access = request.form.get(
            "quality_access",
            "NO"
        )

        store_access = request.form.get(
            "store_access",
            "NO"
        )

        maintenance_access = request.form.get(
            "maintenance_access",
            "NO"
        )

        lpc_access = request.form.get(
            "lpc_access",
            "NO"
        )

        assy_access = request.form.get(
            "assy_access",
            "NO"
        )

        admin_access = request.form.get(
            "admin_access",
            "NO"
        )

        sql = """

        INSERT INTO user_master(

            employee_id,
            employee_name,
            username,
            password,
            department,
            role,
            email,
            status,

            quality_access,
            store_access,
            maintenance_access,
            lpc_access,
            assy_access,
            admin_access

        )

        VALUES(

            %s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s

        )

        """

        values = (

            employee_id,
            employee_name,
            username,
            password,
            department,
            role,
            email,
            status,

            quality_access,
            store_access,
            maintenance_access,
            lpc_access,
            assy_access,
            admin_access

        )

        cursor.execute(sql, values)

        db.commit()

        return """

        <h2>✅ User Saved Successfully</h2>

        <br>

        <a href="/user_master">
        Back To User Master
        </a>

        <br><br>

        <a href="/admin">
        Back To Dashboard
        </a>

        """

    except Exception as e:

        return f"ERROR : {str(e)}"

    # ==========================
# UPDATE PASSWORD
# ==========================

@app.route(
"/update_password/<int:id>",
methods=["POST"]
)
def update_password(id):

    password = request.form["new_password"]

    confirm_password = request.form[
        "confirm_password"
    ]

    if password != confirm_password:

        flash(
        "Password and Confirm Password Not Match"
        )

        return redirect(
        f"/change_password/{id}"
        )

    cursor.execute("""

        UPDATE user_master

        SET password=%s

        WHERE id=%s

    """,
    (
        password,
        id
    ))

    db.commit()

    flash(
    "Password Updated Successfully"
    )

    return redirect(
    "/user_master"
    )


    @app.route("/edit_user/<int:id>")
    def edit_user(id):

      cursor.execute(
        "SELECT * FROM user_master WHERE id=%s",
        (id,)
    )

    user = cursor.fetchone()

    return render_template(
        "edit_user.html",
        user=user
    )
@app.route("/delete_user/<int:id>")
def delete_user(id):

    cursor.execute(
        "DELETE FROM user_master WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/user_master")

@app.route("/change_password/<int:id>")
def change_password(id):

    cursor.execute(
        "SELECT * FROM user_master WHERE id=%s",
        (id,)
    )

    user = cursor.fetchone()

    return render_template(
        "change_password.html",
        user=user
    )

@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):

    cursor.execute("""
        UPDATE user_master
        SET
            employee_id=%s,
            employee_name=%s,
            username=%s,
            email=%s,
            department=%s,
            role=%s,
            status=%s
        WHERE id=%s
    """, (

        request.form["employee_id"],
        request.form["employee_name"],
        request.form["username"],
        request.form["email"],
        request.form["department"],
        request.form["role"],
        request.form["status"],
        id

    ))

    db.commit()

    return redirect("/user_master")

@app.route("/edit_user/<int:id>")
def edit_user(id):

    cursor.execute(
        "SELECT * FROM user_master WHERE id=%s",
        (id,)
    )

    user = cursor.fetchone()

    return render_template(
        "edit_user.html",
        user=user
    )
# ==========================
# SPARE PARTS MASTER
# ==========================
@app.route("/spare_parts_master")
def spare_parts_master():

    search = request.args.get("search", "")

    if search:

        cursor.execute("""
            SELECT *
            FROM spare_parts_master
            WHERE part_no LIKE %s
            OR part_name LIKE %s
            OR machine_name LIKE %s
            OR store_location LIKE %s
            ORDER BY id DESC
        """, (

            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"

        ))

    else:

        cursor.execute("""
            SELECT *
            FROM spare_parts_master
            ORDER BY id DESC
        """)

    spares = cursor.fetchall()

    return render_template(
        "spare_parts_master.html",
        spares=spares
    )
@app.route("/save_spare", methods=["POST"])
def save_spare():

    cursor.execute("""
        INSERT INTO spare_parts_master
        (
            part_no,
            part_name,
            category,
            machine_name,
            store_location,
            rack_no,
            bin_no,
            unit,
            current_stock,
            minimum_stock,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (

        request.form["part_no"],
        request.form["part_name"],
        request.form["category"],
        request.form["machine_name"],
        request.form["store_location"],
        request.form["rack_no"],
        request.form["bin_no"],
        request.form["unit"],
        request.form["current_stock"],
        request.form["minimum_stock"],
        request.form["status"]

    ))

    db.commit()

    return redirect("/spare_parts_master")
@app.route("/edit_spare/<int:id>")
def edit_spare(id):

    cursor.execute(
        "SELECT * FROM spare_parts_master WHERE id=%s",
        (id,)
    )

    spare = cursor.fetchone()

    return render_template(
        "edit_spare.html",
        spare=spare
    )
@app.route("/update_spare/<int:id>", methods=["POST"])
def update_spare(id):

    cursor.execute("""
        UPDATE spare_parts_master
        SET
            part_no=%s,
            part_name=%s,
            category=%s,
            machine_name=%s,
            store_location=%s,
            rack_no=%s,
            bin_no=%s,
            unit=%s,
            current_stock=%s,
            minimum_stock=%s,
            status=%s
        WHERE id=%s
    """, (

        request.form["part_no"],
        request.form["part_name"],
        request.form["category"],
        request.form["machine_name"],
        request.form["store_location"],
        request.form["rack_no"],
        request.form["bin_no"],
        request.form["unit"],
        request.form["current_stock"],
        request.form["minimum_stock"],
        request.form["status"],
        id

    ))

    db.commit()

    return redirect("/spare_parts_master")
@app.route("/delete_spare/<int:id>")
def delete_spare(id):

    cursor.execute(
        "DELETE FROM spare_parts_master WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/spare_parts_master")
@app.route("/download_spare_template")
def download_spare_template():

    df = pd.DataFrame(columns=[

        "Part No",
        "Part Name",
        "Category",
        "Machine Name",
        "Store Location",
        "Rack No",
        "Bin No",
        "Unit",
        "Current Stock",
        "Minimum Stock",
        "Status"

    ])

    file_name = "Spare_Parts_Template.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
@app.route("/upload_spare_excel", methods=["POST"])
def upload_spare_excel():

    file = request.files["excel_file"]

    if file.filename == "":
        return redirect("/spare_parts_master")

    df = pd.read_excel(file)

    for _, row in df.iterrows():

        cursor.execute("""
        INSERT INTO spare_parts_master
        (
            part_no,
            part_name,
            category,
            machine_name,
            store_location,
            rack_no,
            bin_no,
            unit,
            current_stock,
            minimum_stock,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (

            row["Part No"],
            row["Part Name"],
            row["Category"],
            row["Machine Name"],
            row["Store Location"],
            row["Rack No"],
            row["Bin No"],
            row["Unit"],
            row["Current Stock"],
            row["Minimum Stock"],
            row["Status"]

        ))

    db.commit()

    return redirect("/spare_parts_master")
@app.route("/export_spare_excel")
def export_spare_excel():

    cursor.execute("""
        SELECT
        part_no,
        part_name,
        category,
        machine_name,
        store_location,
        rack_no,
        bin_no,
        unit,
        current_stock,
        minimum_stock,
        status
        FROM spare_parts_master
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[

        "Part No",
        "Part Name",
        "Category",
        "Machine Name",
        "Store Location",
        "Rack No",
        "Bin No",
        "Unit",
        "Current Stock",
        "Minimum Stock",
        "Status"

    ])

    file_name = "Spare_Parts_Master.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
# ==========================
# SPARE ISSUE
# ==========================

@app.route("/spare_issue")
def spare_issue():

    search = request.args.get("search", "")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    cursor.execute("""
        SELECT *
        FROM spare_parts_master
        WHERE status='ACTIVE'
        ORDER BY part_no
    """)
    spare_parts = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT machine_name
        FROM spare_parts_master
        WHERE machine_name IS NOT NULL
        ORDER BY machine_name
    """)
    machines = cursor.fetchall()

    sql = """
    SELECT *
    FROM spare_issue
    WHERE 1=1
    """

    params = []

    if search:

        sql += """
        AND (
            part_no LIKE %s
            OR part_name LIKE %s
        )
        """

        params.extend([
            "%" + search + "%",
            "%" + search + "%"
        ])

    if from_date:
        sql += " AND issue_date >= %s"
        params.append(from_date)

    if to_date:
        sql += " AND issue_date <= %s"
        params.append(to_date)

    sql += " ORDER BY issue_id DESC"

    cursor.execute(sql, params)

    issue_history = cursor.fetchall()

    return render_template(
        "spare_issue.html",
        spare_parts=spare_parts,
        machines=machines,
        issue_history=issue_history
    )
# ==========================
# Export ISSUE
# ==========================
@app.route("/export_issue_excel")
def export_issue_excel():

    cursor.execute("""
    SELECT
        issue_date,
        issue_no,
        ticket_no,
        machine_name,
        part_no,
        part_name,
        issue_qty,
        issued_to,
        department,
        location,
        rack_location,
        reason,
        remarks
    FROM spare_issue
    ORDER BY issue_id DESC
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[

        "Issue Date",
        "Issue No",
        "Ticket No",
        "Machine Name",
        "Part No",
        "Part Name",
        "Issue Qty",
        "Issued To",
        "Department",
        "Location",
        "Rack Location",
        "Reason",
        "Remarks"

    ])

    file_name = "Spare_Issue_Report.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
# ==========================
# Save ISSUE
# ==========================
@app.route("/save_issue", methods=["POST"])
def save_issue():

    try:

        issue_no = request.form["issue_no"]
        issue_date = request.form["issue_date"]
        ticket_no = request.form["ticket_no"]
        machine_name = request.form["machine_name"]

        part_no = request.form["part_no"]
        part_name = request.form["part_name"]

        issue_qty_text = request.form.get("issue_qty", "").strip()

        if not issue_qty_text:
            return "Please Enter Issue Quantity"

        issue_qty = int(issue_qty_text)

        issued_to = request.form["issued_to"]
        department = request.form["department"]

        location = request.form["location"]
        rack_location = request.form["rack_location"]

        reason = request.form["reason"]
        remarks = request.form["remarks"]

        # Check Current Stock
        cursor.execute("""
            SELECT current_stock
            FROM spare_parts_master
            WHERE part_no=%s
        """, (part_no,))

        stock = cursor.fetchone()

        if stock is None:
            return "Part Not Found"

        current_stock = int(stock[0])

        if issue_qty > current_stock:
            return f"""
            <h2>Insufficient Stock</h2>
            <p>Available Stock : {current_stock}</p>
            <a href="/spare_issue">Back</a>
            """

        # Save Issue
        cursor.execute("""
        INSERT INTO spare_issue
        (
            issue_no,
            issue_date,
            ticket_no,
            machine_name,
            part_no,
            part_name,
            issue_qty,
            issued_to,
            department,
            location,
            rack_location,
            reason,
            remarks
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            issue_no,
            issue_date,
            ticket_no,
            machine_name,
            part_no,
            part_name,
            issue_qty,
            issued_to,
            department,
            location,
            rack_location,
            reason,
            remarks
        ))

        # Auto Reduce Stock
        cursor.execute("""
        UPDATE spare_parts_master
        SET current_stock = current_stock - %s
        WHERE part_no=%s
        """,
        (issue_qty, part_no))

        db.commit()

        return redirect("/spare_issue")

    except Exception as e:
        return f"ERROR : {e}"

    @app.route("/spare_issue")
    def spare_issue():

     cursor.execute("""
        SELECT *
        FROM spare_parts_master
        WHERE status='ACTIVE'
        ORDER BY part_no
    """)
    spare_parts = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT machine_name
        FROM spare_parts_master
        ORDER BY machine_name
    """)
    machines = cursor.fetchall()

    cursor.execute("""
        SELECT *
        FROM spare_issue
        ORDER BY issue_id DESC
    """)
    issue_history = cursor.fetchall()

    return render_template(
        "spare_issue.html",
        spare_parts=spare_parts,
        machines=machines,
        issue_history=issue_history
    )
    return {}
@app.route("/get_part/<part_no>")
def get_part(part_no):

    cursor.execute("""
        SELECT
            part_name,
            machine_name,
            current_stock,
            store_location,
            rack_no,
            bin_no
        FROM spare_parts_master
        WHERE part_no=%s
    """, (part_no,))

    data = cursor.fetchone()

    if data:

        return {
            "part_name": data[0],
            "machine_name": data[1],
            "current_stock": data[2],
            "store_location": data[3],
            "rack_no": data[4],
            "bin_no": data[5]
        }

    return {}
# ==========================
# SPARE RECEIVE
# ==========================

@app.route("/spare_receive")
def spare_receive():

    search = request.args.get("search","")
    from_date = request.args.get("from_date","")
    to_date = request.args.get("to_date","")

    cursor.execute("""
    SELECT *
    FROM spare_parts_master
    ORDER BY part_no
    """)
    spare_parts = cursor.fetchall()

    sql = """
    SELECT *
    FROM spare_receive
    WHERE 1=1
    """

    params = []

    if search:

        sql += """
        AND (
            part_no LIKE %s
            OR part_name LIKE %s
        )
        """

        params.extend([
            "%" + search + "%",
            "%" + search + "%"
        ])

    if from_date:
        sql += " AND receive_date >= %s"
        params.append(from_date)

    if to_date:
        sql += " AND receive_date <= %s"
        params.append(to_date)

    sql += " ORDER BY receive_id DESC"

    cursor.execute(sql, params)

    receive_history = cursor.fetchall()

    return render_template(
        "spare_receive.html",
        spare_parts=spare_parts,
        receive_history=receive_history
    )
@app.route("/save_receive", methods=["POST"])
def save_receive():

    try:

        receive_no = request.form["receive_no"]
        receive_date = request.form["receive_date"]

        part_no = request.form["part_no"]
        part_name = request.form["part_name"]

        machine_name = request.form.get("machine_name", "")
        current_stock = int(request.form.get("current_stock", 0))

        receive_qty = int(request.form["receive_qty"])

        supplier_name = request.form["supplier_name"]
        invoice_no = request.form["invoice_no"]

        location = request.form.get("location", "")
        rack_location = request.form.get("rack_location", "")

        received_by = request.form["received_by"]
        remarks = request.form["remarks"]

        cursor.execute("""
        INSERT INTO spare_receive
        (
            receive_no,
            receive_date,
            part_no,
            part_name,
            machine_name,
            current_stock,
            receive_qty,
            supplier_name,
            invoice_no,
            location,
            rack_location,
            received_by,
            remarks
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            receive_no,
            receive_date,
            part_no,
            part_name,
            machine_name,
            current_stock,
            receive_qty,
            supplier_name,
            invoice_no,
            location,
            rack_location,
            received_by,
            remarks
        ))

        cursor.execute("""
        UPDATE spare_parts_master
        SET current_stock = current_stock + %s
        WHERE part_no=%s
        """,
        (
            receive_qty,
            part_no
        ))

        db.commit()

        return redirect("/spare_receive")

    except Exception as e:

        return f"ERROR : {e}"
@app.route("/export_receive_excel")
def export_receive_excel():

    cursor.execute("""
    SELECT
        receive_date,
        receive_no,
        part_no,
        part_name,
        receive_qty,
        supplier_name,
        invoice_no,
        received_by,
        remarks
    FROM spare_receive
    ORDER BY receive_id DESC
    """)

    data = cursor.fetchall()

    import pandas as pd

    df = pd.DataFrame(
        data,
        columns=[
            "Receive Date",
            "Receive No",
            "Part No",
            "Part Name",
            "Receive Qty",
            "Supplier Name",
            "Invoice No",
            "Received By",
            "Remarks"
        ]
    )

    file_name = "Spare_Receive_Report.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )
# ==========================
# ASSY MAINTENANCE ACTION
# ==========================

@app.route("/assy_maintenance_action")
def assy_maintenance_action():

    cursor.execute("""
    SELECT
    ticket_no,
    machine_name,
    problem_type,
    breakdown_date,
    breakdown_time
    FROM assy_breakdown
    WHERE status='OPEN'
    """)

    open_breakdowns = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM assy_action
    ORDER BY action_id DESC
    """)

    action_history = cursor.fetchall()

    return render_template(
    "assy_maintenance_action.html",
    open_breakdowns=open_breakdowns,
    action_history=action_history
)

# ==========================
# SAVE ASSY MAINTENANCE ACTION
# ==========================

@app.route("/save_assy_action", methods=["POST"])
def save_assy_action():

    try:

        ticket_no = request.form.get("ticket_no")
        machine_name = request.form.get("machine_name")
        problem_type = request.form.get("problem_type")

        root_cause = request.form.get("reason")
        action_taken = request.form.get("action_taken")

        technician_name = request.form.get("technician_name")

        part_used = request.form.get("part_used")

        qty_used = request.form.get("qty_used",0)

        down_time = request.form.get("down_time",0)


        if down_time == "":
         down_time = 0
        else:
            down_time = int(down_time)

        remarks = request.form.get("remarks")

        status = request.form.get("status")
        from datetime import date

        action_date = date.today()
        
        print("================================")
        print("Ticket No =", ticket_no)
        print("Down Time =", down_time)
        print("================================")


        cursor.execute("""
        INSERT INTO assy_action
        (
            ticket_no,
            action_date,
            machine_name,
            problem_type,
            root_cause,
            action_taken,
            technician_name,
            part_used,
            qty_used,
            down_time,
            remarks,
            status
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            ticket_no,
            action_date,
            machine_name,
            problem_type,
            root_cause,
            action_taken,
            technician_name,
            part_used,
            qty_used,
            down_time,
            remarks,
            status
        ))
        

        db.commit()

        # CLOSE ASSY BREAKDOWN
        cursor.execute("""
        UPDATE assy_breakdown
        SET status='CLOSED'
        WHERE ticket_no=%s
        """, (ticket_no,))

        db.commit()
        return """
        <h2>✅ ASSY Maintenance Action Saved Successfully</h2>

        <br>

        <a href='/assy_maintenance_action'>
        Back To ASSY Maintenance Action
        </a>

        <br><br>

        <a href='/maintenance'>
        Back To Dashboard
        </a>
        """

    except Exception as e:

        return f"ERROR : {e}"

# ==========================
# ASSY MAINTENANCE HISTORY
# ==========================

@app.route("/assy_maintenance_history")
def assy_maintenance_history():

    cursor.execute("""
    SELECT
    ticket_no,
    machine_name,
    problem_type,
    technician_name,
    down_time,
    status
    FROM assy_action
    ORDER BY action_id DESC
    """)

    history_data = cursor.fetchall()

    return render_template(
        "assy_maintenance_history.html",
        history_data=history_data
    )
# ==========================
# ASSY MAINTENANCE REPORT
# ==========================

@app.route("/assy_maintenance_report")
def assy_maintenance_report():

    # Daily Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_action
    WHERE DATE(action_date)=CURDATE()
    """)

    daily_count = cursor.fetchone()[0]

    # Weekly Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_action
    WHERE YEARWEEK(action_date,1)=YEARWEEK(CURDATE(),1)
    """)

    weekly_count = cursor.fetchone()[0]

    # Monthly Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_action
    WHERE MONTH(action_date)=MONTH(CURDATE())
    AND YEAR(action_date)=YEAR(CURDATE())
    """)

    monthly_count = cursor.fetchone()[0]

    # ASSY Maintenance Report Data

    cursor.execute("""

    SELECT

        a.ticket_no,

        b.breakdown_date,

        a.machine_name,

        a.problem_type,

        a.technician_name,

        a.down_time,

        a.status

    FROM assy_action a

    LEFT JOIN assy_breakdown b

    ON a.ticket_no = b.ticket_no

    ORDER BY a.action_id DESC

    """)

    report_data = cursor.fetchall()

    # Total Spare Issue Transactions

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_spare_issue
    """)

    total_issue = cursor.fetchone()[0]

    # Total Spare Receive Transactions

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_spare_receive
    """)

    total_receive = cursor.fetchone()[0]

    # Total Issued Quantity

    cursor.execute("""
    SELECT IFNULL(SUM(issue_qty),0)
    FROM assy_spare_issue
    """)

    total_issue_qty = cursor.fetchone()[0]

    # Total Received Quantity

    cursor.execute("""
    SELECT IFNULL(SUM(receive_qty),0)
    FROM assy_spare_receive
    """)

    total_receive_qty = cursor.fetchone()[0]

    return render_template(

        "assy_maintenance_report.html",

        daily_count=daily_count,

        weekly_count=weekly_count,

        monthly_count=monthly_count,

        total_issue=total_issue,

        total_receive=total_receive,

        total_issue_qty=total_issue_qty,

        total_receive_qty=total_receive_qty,

        report_data=report_data

    )
# =================================
# ASSY SPARE CONSUMPTION REPORT
# =================================

@app.route("/assy_spare_consumption_report")
def assy_spare_consumption_report():

    cursor.execute("""
    SELECT
    part_no,
    part_name,
    COUNT(*) AS total_issue,
    SUM(issue_qty) AS total_qty
    FROM assy_spare_issue
    GROUP BY part_no, part_name
    ORDER BY total_qty DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "assy_spare_consumption_report.html",
        report_data=report_data
    )
# =================================
# ASSY LOW STOCK REPORT
# =================================

@app.route("/assy_low_stock_report")
def assy_low_stock_report():

    cursor.execute("""
    SELECT
    part_no,
    part_name,
    category,
    machine,
    stock_qty,
    minimum_stock,
    status
    FROM assy_spare_parts_master
    WHERE stock_qty <= minimum_stock
    ORDER BY stock_qty ASC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "assy_low_stock_report.html",
        report_data=report_data
    )
# ==========================
# EXPORT ASSY REPORT EXCEL
# ==========================

@app.route("/export_assy_report")
def export_assy_report():

    cursor.execute("""
    SELECT
    ticket_no,
    action_date,
    machine_name,
    problem_type,
    technician_name,
    down_time,
    status
    FROM assy_action
    ORDER BY action_id DESC
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "Ticket No",
            "Action Date",
            "Machine Name",
            "Problem Type",
            "Technician",
            "Downtime (Min)",
            "Status"
        ]
    )

    file_name = "ASSY_Maintenance_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )
@app.route("/assy_monthly_report_excel")
def assy_monthly_report_excel():

    return send_file(
        "Assy_Monthly_Report.xlsx",
        as_attachment=True
    )
# ==========================
# ASSY MACHINE WISE REPORT
# ==========================

@app.route("/assy_machine_report")
def assy_machine_report():

    cursor.execute("""
    SELECT
    machine_name,
    COUNT(*) AS breakdown_count,
    SUM(down_time) AS total_downtime
    FROM assy_action
    GROUP BY machine_name
    ORDER BY breakdown_count DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "assy_machine_Wise_report.html",
        report_data=report_data
    )
# ==========================
# DAILY REPORT
# ==========================

@app.route("/assy_daily_report")
def assy_daily_report():

    cursor.execute("""
    SELECT
    ticket_no,
    action_date,
    machine_name,
    problem_type,
    technician_name,
    down_time,
    status
    FROM assy_action
    WHERE action_date = CURDATE()
    ORDER BY action_id DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "assy_daily_report.html",
        report_data=report_data
    )
# ==========================
# WEEKLY REPORT
# ==========================

@app.route("/assy_weekly_report")
def assy_weekly_report():

    cursor.execute("""
    SELECT
    ticket_no,
    action_date,
    machine_name,
    problem_type,
    technician_name,
    down_time,
    status
    FROM assy_action
    WHERE YEARWEEK(action_date,1)=YEARWEEK(CURDATE(),1)
    ORDER BY action_id DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "assy_weekly_report.html",
        report_data=report_data
    )
# ==========================
# MONTHLY REPORT
# ==========================

@app.route("/assy_monthly_report")
def assy_monthly_report():

    cursor.execute("""
    SELECT
    ticket_no,
    action_date,
    machine_name,
    problem_type,
    technician_name,
    down_time,
    status
    FROM assy_action
    WHERE MONTH(action_date)=MONTH(CURDATE())
    AND YEAR(action_date)=YEAR(CURDATE())
    ORDER BY action_id DESC
    """)

    report_data = cursor.fetchall()

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_action
    WHERE MONTH(action_date)=MONTH(CURDATE())
    AND YEAR(action_date)=YEAR(CURDATE())
    """)

    total_breakdown = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(down_time)
    FROM assy_action
    WHERE MONTH(action_date)=MONTH(CURDATE())
    AND YEAR(action_date)=YEAR(CURDATE())
    """)

    total_downtime = cursor.fetchone()[0]

    return render_template(
        "assy_monthly_report.html",
        report_data=report_data,
        total_breakdown=total_breakdown,
        total_downtime=total_downtime
    )
# ==========================
# TOP BREAKDOWN MACHINES
# ==========================

@app.route("/top_breakdown_machines")
def top_breakdown_machines():

    cursor.execute("""
    SELECT
    machine_name,
    COUNT(*) AS total_breakdown,
    SUM(down_time) AS total_downtime
    FROM assy_action
    GROUP BY machine_name
    ORDER BY total_breakdown DESC
    LIMIT 10
    """)

    report_data = cursor.fetchall()

    return render_template(
        "top_breakdown_machines.html",
        report_data=report_data
    )
# ==========================
# Assy PROBLEM WISE REPORT
# ==========================

@app.route("/Assy_problem_wise_report")
def Assy_problem_wise_report():

    cursor.execute("""
    SELECT
    problem_type,
    COUNT(*) AS total_breakdown,
    SUM(down_time) AS total_downtime
    FROM assy_action
    GROUP BY problem_type
    ORDER BY total_breakdown DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "Assy_problem_wise_report.html",
        report_data=report_data
    )
# ==========================
# Assy DOWN TIME REPORT
# ==========================

@app.route("/Assy_downtime_report")
def Assy_downtime_report():

    cursor.execute("""
    SELECT
    machine_name,
    COUNT(*) AS total_breakdown,
    SUM(down_time) AS total_downtime
    FROM assy_action
    GROUP BY machine_name
    ORDER BY total_downtime DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "Assy_downtime_report.html",
        report_data=report_data
    )
# ==========================
# Assy SPARE CONSUMPTION REPORT
# ==========================

@app.route("/Assy_spare_consumption_report")
def Assy_spare_consumption_report():

    cursor.execute("""
    SELECT
    part_used,
    COUNT(*) AS total_used,
    SUM(qty_used) AS total_qty
    FROM assy_action
    GROUP BY part_used
    ORDER BY total_qty DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "Assy_spare_consumption_report.html",
        report_data=report_data
    )
# ==========================
# Assy RCA REPORT
# ==========================

@app.route("/Assy_rca_report")
def Assy_rca_report():

    cursor.execute("""
    SELECT
    ticket_no,
    machine_name,
    problem_type,
    root_cause,
    action_taken,
    technician_name,
    action_date
    FROM assy_action
    ORDER BY action_id DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "Assy_rca_report.html",
        report_data=report_data
    )
# ==========================
# TECHNICIAN PERFORMANCE REPORT
# ==========================

@app.route("/Assy_technician_performance_report")
def Assy_technician_performance_report():

    cursor.execute("""
    SELECT
    technician_name,
    COUNT(*) AS total_breakdown,
    SUM(down_time) AS total_downtime
    FROM assy_action
    GROUP BY technician_name
    ORDER BY total_breakdown DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "Assy_technician_performance_report.html",
        report_data=report_data
    )
# ==========================
# EXPORT ASSY BREAKDOWN EXCEL
# ==========================

@app.route("/export_assy_breakdown")
def export_assy_breakdown():

    cursor.execute("""
    SELECT
    ticket_no,
    breakdown_date,
    machine_name,
    problem_type,
    status
    FROM assy_breakdown
    ORDER BY ticket_no DESC
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "Ticket No",
            "Breakdown Date",
            "Machine Name",
            "Problem Type",
            "Status"
        ]
    )

    file_name = "ASSY_Breakdown_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )
# ==========================
# EXPORT RCA REPORT EXCEL
# ==========================

@app.route("/export_rca_report")
def export_rca_report():

    cursor.execute("""
    SELECT
    ticket_no,
    action_date,
    machine_name,
    problem_type,
    root_cause,
    action_taken,
    technician_name
    FROM assy_action
    ORDER BY action_id DESC
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "Ticket No",
            "Action Date",
            "Machine Name",
            "Problem Type",
            "Root Cause",
            "Action Taken",
            "Technician Name"
        ]
    )

    file_name = "ASSY_RCA_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )
# ==========================
# ASSY INVENTORY EXCEL EXPORT
# ==========================

@app.route("/Assy_export_inventory_excel")
def Assy_export_inventory_excel():

    cursor.execute("""
    SELECT *
    FROM assy_spare_parts_master
    ORDER BY part_no
    """)

    data = cursor.fetchall()

    columns = [i[0] for i in cursor.description]

    df = pd.DataFrame(
        data,
        columns=columns
    )

    file_name = "Assy_Inventory_Report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )
# ==========================
# LOW STOCK REPORT
# ==========================

@app.route("/low_stock_report")
def low_stock_report():

    cursor.execute("""
    SELECT
    part_no,
    part_name,
    stock_qty,
    minimum_stock
    FROM spare_parts_master
    WHERE stock_qty <= minimum_stock
    ORDER BY stock_qty ASC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "low_stock_report.html",
        report_data=report_data
    )
# ==================================
# ASSY SPARE PARTS MASTER
# ==================================

@app.route("/assy_spare_parts_master")
def assy_spare_parts_master():

    cursor.execute("""
    SELECT *
    FROM assy_spare_parts_master
    ORDER BY id DESC
    """)

    spare_data = cursor.fetchall()

    return render_template(
        "assy_spare_parts_master.html",
        spare_data=spare_data
    )
# ==================================
# SAVE ASSY SPARE PART
# ==================================

@app.route("/save_assy_spare_part", methods=["POST"])
def save_assy_spare_part():

    try:

        cursor.execute("""
INSERT INTO assy_spare_parts_master
(
    part_no,
    part_name,
    category,
    machine,
    store_location,
    rack_no,
    bin_no,
    unit,
    stock_qty,
    minimum_stock,
    status
)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""",
(
    request.form.get("part_no", ""),
    request.form.get("part_name", ""),
    request.form.get("category", ""),
    request.form.get("machine", ""),
    request.form.get("store_location", ""),
    request.form.get("rack_no", ""),
    request.form.get("bin_no", ""),
    request.form.get("unit", ""),
    request.form.get("stock_qty") or 0,
    request.form.get("minimum_stock") or 0,
    request.form.get("status", "")
))

        db.commit()

        return redirect(
            "/assy_spare_parts_master"
        )

    except Exception as e:

        return f"ERROR : {e}"
    
from flask import send_file
import pandas as pd

# ==========================
# DOWNLOAD ASSY SPARE TEMPLATE
# ==========================

@app.route("/download_assy_spare_template")
def download_assy_spare_template():

    df = pd.DataFrame(columns=[

        "Part No",
        "Part Name",
        "Category",
        "Machine",
        "Store Location",
        "Rack No",
        "Bin No",
        "Unit",
        "Current Stock",
        "Minimum Stock",
        "Status"

    ])

    file_name = "ASSY_Spare_Template.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )
import pandas as pd
from flask import request, redirect

# ==========================
# UPLOAD ASSY SPARE EXCEL
# ==========================

@app.route("/upload_assy_spare_excel", methods=["POST"])
def upload_assy_spare_excel():

    try:

        file = request.files["excel_file"]

        df = pd.read_excel(file)

        df = df.fillna("")

        for index, row in df.iterrows():

            cursor.execute("""
INSERT INTO assy_spare_parts_master
(
    part_no,
    part_name,
    category,
    machine,
    store_location,
    rack_no,
    bin_no,
    unit,
    stock_qty,
    minimum_stock,
    status
)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""",
(
    row["Part No"],
    row["Part Name"],
    row["Category"],
    row["Machine"],
    row["Store Location"],
    row["Rack No"],
    row["Bin No"],
    row["Unit"],
    int(row["Current Stock"]) if row["Current Stock"] != "" else 0,
    int(row["Minimum Stock"]) if row["Minimum Stock"] != "" else 0,
    row["Status"]
))
        db.commit()

        return redirect("/assy_spare_parts_master")

    except Exception as e:

        return f"ERROR : {e}"
    
    
# ==================================
# EDIT ASSY SPARE PART
# ==================================

@app.route("/edit_assy_spare_part/<int:id>")
def edit_assy_spare_part(id):

    cursor.execute("""
    SELECT *
    FROM assy_spare_parts_master
    WHERE id=%s
    """,(id,))

    spare = cursor.fetchone()

    return render_template(
        "edit_assy_spare_part.html",
        spare=spare
    )
# ==================================
# DELETE ASSY SPARE PART
# ==================================

@app.route("/delete_assy_spare_part/<int:id>")
def delete_assy_spare_part(id):

    cursor.execute("""
    DELETE FROM assy_spare_parts_master
    WHERE id=%s
    """,(id,))

    db.commit()

    return redirect(
        "/assy_spare_parts_master"
    )
# ==========================
# ASSY SPARE ISSUE
# ==========================

@app.route("/assy_spare_issue")
def assy_spare_issue():

    cursor.execute("""
    SELECT
    part_no,
    part_name,
    stock_qty
    FROM assy_spare_parts_master
    ORDER BY part_name
    """)

    spare_parts = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM assy_spare_issue
    ORDER BY id DESC
    """)

    issue_history = cursor.fetchall()

    return render_template(
        "assy_spare_issue.html",
        spare_parts=spare_parts,
        issue_history=issue_history
    )
# =================================
# SAVE ASSY SPARE ISSUE
# =================================

@app.route("/save_assy_spare_issue", methods=["POST"])
def save_assy_spare_issue():

    try:

        issue_no = request.form["issue_no"]
        issue_date = request.form["issue_date"]

        machine_name = request.form["machine_name"]

        part_no = request.form["part_no"]
        part_name = request.form["part_name"]

        current_stock = int(
            request.form["current_stock"]
        )

        issue_qty = int(request.form["issue_qty"])

        if issue_qty > current_stock:
            return "ERROR : Not Enough Stock Available"

        balance_stock = current_stock - issue_qty

        issued_by = request.form["issued_by"]

        remarks = request.form["remarks"]

        cursor.execute("""
        INSERT INTO assy_spare_issue
        (
            issue_no,
            issue_date,
            machine_name,
            part_no,
            part_name,
            current_stock,
            issue_qty,
            balance_stock,
            issued_by,
            remarks
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            issue_no,
            issue_date,
            machine_name,
            part_no,
            part_name,
            current_stock,
            issue_qty,
            balance_stock,
            issued_by,
            remarks
        ))

        cursor.execute("""
        UPDATE assy_spare_parts_master
        SET stock_qty=%s
        WHERE part_no=%s
        """,
        (
            balance_stock,
            part_no
        ))

        db.commit()

        return redirect(
            "/assy_spare_issue"
        )

    except Exception as e:

        return f"ERROR : {e}"

    # =================================
# ASSY SPARE RECEIVE PAGE
# =================================

@app.route("/assy_spare_receive")
def assy_spare_receive():

    cursor.execute("""
    SELECT
    part_no,
    part_name,
    stock_qty
    FROM assy_spare_parts_master
    ORDER BY part_name
    """)

    spare_parts = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM assy_spare_receive
    ORDER BY id DESC
    """)

    receive_history = cursor.fetchall()

    return render_template(
        "assy_spare_receive.html",
        spare_parts=spare_parts,
        receive_history=receive_history
    )
# =================================
# SAVE ASSY SPARE RECEIVE
# =================================

@app.route("/save_assy_spare_receive", methods=["POST"])
def save_assy_spare_receive():

    try:

        receive_no = request.form["receive_no"]
        receive_date = request.form["receive_date"]

        supplier_name = request.form["supplier_name"]
        invoice_no = request.form["invoice_no"]

        part_no = request.form["part_no"]
        part_name = request.form["part_name"]

        current_stock = int(
            request.form["current_stock"]
        )

        receive_qty = int(
            request.form["receive_qty"]
        )

        new_stock = (
            current_stock + receive_qty
        )

        received_by = request.form["received_by"]

        remarks = request.form["remarks"]

        cursor.execute("""
        INSERT INTO assy_spare_receive
        (
            receive_no,
            receive_date,
            supplier_name,
            invoice_no,
            part_no,
            part_name,
            current_stock,
            receive_qty,
            new_stock,
            received_by,
            remarks
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            receive_no,
            receive_date,
            supplier_name,
            invoice_no,
            part_no,
            part_name,
            current_stock,
            receive_qty,
            new_stock,
            received_by,
            remarks
        ))

        cursor.execute("""
        UPDATE assy_spare_parts_master
        SET stock_qty=%s
        WHERE part_no=%s
        """,
        (
            new_stock,
            part_no
        ))

        db.commit()

        return redirect(
            "/assy_spare_receive"
        )

    except Exception as e:

        return f"ERROR : {e}"
    # =================================
# ASSY DASHBOARD
# =================================

@app.route("/assy_dashboard")
def assy_dashboard():

    # Total ASSY Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_breakdown
    """)
    total_breakdown = cursor.fetchone()[0]

    # Open Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_breakdown
    WHERE status='OPEN'
    """)
    open_breakdown = cursor.fetchone()[0]

    # Closed Breakdown

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_breakdown
    WHERE status='CLOSED'
    """)
    closed_breakdown = cursor.fetchone()[0]

    # Low Stock

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_spare_parts_master
    WHERE stock_qty <= minimum_stock
    """)
    low_stock = cursor.fetchone()[0]

    # Spare Issue

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_spare_issue
    """)
    total_issue = cursor.fetchone()[0]

    # Spare Receive

    cursor.execute("""
    SELECT COUNT(*)
    FROM assy_spare_receive
    """)
    total_receive = cursor.fetchone()[0]

    return render_template(
    "assy_dashboard.html",

    total_breakdown=total_breakdown,
    open_breakdown=open_breakdown,
    closed_breakdown=closed_breakdown,

    low_stock=low_stock,
    total_issue=total_issue,
    total_receive=total_receive
)
# Total Downtime

cursor.execute("""
SELECT IFNULL(SUM(down_time),0)
FROM assy_action
""")

total_downtime = cursor.fetchone()[0]
# =================================
# ASSY PROBLEM WISE REPORT
# =================================

@app.route("/assy_problem_wise_report")
def assy_problem_wise_report():

    cursor.execute("""
    SELECT
    problem_type,
    COUNT(*) AS total_breakdown,
    SUM(down_time) AS total_downtime
    FROM assy_action
    GROUP BY problem_type
    ORDER BY total_breakdown DESC
    """)

    report_data = cursor.fetchall()

    return render_template(
        "problem_wise_report.html",
        report_data=report_data
    )
# =================================
# STOCK CARD REPORT
# =================================

@app.route("/assy_stock_card_report")
def stock_card_report():

    cursor.execute("""
    SELECT
    part_no,
    part_name
    FROM assy_spare_parts_master
    ORDER BY part_name
    """)

    spare_parts = cursor.fetchall()

    return render_template(
        "assy_stock_card_report.html",
        spare_parts=spare_parts
    )

# =================================
# VIEW STOCK CARD
# =================================

@app.route("/view_stock_card", methods=["POST"])
def view_stock_card():

    part_no = request.form["part_no"]

    cursor.execute("""

    SELECT
    receive_date,
    'RECEIVE',
    receive_qty
    FROM assy_spare_receive
    WHERE part_no=%s

    UNION ALL

    SELECT
    issue_date,
    'ISSUE',
    issue_qty
    FROM assy_spare_issue
    WHERE part_no=%s

    ORDER BY 1

    """,(part_no, part_no))

    report_data = cursor.fetchall()

    return render_template(
        "assy_stock_card_result.html",
        report_data=report_data,
        part_no=part_no
    )
# =================================
# QUALITY DASHBOARD
# =================================

@app.route("/quality_dashboard")
def quality_dashboard():

    cursor.execute("""
    SELECT
    IFNULL(SUM(production_qty),0),
    IFNULL(SUM(defect_qty),0)
    FROM quality_defects
    """)

    data = cursor.fetchone()

    production_qty = data[0]
    defect_qty = data[1]

    if production_qty > 0:

        ppm = round(
            (defect_qty / production_qty) * 1000000,
            2
        )

        fpy = round(
            ((production_qty - defect_qty)
            / production_qty) * 100,
            2
        )

    else:
        ppm = 0
        fpy = 0

    # LPC DEFECT

    cursor.execute("""
    SELECT COUNT(*)
    FROM quality_defects
    WHERE defect_category='LPC DEFECT'
    """)
    lpc_defect = cursor.fetchone()[0]

    # DOCK DEFECT

    cursor.execute("""
    SELECT COUNT(*)
    FROM quality_defects
    WHERE defect_category='DOCK DEFECT'
    """)
    dock_defect = cursor.fetchone()[0]

    # VISUAL DEFECT

    cursor.execute("""
    SELECT COUNT(*)
    FROM quality_defects
    WHERE defect_category='VISUAL DEFECT'
    """)
    visual_defect = cursor.fetchone()[0]

    # TOTAL DEFECT

    total_defect = (
        lpc_defect +
        dock_defect +
        visual_defect
    )

    # GOOD QTY

    good_qty = (
        production_qty -
        defect_qty
    )

    # DEFECT LIST

    cursor.execute("""
    SELECT *
    FROM quality_defects
    ORDER BY id DESC
    LIMIT 50
    """)
    defects = cursor.fetchall()

    # MACHINE WISE DEFECT

    cursor.execute("""

SELECT

machine_name,
SUM(defect_qty)

FROM quality_defects

GROUP BY machine_name

ORDER BY SUM(defect_qty) DESC

    """)

    machine_data = cursor.fetchall()


    # MONTHLY PPM TREND

    cursor.execute("""

SELECT

DATE_FORMAT(
MIN(defect_date),
'%b'
) AS month,

ROUND(
(
SUM(defect_qty) /
NULLIF(SUM(production_qty),0)
) * 1000000,
2
) AS ppm

FROM quality_defects

GROUP BY
YEAR(defect_date),
MONTH(defect_date)

ORDER BY
YEAR(defect_date),
MONTH(defect_date)

""")

    ppm_trend = cursor.fetchall()

    return render_template(
        "quality_dashboard.html",
        production_qty=production_qty,
        defect_qty=defect_qty,
        ppm=ppm,
        fpy=fpy,
        lpc_defect=lpc_defect,
        dock_defect=dock_defect,
        visual_defect=visual_defect,
        total_defect=total_defect,
        good_qty=good_qty,
        defects=defects,
        machine_data=machine_data,
        ppm_trend=ppm_trend
    )
@app.route("/quality_defect_entry")
def quality_defect_entry():

    today = datetime.now().strftime("%Y-%m-%d")

    return render_template(
        "quality_defect_entry.html",
        defect_date=today
    )

# ===============================
# SAVE QUALITY DEFECT
# ===============================

@app.route("/save_quality_defect", methods=["POST"])
def save_quality_defect():

    defect_date = request.form["defect_date"]
    machine_name = request.form["machine_name"]
    part_no = request.form["part_no"]
    defect_category = request.form["defect_category"]
    defect_type = request.form["defect_type"]
    production_qty = request.form["production_qty"]
    defect_qty = request.form["defect_qty"]
    inspector = request.form["inspector"]
    remarks = request.form["remarks"]

    cursor.execute("""
    INSERT INTO quality_defects(

        defect_date,
        machine_name,
        part_no,
        defect_category,
        defect_type,
        production_qty,
        defect_qty,
        inspector,
        remarks

    )

    VALUES(

        %s,%s,%s,%s,%s,%s,%s,%s,%s

    )

    """,

    (

        defect_date,
        machine_name,
        part_no,
        defect_category,
        defect_type,
        production_qty,
        defect_qty,
        inspector,
        remarks

    ))

    db.commit()

    flash("✅ Quality Defect Saved Successfully")

    return redirect("/quality_dashboard")
import pandas as pd
from flask import send_file

@app.route("/download_quality_excel")
def download_quality_excel():

    query = """
    SELECT *
    FROM quality_defects
    """

    df = pd.read_sql(query, db)

    file_path = "quality_report.xlsx"

    df.to_excel(
        file_path,
        index=False
    )

    return send_file(
        file_path,
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)
