Namespace Accounts

Public Class Account

    Public Property AccountNumber As String
    Public Property Balance As Decimal

    Public Sub New(accountNumber As String, initialBalance As Decimal)
        Me.AccountNumber = accountNumber
        Me.Balance = initialBalance
    End Sub

    Public Sub Credit(amount As Decimal)
        Me.Balance += amount
    End Sub

    Public Sub Debit(amount As Decimal)
        Me.Balance -= amount
    End Sub

End Class

End Namespace
