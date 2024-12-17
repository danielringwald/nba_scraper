from .index import app
import os

if __name__ == "__main__":
    print(os.getcwd())
    app.run(debug=False)
