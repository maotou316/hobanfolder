//**************************************************
// File:    SortByDate.js
// Author:  Yulin Huang
//
// Move files to subFolders by Date
//**************************************************
var vbOKCancel = 1;
var vbOK = 1;
var vbInformation = 64;
var vbCancel = 2;
var result;

var Message = "���T�w�N�|�}�l�N�ɮ׫������J��Ƨ��A�p������Ы�����";
var Title = "�нT�{";
var start = new Date().getTime();

// Create the WshShell object variable.
var WshShell = WScript.CreateObject("WScript.Shell");

result = WshShell.Popup(
            Message,
            0,
            Title,
            vbOKCancel + vbInformation); // Show dialog box.

if (result == vbCancel) WScript.Quit();

var path = GetPath();
var fn = GetFileName();

var wsh = WScript.CreateObject("WScript.Shell");

// Create FileSystemObject object to access the file system.
var fso = WScript.CreateObject("Scripting.FileSystemObject");

// Get Folders collection.
var oFolder = fso.GetFolder(wsh.ExpandEnvironmentStrings(path));
var oFiles = new Enumerator(oFolder.Files);   // Files collection

var countFiles = 0;
var countFolders = 0;

for (; !oFiles.atEnd(); oFiles.moveNext())   // All files
{
    var oFile = oFiles.item();
    if (oFile.name == fn) continue;

    var fileDate = new Date(Date.parse(oFile.DateLastModified));
    var fileYDM = fileDate.getFullYear().toString() +
                  zeroit(fileDate.getMonth() + 1) +
                  zeroit(fileDate.getDate());
    
    var folderYDM = path + fileYDM;
    var MoveTo = folderYDM + "\\" + oFile.name;

    if (!fso.FolderExists(folderYDM)) {
        fso.CreateFolder(folderYDM);
        countFolders++;n
    }

    // Todo: �p�G�ɮפw�s�b�A�����O�_�ۦP
    if (fso.FileExists(MoveTo)) {
        if (IsSameFile(oFile, fso.GetFile(MoveTo))) {
            oFile.Move(MoveTo); // �ۦP���ɮסA�л\
        } else {
            MoveTo = RenameFile(MoveTo); // ���P�ɮסA���s�R�W
            oFile.Move(MoveTo);
        }
    } else {
        oFile.Move(MoveTo);
    }

    countFiles++;
}

var end = new Date().getTime();
var time = (end - start) / 1000;

WScript.Echo("�w�إ�" + countFolders + "�ӷs��Ƨ��A�ñN" + countFiles + "���ɮ׫��Ӥ����J��Ƨ���\n�@��F" + time + "��");

function GetPath() {
    var path = WScript.ScriptFullName;
    path = path.substr(0, path.lastIndexOf("\\") + 1);
    return path;
}

function GetFileName() {
    var path = WScript.ScriptFullName;
    var ln = path.length;
    var p = path.lastIndexOf("\\");
    var filename = path.substr(p + 1, ln - p - 1);
    return filename;
}

function zeroit(str) {
    return str < 10 ? "0" + str : str.toString();
}

function RenameFile(filePath) {
    var ext = filePath.substring(filePath.lastIndexOf('.'));
    var baseName = filePath.substring(0, filePath.lastIndexOf('.'));
    var counter = 1;

    while (fso.FileExists(filePath)) {
        filePath = baseName + "_" + counter + ext;
        counter++;
    }

    return filePath;
}

function IsSameFile(file1, file2) {
    // ����ɮת��j�p�M���e�O�_�ۦP
    if (file1.Size != file2.Size) {
        return false;
    }

    // �}���ɮ�Ū���ä�����e
    var stream1 = fso.OpenTextFile(file1.Path, 1);
    var stream2 = fso.OpenTextFile(file2.Path, 1);

    var isSame = true;
    while (!stream1.AtEndOfStream && !stream2.AtEndOfStream) {
        if (stream1.Read(1024) != stream2.Read(1024)) {
            isSame = false;
            break;
        }
    }

    stream1.Close();
    stream2.Close();

    return isSame;
}
//*** End
