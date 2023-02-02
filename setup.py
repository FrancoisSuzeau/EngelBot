from cx_Freeze import setup, Executable
import os

# if your architecture is different then don't hesitate to change the relative path of your file when the main call is
executables = [
        Executable(
            script="bot.py", 
            base=None,
            targetName="EngelBot.exe",
            icon = None # if you want to use an icon file, specify the file name here
        )
]

packages = ["idna", "os", "discord", "pandas", "dotenv", "tensorflow", "nltk", "numpy", "tflearn", "random", "json", "pickle", "shutil"]
includefiles = [os.path.join(".", "materials"), os.path.join(".", "packages")] #include path of your personnal module if they are not located in the same directory of your main script
binaries = []
excludes = [
    'tkinter', 'jupyter-client', 'ipykernel', 'jupyter-core', 'matplotlib-inline', 'pyinstaller-hooks-contrib', 'pip', 'pytest', 'cx-freeze',
    'plotly','pyinstaller', 'matplotlib', 'markdown', 'google-auth', 'keras', 'windows-curses', 'speedtest-cli', 
    'py', 'scipy', 'pyspeedtest', 'scikit-learn', 'wheel' 'seaborn', 'google-auth-oauthlib', 'colorama', 'google-pasta', 'sklearn', 'halfedge-mesh'
]
options = {
    'build_exe': {    
        'excludes':excludes,
        'packages':packages,
        'include_files':includefiles,
        'bin_includes':binaries,
        "include_msvcr": True
    },
}
# all the external module (such as matplot lib etc is copy directly in the lib directory and then transformed in a dynamic library file)

# change the name field with name of your application
setup(
    name = "EngelBot",
    options = options,
    version = "1.0",
    description = 'Un bot discord',
    executables = executables
)

# the executable is in the 'build/exe.win-amd64-xx' directory but named as the name of your main file