@echo off

"C:\Program Files (x86)\WinSCP\WinSCP.com" ^
  /log="C:\winscplog\WinSCP.log" /ini=nul ^
  /command ^
    "open ftp://marcos:32922161@melectronica.ddns.net/" ^
    "put C:\logs\* /home/marcos/ftpdata/logs/" ^    
    "exit"

set WINSCP_RESULT=%ERRORLEVEL%
if %WINSCP_RESULT% equ 0 (
  echo Success
) else (
  echo Error
)

exit /b %WINSCP_RESULT%
