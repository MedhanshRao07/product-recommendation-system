"""
╔══════════════════════════════════════════════════════════════╗
║              🛍️  Suggestify — Project Launcher               ║
║                                                              ║
║   Start the entire full-stack application with one command:  ║
║                      python run.py                           ║
║                                                              ║
║   Options:                                                   ║
║     python run.py              → Start everything            ║
║     python run.py --backend    → Start backend only          ║
║     python run.py --frontend   → Start frontend only         ║
║     python run.py --check      → Check dependencies only     ║
║     python run.py --install    → Install all dependencies    ║
║                                                              ║
║   Press Ctrl+C to gracefully shut down all services.         ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys

# Fix Windows terminal encoding so Unicode characters display correctly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import subprocess
import signal
import time
import shutil
import argparse
from pathlib import Path


# ──────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
VENV_DIR = BACKEND_DIR / "venv"
VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
VENV_PIP = VENV_DIR / "Scripts" / "pip.exe"
BACKEND_REQUIREMENTS = PROJECT_ROOT / "requirements.txt"
BACKEND_ENV_FILE = BACKEND_DIR / ".env"
ENV_EXAMPLE = PROJECT_ROOT / "config" / ".env.example"

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
REACT_PORT = 3000

# ANSI color codes for pretty terminal output
class Colors:
    HEADER  = "\033[95m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"


# ──────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────
def log(icon, message, color=Colors.RESET):
    """Print a formatted log message."""
    print(f"  {color}{icon}  {message}{Colors.RESET}")


def log_header(title):
    """Print a section header."""
    print()
    print(f"  {Colors.BOLD}{Colors.CYAN}{'─' * 56}{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.CYAN}  {title}{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.CYAN}{'─' * 56}{Colors.RESET}")


def log_success(message):
    log("✅", message, Colors.GREEN)


def log_warning(message):
    log("⚠️ ", message, Colors.YELLOW)


def log_error(message):
    log("❌", message, Colors.RED)


def log_info(message):
    log("ℹ️ ", message, Colors.BLUE)


def log_working(message):
    log("⏳", message, Colors.DIM)


# ──────────────────────────────────────────────────────────────
# Dependency Checks
# ──────────────────────────────────────────────────────────────
def check_python():
    """Verify Python is available and meets minimum version."""
    version = sys.version_info
    if version >= (3, 8):
        log_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        log_error(f"Python 3.8+ required (found {version.major}.{version.minor})")
        return False


def check_node():
    """Verify Node.js is installed and meets minimum version."""
    node_path = shutil.which("node")
    if not node_path:
        log_error("Node.js not found. Install from https://nodejs.org/")
        return False
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=10
        )
        version_str = result.stdout.strip().lstrip("v")
        major = int(version_str.split(".")[0])
        if major >= 16:
            log_success(f"Node.js v{version_str}")
            return True
        else:
            log_error(f"Node.js 16+ required (found v{version_str})")
            return False
    except Exception as e:
        log_error(f"Could not check Node.js version: {e}")
        return False


def check_npm():
    """Verify npm is installed."""
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    npm_path = shutil.which(npm_cmd)
    if not npm_path:
        log_error("npm not found. It should come with Node.js.")
        return False
    try:
        result = subprocess.run(
            [npm_cmd, "--version"],
            capture_output=True, text=True, timeout=10
        )
        log_success(f"npm v{result.stdout.strip()}")
        return True
    except Exception:
        log_error("Could not check npm version.")
        return False


def check_venv():
    """Verify the backend virtual environment exists."""
    if VENV_PYTHON.exists():
        log_success(f"Backend venv found at {VENV_DIR.relative_to(PROJECT_ROOT)}")
        return True
    else:
        log_warning("Backend venv not found.")
        log_info(f"Create it with: python -m venv {VENV_DIR}")
        return False


def check_env_file():
    """Verify the backend .env file exists."""
    if BACKEND_ENV_FILE.exists():
        log_success(".env file found in backend/")
        return True
    else:
        log_warning(".env file missing in backend/")
        if ENV_EXAMPLE.exists():
            log_info(f"Copy the template:  copy config\\.env.example backend\\.env")
        return False


def check_node_modules():
    """Verify frontend node_modules exist."""
    node_modules = FRONTEND_DIR / "node_modules"
    if node_modules.exists() and any(node_modules.iterdir()):
        log_success("Frontend node_modules installed")
        return True
    else:
        log_warning("Frontend node_modules not found.")
        log_info("Run:  python run.py --install")
        return False


def check_all_dependencies():
    """Run all dependency checks and return True if everything passes."""
    log_header("🔍  Dependency Check")
    results = [
        check_python(),
        check_node(),
        check_npm(),
        check_venv(),
        check_env_file(),
        check_node_modules(),
    ]
    print()
    if all(results):
        log_success("All dependencies satisfied! Ready to launch.")
        return True
    else:
        log_warning("Some checks failed. Fix the issues above before starting.")
        return False


# ──────────────────────────────────────────────────────────────
# Dependency Installation
# ──────────────────────────────────────────────────────────────
def install_backend_deps():
    """Create venv (if needed) and install Python dependencies."""
    log_header("📦  Backend Dependencies")

    # Create venv if it doesn't exist
    if not VENV_PYTHON.exists():
        log_working("Creating virtual environment...")
        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=True
        )
        log_success("Virtual environment created.")

    # Install/upgrade pip
    log_working("Upgrading pip...")
    subprocess.run(
        [str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip"],
        capture_output=True, check=True
    )

    # Install requirements
    if BACKEND_REQUIREMENTS.exists():
        log_working("Installing Python packages from requirements.txt...")
        result = subprocess.run(
            [str(VENV_PIP), "install", "-r", str(BACKEND_REQUIREMENTS)],
            cwd=str(BACKEND_DIR)
        )
        if result.returncode == 0:
            log_success("Backend dependencies installed.")
        else:
            log_error("Failed to install some backend dependencies.")
            return False
    else:
        log_warning("requirements.txt not found in backend/")

    # Copy .env if missing
    if not BACKEND_ENV_FILE.exists() and ENV_EXAMPLE.exists():
        shutil.copy2(str(ENV_EXAMPLE), str(BACKEND_ENV_FILE))
        log_success("Copied .env.example → backend/.env (edit with your credentials!)")

    return True


def install_frontend_deps():
    """Install frontend npm dependencies."""
    log_header("📦  Frontend Dependencies")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

    if not FRONTEND_DIR.exists():
        log_error("frontend/ directory not found!")
        return False

    log_working("Installing npm packages (this may take a minute)...")
    result = subprocess.run(
        [npm_cmd, "install"],
        cwd=str(FRONTEND_DIR)
    )
    if result.returncode == 0:
        log_success("Frontend dependencies installed.")
        return True
    else:
        log_error("Failed to install frontend dependencies.")
        return False


def install_all():
    """Install all dependencies for both backend and frontend."""
    print(f"\n  {Colors.BOLD}{Colors.HEADER}"
          f"🛍️  Suggestify — Installing Dependencies"
          f"{Colors.RESET}\n")
    ok_back = install_backend_deps()
    ok_front = install_frontend_deps()
    print()
    if ok_back and ok_front:
        log_success("All dependencies installed! Run: python run.py")
    else:
        log_warning("Some installations had issues. Check the output above.")


# ──────────────────────────────────────────────────────────────
# Process Management
# ──────────────────────────────────────────────────────────────
class ProcessManager:
    """
    Manages backend and frontend subprocesses.
    Ensures clean startup and graceful shutdown.
    """

    def __init__(self):
        self.processes = {}
        self._shutting_down = False

    def start_backend(self):
        """Start the Flask backend using the venv Python."""
        log_header("🚀  Starting Flask Backend")

        if not VENV_PYTHON.exists():
            log_error("Backend venv not found. Run: python run.py --install")
            return False

        # Build the environment: inherit current env + set PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)

        log_info(f"Using Python: {VENV_PYTHON.relative_to(PROJECT_ROOT)}")
        log_info(f"PYTHONPATH:   {PROJECT_ROOT}")
        log_working(f"Starting Flask on http://localhost:{FLASK_PORT} ...")

        try:
            process = subprocess.Popen(
                [
                    str(VENV_PYTHON),
                    "-m", "backend.app"
                ],
                cwd=str(PROJECT_ROOT),
                env=env,
                # Pipe nothing — let Flask output go directly to this terminal
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                if sys.platform == "win32" else 0,
            )
            self.processes["backend"] = process
            time.sleep(2)  # Give Flask a moment to start

            if process.poll() is None:
                log_success(f"Flask backend running   →  http://localhost:{FLASK_PORT}")
                return True
            else:
                log_error(f"Backend exited with code {process.returncode}")
                return False
        except Exception as e:
            log_error(f"Failed to start backend: {e}")
            return False

    def start_frontend(self):
        """Start the React dev server via npm."""
        log_header("🚀  Starting React Frontend")

        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

        if not (FRONTEND_DIR / "node_modules").exists():
            log_error("node_modules not found. Run: python run.py --install")
            return False

        log_working(f"Starting React on http://localhost:{REACT_PORT} ...")

        env = os.environ.copy()
        env["BROWSER"] = "none"  # Don't auto-open browser
        env["PORT"] = str(REACT_PORT)

        try:
            process = subprocess.Popen(
                [npm_cmd, "start"],
                cwd=str(FRONTEND_DIR),
                env=env,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                if sys.platform == "win32" else 0,
            )
            self.processes["frontend"] = process
            time.sleep(3)  # Give React a moment to compile

            if process.poll() is None:
                log_success(f"React frontend running  →  http://localhost:{REACT_PORT}")
                return True
            else:
                log_error(f"Frontend exited with code {process.returncode}")
                return False
        except Exception as e:
            log_error(f"Failed to start frontend: {e}")
            return False

    def shutdown(self):
        """Gracefully shut down all running processes."""
        if self._shutting_down:
            return
        self._shutting_down = True

        print()
        log_header("🛑  Shutting Down")

        for name, process in self.processes.items():
            if process.poll() is None:
                log_working(f"Stopping {name} (PID {process.pid})...")
                try:
                    if sys.platform == "win32":
                        # On Windows, terminate the process tree
                        subprocess.run(
                            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                            capture_output=True,
                            timeout=10
                        )
                    else:
                        process.terminate()
                        process.wait(timeout=5)
                    log_success(f"{name} stopped.")
                except subprocess.TimeoutExpired:
                    process.kill()
                    log_warning(f"{name} force-killed.")
                except Exception as e:
                    log_warning(f"Error stopping {name}: {e}")
            else:
                log_info(f"{name} already exited (code {process.returncode})")

        print()
        log_success("All services stopped. Goodbye! 👋")
        print()

    def wait(self):
        """Block until Ctrl+C or a process exits unexpectedly."""
        print()
        print(f"  {Colors.BOLD}{Colors.GREEN}{'═' * 56}{Colors.RESET}")
        print(f"  {Colors.BOLD}{Colors.GREEN}"
              f"  🎉  Suggestify is running!"
              f"{Colors.RESET}")
        print(f"  {Colors.BOLD}{Colors.GREEN}{'═' * 56}{Colors.RESET}")
        print()
        log_info(f"Backend  →  http://localhost:{FLASK_PORT}")
        log_info(f"Frontend →  http://localhost:{REACT_PORT}")
        print()
        log_info(f"Press {Colors.BOLD}Ctrl+C{Colors.RESET}{Colors.BLUE} to stop all services.")
        print()

        try:
            while True:
                # Check if any process has died unexpectedly
                for name, process in self.processes.items():
                    if process.poll() is not None and not self._shutting_down:
                        log_warning(
                            f"{name} exited unexpectedly (code {process.returncode})"
                        )
                        self.shutdown()
                        return
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()


# ──────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────
def print_banner():
    banner = f"""
  {Colors.BOLD}{Colors.HEADER}
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║       🛍️   S U G G E S T I F Y                           ║
  ║       AI-Powered Product Recommendations                 ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
  {Colors.RESET}"""
    print(banner)


# ──────────────────────────────────────────────────────────────
# Main Entry Point
# ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🛍️ Suggestify — Full-Stack Project Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py              Start both backend and frontend
  python run.py --backend    Start backend only
  python run.py --frontend   Start frontend only
  python run.py --check      Check if all dependencies are ready
  python run.py --install    Install all dependencies
        """
    )
    parser.add_argument(
        "--backend", action="store_true",
        help="Start only the Flask backend"
    )
    parser.add_argument(
        "--frontend", action="store_true",
        help="Start only the React frontend"
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Check all dependencies without starting"
    )
    parser.add_argument(
        "--install", action="store_true",
        help="Install all dependencies (creates venv, pip install, npm install)"
    )

    args = parser.parse_args()

    # ── Handle --check ──
    if args.check:
        print_banner()
        ok = check_all_dependencies()
        sys.exit(0 if ok else 1)

    # ── Handle --install ──
    if args.install:
        print_banner()
        install_all()
        sys.exit(0)

    # ── Start services ──
    print_banner()

    # Quick pre-flight check
    if not check_all_dependencies():
        print()
        log_info("Run 'python run.py --install' to fix missing dependencies.")
        print()
        sys.exit(1)

    manager = ProcessManager()

    # Register signal handler for graceful shutdown
    def handle_signal(signum, frame):
        manager.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    if sys.platform == "win32":
        signal.signal(signal.SIGBREAK, handle_signal)
    else:
        signal.signal(signal.SIGTERM, handle_signal)

    # Determine what to start
    start_back = args.backend or (not args.backend and not args.frontend)
    start_front = args.frontend or (not args.backend and not args.frontend)

    if start_back:
        if not manager.start_backend():
            log_error("Backend failed to start. Check errors above.")
            manager.shutdown()
            sys.exit(1)

    if start_front:
        if not manager.start_frontend():
            log_error("Frontend failed to start. Check errors above.")
            manager.shutdown()
            sys.exit(1)

    manager.wait()


if __name__ == "__main__":
    main()
