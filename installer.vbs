Set objShell = CreateObject("WScript.Shell")
osType = objShell.RegRead("HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProductName")
If InStr(osType, "Windows") = 0 Then
    WScript.Echo "Ce script ne peut etre execute que sur un systeme Windows."
    WScript.Sleep 3000 ' Delai 3 secondes
    WScript.Quit
End If

scriptPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1)
batchPath = scriptPath & "\wizardOra\Wizard.bat"
batchPath = Replace(batchPath, "/", "\\")

Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "cmd.exe", "/c """ & batchPath & """", "", "runas", 1