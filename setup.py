"""Build script for Newelle (see pyproject.toml for metadata).

Build-time tools: glib-compile-resources, glib-compile-schemas, msgfmt.
"""
import shutil
import subprocess
from pathlib import Path

from setuptools import Command, find_packages, setup
from setuptools.command.build_py import build_py

APP_ID = "io.github.qwersyk.Newelle"

# Relative to the project root, which is the working directory during builds.
GENERATED = Path("build") / "newelle-data"
PACKAGE_DATA = GENERATED / "package"  # copied into the package as newelle/_data
SYSTEM_DATA = GENERATED / "system"  # installed under <prefix>/share

# Modules kept in src/ that are not shipped: stripped features and unused extensions.
EXCLUDED_MODULES = {
    "newelle.divergence",
    "newelle.vision",
    "newelle.handlers.memory.llamaindex_memory_handler",
}


def run_tool(*args):
    subprocess.run([str(arg) for arg in args], check=True)


def linguas():
    lines = Path("po/LINGUAS").read_text().splitlines()
    return [lang for line in lines for lang in line.split("#")[0].split()]


class BuildData(Command):
    description = "compile the GResource bundle, GSettings schema, translations and desktop files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree(GENERATED, ignore_errors=True)
        share = PACKAGE_DATA / "share"

        PACKAGE_DATA.mkdir(parents=True)
        run_tool("glib-compile-resources", "--sourcedir=src",
                 f"--target={PACKAGE_DATA / 'newelle.gresource'}", "src/newelle.gresource.xml")

        schemas = share / "glib-2.0" / "schemas"
        schemas.mkdir(parents=True)
        shutil.copy(f"data/{APP_ID}.gschema.xml", schemas)
        run_tool("glib-compile-schemas", "--strict", schemas)

        icons = share / "icons" / "hicolor"
        shutil.copytree("data/icons/hicolor", icons)
        for svg in Path("data/icons").glob("*.svg"):
            shutil.copy(svg, icons / "symbolic" / "apps")
        shutil.copy("data/icons/lobehub-icons.LICENSE", share / "icons")

        for lang in linguas():
            target = share / "locale" / lang / "LC_MESSAGES"
            target.mkdir(parents=True)
            run_tool("msgfmt", "-o", target / "newelle.mo", f"po/{lang}.po")

        (SYSTEM_DATA / "applications").mkdir(parents=True)
        run_tool("msgfmt", "--desktop", "-d", "po", "--template", f"data/{APP_ID}.desktop.in",
                 "-o", SYSTEM_DATA / "applications" / f"{APP_ID}.desktop")
        (SYSTEM_DATA / "appdata").mkdir(parents=True)
        run_tool("msgfmt", "--xml", "-d", "po", "--template", f"data/{APP_ID}.appdata.xml.in",
                 "-o", SYSTEM_DATA / "appdata" / f"{APP_ID}.appdata.xml")


class BuildPy(build_py):
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return [m for m in modules if f"{m[0]}.{m[1]}" not in EXCLUDED_MODULES]

    def run(self):
        self.run_command("build_data")
        super().run()
        if not self.dry_run:
            shutil.copytree(PACKAGE_DATA, Path(self.build_lib) / "newelle" / "_data",
                            dirs_exist_ok=True)


setup(
    package_dir={"newelle": "src"},
    # Package data comes only from build_data, not from MANIFEST.in (sdist only).
    include_package_data=False,
    packages=["newelle"] + [f"newelle.{name}" for name in find_packages("src")],
    data_files=[
        ("share/applications", [(SYSTEM_DATA / "applications" / f"{APP_ID}.desktop").as_posix()]),
        ("share/appdata", [(SYSTEM_DATA / "appdata" / f"{APP_ID}.appdata.xml").as_posix()]),
        ("share/icons/hicolor/scalable/apps", [f"data/icons/hicolor/scalable/apps/{APP_ID}.svg"]),
        ("share/icons/hicolor/symbolic/apps", [f"data/icons/hicolor/symbolic/apps/{APP_ID}-symbolic.svg"]),
    ],
    cmdclass={"build_data": BuildData, "build_py": BuildPy},
)
