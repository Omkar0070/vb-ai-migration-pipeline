' ***********************************************************************************************
' Required Notice: Copyright (C) EPPlus Software AB. 
' This software is licensed under PolyForm Noncommercial License 1.0.0 
' and may only be used for noncommercial purposes 
' https://polyformproject.org/licenses/noncommercial/1.0.0/
' 
' A commercial license to use this software can be purchased at https://epplussoftware.com
' ************************************************************************************************
' Date               Author                       Change
' ************************************************************************************************
' 01/27/2020         EPPlus Software AB           Initial release EPPlus 5
' ***********************************************************************************************
Imports System
Imports System.IO

Namespace EPPlusSamples
    Public Class FileUtil
        Private Shared _outputDir As DirectoryInfo = Nothing
        Public Shared Property OutputDir As DirectoryInfo
            Get
                Return _outputDir
            End Get
            Set(ByVal value As DirectoryInfo)
                _outputDir = value
                If Not _outputDir.Exists Then
                    Call _outputDir.Create()
                End If
            End Set
        End Property
        Public Shared Function GetCleanFileInfo(ByVal file As String) As FileInfo
            Dim fi = New FileInfo(OutputDir.FullName & Path.DirectorySeparatorChar.ToString() & file)
            If fi.Exists Then
                fi.Delete()  ' ensures we create a new workbook
            End If
            Return fi
        End Function
        Public Shared Function GetFileInfo(ByVal file As String) As FileInfo
            Return New FileInfo(OutputDir.FullName & Path.DirectorySeparatorChar.ToString() & file)
        End Function

        Public Shared Function GetFileInfo(ByVal altOutputDir As DirectoryInfo, ByVal file As String, ByVal Optional deleteIfExists As Boolean = True) As FileInfo
            Dim fi = New FileInfo(altOutputDir.FullName & Path.DirectorySeparatorChar.ToString() & file)
            If deleteIfExists AndAlso fi.Exists Then
                fi.Delete()  ' ensures we create a new workbook
            End If
            Return fi
        End Function


        Friend Shared Function GetDirectoryInfo(ByVal directory As String) As DirectoryInfo
            Dim di = New DirectoryInfo(_outputDir.FullName & Path.DirectorySeparatorChar.ToString() & directory)
            If Not di.Exists Then
                di.Create()
            End If
            Return di
        End Function
        ''' <summary>
        ''' Returns a fileinfo with the full path of the requested file
        ''' </summary>
        ''' <paramname="directory">A subdirectory</param>
        ''' <paramname="file"></param>
        ''' <returns></returns>
        Public Shared Function GetFileInfo(ByVal directory As String, ByVal file As String) As FileInfo
            Dim rootDir = GetRootDirectory().FullName
            Return New FileInfo(Path.Combine(rootDir, directory, file))
        End Function

        Public Shared Function GetRootDirectory() As DirectoryInfo
            Dim currentDir = AppDomain.CurrentDomain.BaseDirectory
            While Not currentDir.EndsWith("bin")
                currentDir = Directory.GetParent(currentDir).FullName.TrimEnd("\"c)
            End While
            Return New DirectoryInfo(currentDir).Parent
        End Function

        Public Shared Function GetSubDirectory(ByVal directory As String, ByVal subDirectory As String) As DirectoryInfo
            Dim currentDir = GetRootDirectory().FullName
            Return New DirectoryInfo(Path.Combine(currentDir, directory, subDirectory))
        End Function
    End Class
End Namespace
