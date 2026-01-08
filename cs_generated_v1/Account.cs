```csharp
namespace Accounts
{
    public class Account
    {
        public string AccountNumber { get; set; }
        public decimal Balance { get; set; }

        public Account(string accountNumber, decimal initialBalance)
        {
            this.AccountNumber = accountNumber;
            this.Balance = initialBalance;
        }

        public void Credit(decimal amount)
        {
            this.Balance += amount;
        }

        public void Debit(decimal amount)
        {
            this.Balance -= amount;
        }
    }
}
```