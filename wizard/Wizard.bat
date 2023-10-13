@echo off

rem Vérifier les privilèges administratifs
>nul 2>&1 net session
if %errorlevel% neq 0 (
    echo Ce script necessite des droits administrateur. Veuillez lancer installer.vbs.
    pause
    exit /b
)

setlocal enabledelayedexpansion

rem Variables d'installation de Python
set "pythonVersion=3.11.3"
set "pythonURL=https://www.python.org/ftp/python/%pythonVersion%/python-%pythonVersion%-amd64.exe"
set "installDir=C:\Python%pythonVersion%"

rem Vérifier si Python est déjà installé
python --version > nul 2>&1
if %errorlevel% equ 0 (
    echo Python est deja installe sur ce systeme.
    set /p "continue=Installer les bibliotheques Yacam ? (y/n): "
    if /i "!continue!"=="y" (
        goto install_libraries
    ) else (
        echo Arret du script.
        timeout /t 3 > nul
        exit /b
    )
) else (
    rem Installation de Python
    echo **************************************
    echo        INSTALLATION DE PYTHON
    echo **************************************
    echo.

    rem Téléchargement de Python %pythonVersion%...
    "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "(New-Object System.Net.WebClient).DownloadFile('%pythonURL%', 'python-%pythonVersion%-amd64.exe')"

    rem Vérifier si le téléchargement a réussi
    if not exist python-%pythonVersion%-amd64.exe (
        echo ERROR : Echec du telechargement de Python.
        timeout /t 3 > nul
        exit /b
    )

    rem Installation de Python %pythonVersion%...
    start /wait python-%pythonVersion%-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    rem Configuration du chemin d'accès (PATH)
    echo Configuration du chemin d'accès...
    setx /m PATH "!installDir!;!installDir%\Scripts;!PATH!"

    rem Nettoyage des fichiers temporaires
    echo Nettoyage des fichiers temporaires...
    del python-%pythonVersion%-amd64.exe

    echo Installation de Python terminee.

    :install_libraries
    rem Installation des bibliothèques Yacam
    echo **************************************
    echo     INSTALLATION DES MODULES ORA
    echo **************************************
    echo.

    where pip > nul 2>&1
    if %errorlevel% equ 0 (
        pip install ultralytics supervision requests network
        cd yolov5
        pip install -r requirements.txt
        echo y | pip uninstall torch
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ) else (
        echo ERROR : pip n'est pas installe.
    )
)

timeout /t 3 > nul