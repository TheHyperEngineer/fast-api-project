"""
Bootstrap module. This file provides a minimal script-style entrypoint that
instantiates the Application class and runs it. This is the clear entry point
for the application (analogous to Spring Boot's main class).
"""

from app.application import Application

_application = Application()
app = _application.get_app()


if __name__ == "__main__":
    # When run directly, start the uvicorn server (keeps same behavior as before)
    _application.run(host="0.0.0.0", port=8000, reload=True)
