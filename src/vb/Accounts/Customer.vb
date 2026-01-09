Namespace Banking

    Public Class Customer

        Public Property CustomerId As Integer
        Public Property Name As String
        Public Property Balance As Decimal

        Public Sub New(id As Integer, name As String, initialBalance As Decimal)
            CustomerId = id
            Me.Name = name
            Balance = initialBalance
        End Sub

        Public Sub Deposit(amount As Decimal)
            If amount <= 0 Then
                Throw New ArgumentException("Deposit amount must be greater than zero")
            End If

            Balance += amount
        End Sub

        Public Sub Withdraw(amount As Decimal)
            If amount <= 0 Then
                Throw New ArgumentException("Withdraw amount must be greater than zero")
            End If

            If amount > Balance Then
                Throw New InvalidOperationException("Insufficient balance")
            End If

            Balance -= amount
        End Sub

        Public Function GetSummary() As String
            Return $"Customer {CustomerId}: {Name}, Balance = {Balance}"
        End Function

    End Class

End Namespace
