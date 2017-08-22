'explorado.vbs
'Adaptado de https://ss64.com/vb/syntax-userinfo.html

On Error Resume Next
Dim objSysInfo, objUser
Set objSysInfo = CreateObject("ADSystemInfo")
Set objUser = GetObject("LDAP://" & objSysInfo.UserName)
WScript.Echo "DN: " & objUser.distinguishedName
WScript.Echo "First name: " & objUser.givenName
WScript.Echo "First name: " & objUser.FirstName
WScript.Echo "Last name: " & objUser.sn
'WScript.Echo "Last name: " & objUser.LastName
WScript.Echo "Display name: " & objUser.displayName
'WScript.Echo "Display name: " & objUser.FullName
WScript.Echo "Email: " & objUser.mail
WScript.Echo "User logon name: " & objUser.userPrincipalName
WScript.Echo "pre-Windows 2000 logon name: " & objUser.sAMAccountName
WScript.Echo "AccountDisabled: " & objUser.AccountDisabled
WScript.Echo "User must change password at next logon: " & objUser.pwdLastSet
WScript.Echo "User cannot change password: " & objUser.userAccountControl
WScript.Echo "Profile path: " & objUser.profilePath
WScript.Echo "Logon script: " & objUser.scriptPath
WScript.Echo "Home folder, local path: " & objUser.homeDirectory
WScript.Echo "Home folder, Connect, Drive: " & objUser.homeDrive
WScript.Echo "Home folder, Connect, To:: " & objUser.homeDirectory
WScript.Echo "Mobile: " & objUser.mobile
WScript.Echo "Notes: " & objUser.info
