@echo off
REM Augmente le volume système de 10 % (5 presses de touches)
powershell -Command ^
$wsh = New-Object -ComObject WScript.Shell; ^
for ($i=0; $i -lt 5; $i++) { $wsh.SendKeys([char]175); Start-Sleep -Milliseconds 50 }