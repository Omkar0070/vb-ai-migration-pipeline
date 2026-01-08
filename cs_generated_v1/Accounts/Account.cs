namespace Accounts
{
    public class Account
    {
        public string AccountNumber { get; set; }
        public decimal Balance { get; set; }

        public Account(string accountNumber, decimal initialBalance)
        {
            AccountNumber = accountNumber;
            Balance = initialBalance;
        }

        public void Credit(decimal amount)
        {
            Balance += amount;
        }

        public void Debit(decimal amount)
        {
            Balance -= amount;
        }
    }
}