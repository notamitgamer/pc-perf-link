Set fso = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

' 1. DEFINE PATHS
targetFolder = "G:\platform-tools-latest-windows\platform-tools"
' Using python.exe instead of pythonw.exe so we can see the window for debugging
pythonPath = "C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe"
scriptPath = targetFolder & "\server_bridge.py"

' 2. CHECK IF FILES EXIST
If Not fso.FolderExists(targetFolder) Then
    MsgBox "Folder not found: " & targetFolder, 16, "Error"
    WScript.Quit
End If

If Not fso.FileExists(pythonPath) Then
    MsgBox "Python not found at: " & pythonPath, 16, "Error"
    WScript.Quit
End If

If Not fso.FileExists(scriptPath) Then
    MsgBox "Script not found: " & scriptPath, 16, "Error"
    WScript.Quit
End If

' 3. EXECUTE
WshShell.CurrentDirectory = targetFolder

' CHANGED: '1' makes the window visible so you can see the error
' Once it works, you can change '1' back to '0' to hide it again
WshShell.Run """" & pythonPath & """ """ & scriptPath & """", 0, False
