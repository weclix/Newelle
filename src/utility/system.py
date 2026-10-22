import subprocess
import os
import re
import shlex

def is_wayland() -> bool:
    """
    Check if we are in a Wayland environment

    Returns:
        bool: True if we are in a Wayland environment
    """
    if os.getenv("WAYLAND_DISPLAY"):
        return True
    return False

def voice_mode_layer_shell_available() -> bool:
    """Return whether GTK Layer Shell can position the Voice Mode pill."""
    try:
        import gi

        gi.require_version("Gtk4LayerShell", "1.0")
        from gi.repository import Gtk4LayerShell
    except (ImportError, ValueError):
        return False
    try:
        return bool(Gtk4LayerShell.is_supported())
    except Exception:
        return False

def open_website(website):
    """Opens a website using xdg-open

    Args:
        website (): url of the website 
    """
    subprocess.Popen(["gio", "open", website])

def open_folder(folder):
    """Opens a website using xdg-open

    Args:
        folder (): location of the folder 
    """
    subprocess.Popen(["gio", "open", folder])


def open_in_external_terminal(command: str, external_terminal: str) -> bool:
    """
    Run a command in the external terminal chosen by the user.

    The external terminal setting is a command template that may contain
    ``{0}``, which is replaced with the command to run. When the template has
    no placeholder, the command is appended as the last argument.

    Args:
        command: shell command to run in the terminal
        external_terminal: external terminal command template

    Returns:
        bool: True if the terminal was started, False otherwise
    """
    template = (external_terminal or "").strip()
    if template == "":
        return False
    try:
        arguments = shlex.split(template)
    except ValueError:
        return False
    if len(arguments) == 0:
        return False
    placeholder_found = False
    for i, argument in enumerate(arguments):
        if "{0}" in argument:
            arguments[i] = argument.replace("{0}", command)
            placeholder_found = True
    if not placeholder_found:
        arguments.append(command)
    try:
        subprocess.Popen(arguments)
    except OSError:
        return False
    return True


def has_backend(backend: str, spawn: bool = True) -> bool:
    """Check if a GPU/compute backend is available on the system.

    Args:
        backend: One of "cuda", "rocm", "vulkan", "openvino", "sycl"
        spawn: If True, use a spawn prefix for subprocess calls (Flatpak support removed)

    Returns:
        bool: True if the backend appears to be available
    """
    # Flatpak support removed: no spawn prefix needed
    cmd_prefix = []

    def _run_check(cmd):
        try:
            result = subprocess.run(
                cmd_prefix + cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def _path_check(path):
        return os.path.exists(path)

    if backend == "cuda":
        if _run_check(["nvidia-smi"]):
            return True
        return _path_check("/proc/driver/nvidia/version")

    elif backend == "rocm":
        if _run_check(["rocminfo"]):
            return True
        return _path_check("/opt/rocm")

    elif backend == "vulkan":
        if _run_check(["vulkaninfo"]):
            return True
        icd_dir = "/usr/share/vulkan/icd.d"
        if os.path.isdir(icd_dir):
            return any(f.endswith(".json") for f in os.listdir(icd_dir))
        return False

    elif backend == "openvino":
        # OpenVINO runtime ships a benchmark tool, and the Python package is
        # commonly installed alongside it. Accept either signal.
        if _run_check(["benchmark_app", "-h"]):
            return True
        return _run_check(["python3", "-c", "import openvino"])

    elif backend == "sycl":
        # oneAPI / DPC++ SYCL toolchain. The sycl-ls utility lists SYCL devices
        # and is shipped with the Intel oneAPI compiler; ocloc targets Intel GPUs.
        if _run_check(["sycl-ls"]):
            return True
        return _path_check("/opt/intel/oneAPI")

    return False


def detect_cuda_version() -> float | None:
    """Detect the installed CUDA runtime version.

    Tries nvcc first, then falls back to nvidia-smi output.

    Returns:
        The major.minor CUDA version as a float (e.g. 12.8, 13.2, 11.7),
        or None if CUDA is not found.
    """
    # Flatpak support removed: no spawn prefix needed
    cmd_prefix = []

    try:
        result = subprocess.run(
            cmd_prefix + ["nvcc", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            match = re.search(r"release\s+(\d+)\.(\d+)", result.stdout)
            if match:
                return float(f"{match.group(1)}.{match.group(2)}")
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    try:
        result = subprocess.run(
            cmd_prefix + ["nvidia-smi"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            match = re.search(r"CUDA Version:\s+(\d+)\.(\d+)", result.stdout)
            if match:
                return float(f"{match.group(1)}.{match.group(2)}")
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return None
