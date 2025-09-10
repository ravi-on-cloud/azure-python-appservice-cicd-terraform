from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "change-me"  # needed for flash messages

# Paths & uploads
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB max upload
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("registration.html")

@app.route("/submit", methods=["POST"])
def submit():
    first_name = request.form.get("firstName", "").strip()
    last_name = request.form.get("lastName", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirmPassword", "")
    photo = request.files.get("photo")

    # Server-side validation
    if not first_name or not last_name or not email or not password or not confirm_password or not photo:
        flash("All fields are required.")
        return redirect(url_for("index"))

    if not email.endswith("@gmail.com"):
        flash("Please use a Gmail address.")
        return redirect(url_for("index"))

    if password != confirm_password:
        flash("Passwords do not match.")
        return redirect(url_for("index"))

    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(save_path)
    else:
        flash("Please upload a valid image file (png, jpg, jpeg, gif, webp).")
        return redirect(url_for("index"))

    # Success → show welcome page
    full_name = f"{first_name} {last_name}".strip()
    return render_template("welcome.html", name=full_name)

if __name__ == "__main__":
    # Bind to all interfaces so it's accessible via VM public IP
    app.run(host="0.0.0.0", port=5000, debug=True)

