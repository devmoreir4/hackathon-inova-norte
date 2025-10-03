
import 'package:flutter/material.dart';
import 'package:frontend/app/core/widgets/app_drawer.dart';
import 'package:frontend/app/data/models/transaction.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF003641), // Dark teal background
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Image.asset('assets/logo.png', height: 80),
        actions: [
          Builder(
            builder: (context) => IconButton(
              icon: const Icon(Icons.menu, color: Colors.white),
              onPressed: () => Scaffold.of(context).openEndDrawer(),
            ),
          ),
        ],
      ),
      endDrawer: const AppDrawer(), // Use endDrawer to open from the right
      body: Column(
        children: [
          _BalanceCard(),
          _ActionButtons(),
          const SizedBox(height: 24),
          Expanded(
            child: Container(
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(30),
                  topRight: Radius.circular(30),
                ),
              ),
              child: _TransactionList(),
            ),
          )
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: const Color(0xFF003641),
        selectedItemColor: const Color(0xFF93C83E),
        unselectedItemColor: Colors.white,
        currentIndex: 0,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home_filled), // Changed to filled icon
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.credit_card),
            label: 'Cartões',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bar_chart),
            label: 'Investir',
          ),
        ],
      ),
    );
  }
}

class _BalanceCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Saldo disponível',
            style: TextStyle(color: Colors.white, fontSize: 16),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'R\$ 2.546,30',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Icon(Icons.visibility_off_outlined, color: Colors.white),
            ],
          ),
        ],
      ),
    );
  }
}

class _ActionButtons extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _ActionButton(icon: Icons.pix, label: 'Pix'),
          _ActionButton(icon: Icons.qr_code_scanner, label: 'Pagar'),
          _ActionButton(icon: Icons.receipt_long, label: 'Extrato'),
          _ActionButton(icon: Icons.swap_horiz, label: 'Transferir'),
        ],
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  final IconData icon;
  final String label;

  const _ActionButton({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFF93C83E), // Lime green
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: const Color(0xFF003641), size: 32),
        ),
        const SizedBox(height: 8),
        Text(label, style: const TextStyle(color: Colors.white)),
      ],
    );
  }
}

class _TransactionList extends StatelessWidget {
  final List<Transaction> transactions = [
    Transaction(
        dateDay: '19', dateMonth: 'Jun', description: 'Pix Enviado', author: 'Carlos Rogério',
        amount: 'R\$ 36,50', time: '9:12', isDebit: true),
    Transaction(
        dateDay: '16', dateMonth: 'Jun', description: 'Pix recebido', author: 'José da Silva',
        amount: 'R\$ 536,45', time: '12:26'),
    Transaction(
        dateDay: '10', dateMonth: 'Jun', description: 'Déb. finan. veículo', author: 'Doc. 6652189',
        amount: 'R\$ 984,78', time: '8:00', isDebit: true),
    Transaction(
        dateDay: '06', dateMonth: 'Jun', description: 'Transfer. recebida', author: 'outra if',
        amount: 'R\$ 2.650,78', time: '16:56'),
  ];

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(24.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Histórico da conta', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              Text('Junho ⌄', style: TextStyle(fontSize: 16, color: Colors.grey[600])),
            ],
          ),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: transactions.length,
            itemBuilder: (context, index) {
              return _TransactionListItem(transaction: transactions[index]);
            },
          ),
        ),
      ],
    );
  }
}

class _TransactionListItem extends StatelessWidget {
  final Transaction transaction;

  const _TransactionListItem({required this.transaction});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      child: Row(
        children: [
          Column(
            children: [
              Text(transaction.dateDay, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              Text(transaction.dateMonth, style: TextStyle(color: Colors.grey[600])),
            ],
          ),
          const SizedBox(width: 16),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(transaction.description, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              Text(transaction.author, style: TextStyle(color: Colors.grey[600])),
            ],
          ),
          const Spacer(),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                (transaction.isDebit ? '-' : '+') + transaction.amount,
                style: TextStyle(
                  color: transaction.isDebit ? Colors.red : Colors.green,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(transaction.time, style: TextStyle(color: Colors.grey[600])),
            ],
          ),
        ],
      ),
    );
  }
}
