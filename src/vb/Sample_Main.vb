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
Imports System.Threading.Tasks

Namespace EPPlusSamples
    Public Class Sample_Main
        Public Shared Sub Main(ByVal args As String())
            MainAsync(args).GetAwaiter().GetResult()
        End Sub

        Private Shared Async Function MainAsync(ByVal args As String()) As Task
            Try
                'EPPlus 5 uses a dual license model. This requires you to specifiy the License you are using to be able to use the library. 
                'This sample sets the LicenseContext in the appsettings.json file. An alternative is the commented row below.
                'ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
                'See https://epplussoftware.com/Developers/LicenseException for more info.

                'Set the output directory to the SampleApp folder where the app is running from. 
                FileUtil.OutputDir = New DirectoryInfo($"{AppDomain.CurrentDomain.BaseDirectory}SampleApp")

                Await WorkbookWorksheetAndRangesSamples.RunAsync()
                Await ImportAndExportSamples.RunAsync()
                StylingBasics.Run()
                ConditionalFormattingSamples.Run()

                Await FiltersAndValidation.RunAsync()
                Await DrawingsChartsAndThemesSample.RunAsync()

                FormulaCalculationSample.Run()
                Await TablesPivotTableAndSlicersSample.RunAsync()
                EncryptionProtectionAndVBASample.Run()

                ConnectionsAndQueryTableSample.Run()
            Catch ex As Exception
                Console.WriteLine("Error: {0}", ex.Message)
            End Try
            Dim prevColor = Console.ForegroundColor
            Console.ForegroundColor = ConsoleColor.Green
            Console.WriteLine($"Genereted sample workbooks can be found in {FileUtil.OutputDir.FullName}")
            Console.ForegroundColor = prevColor

            Console.WriteLine()
            Console.WriteLine("Press the return key to exit...")

            Console.ReadKey()
        End Function
    End Class
End Namespace
