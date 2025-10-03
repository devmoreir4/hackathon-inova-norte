
class Transaction {
  final String dateDay;
  final String dateMonth;
  final String description;
  final String author;
  final String amount;
  final String time;
  final bool isDebit;

  Transaction({
    required this.dateDay,
    required this.dateMonth,
    required this.description,
    required this.author,
    required this.amount,
    required this.time,
    this.isDebit = false,
  });
}
