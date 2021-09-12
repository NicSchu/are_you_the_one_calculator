@echo off
echo %1
echo %2

mkdir ..\releases\%1
mkdir ..\releases\%1\%1%2
IF %2 == "" (
move .\dist\calculator ..\releases\%1\%1%2\calculator
) ELSE (
move .\dist\calculator.exe ..\releases\%1\%1%2\calculator.exe
)
7z a -r ..\releases\%1\%1%2.zip ..\releases\%1\%1%2
7z a -r ..\releases\%1\%1%2.7z ..\releases\%1\%1%2