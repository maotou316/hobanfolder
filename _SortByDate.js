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

var Message = "按確定就會開始將檔案按日期放入資料夾，如不執行請按取消";
var Title = "請確認";
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

    // Todo: 如果檔案已存在，先比對是否相同
    if (fso.FileExists(MoveTo)) {
        if (IsSameFile(oFile, fso.GetFile(MoveTo))) {
            oFile.Move(MoveTo); // 相同的檔案，覆蓋
        } else {
            MoveTo = RenameFile(MoveTo); // 不同檔案，重新命名
            oFile.Move(MoveTo);
        }
    } else {
        oFile.Move(MoveTo);
    }

    countFiles++;
}

var end = new Date().getTime();
var time = (end - start) / 1000;

WScript.Echo("已建立" + countFolders + "個新資料夾，並將" + countFiles + "個檔案按照日期放入資料夾中\n共花了" + time + "秒");

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
    // 比較檔案的大小和內容是否相同
    if (file1.Size != file2.Size) {
        return false;
    }

    // 開啟檔案讀取並比較內容
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
