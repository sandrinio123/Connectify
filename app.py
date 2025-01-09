from ext import app
from routes import home, register, login, logout, delete_blog, blog_contents, profiles, user_blogs, create_post

app.run(debug=True, host="0.0.0.0")
