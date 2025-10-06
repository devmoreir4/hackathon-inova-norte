import 'package:flutter/material.dart';
import 'package:frontend/app/features/chat/screens/chat_screen.dart';
import 'package:frontend/app/features/community/screens/community_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _showBalance = true;
  int _selectedIndex = 0;

  static final List<Widget> _widgetOptions = <Widget>[
    const _HomeContent(),
    const ChatScreen(),
    const CommunityScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: _selectedIndex == 0 ? AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: Padding(
          padding: const EdgeInsets.only(left: 16.0),
          child: Image.asset(
            'assets/logo.png',
            height: 200,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.menu, color: Colors.white),
            onPressed: () {
              // Ação do menu
            },
          ),
        ],
      ) : null,
      body: IndexedStack(
        index: _selectedIndex,
        children: _widgetOptions,
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: const Color(0xFF00252E),
        selectedItemColor: const Color(0xFF98CE00),
        unselectedItemColor: Colors.white70,
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.chat),
            label: 'Chat',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Comunidade',
          ),
        ],
      ),
    );
  }
}

class _HomeContent extends StatefulWidget {
  const _HomeContent({super.key});

  @override
  State<_HomeContent> createState() => _HomeContentState();
}

class _HomeContentState extends State<_HomeContent> {
  bool _showBalance = true;

  @override
  Widget build(BuildContext context) {
    return Container(
      color: const Color(0xFF003C44),
      child: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Separador da AppBar
              Container(
                height: 2.0,
                color: const Color(0xFF001A22),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Card de Saldo Disponível
                    Container(
                      padding: const EdgeInsets.all(16.0),
                      decoration: BoxDecoration(
                        color: const Color(0xFF072C30), // Background do card de saldo sólido
                        borderRadius: BorderRadius.circular(10),
                        // Removida a boxShadow
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Saldo disponível',
                            style: TextStyle(color: Colors.white, fontSize: 16), // Texto branco
                          ),
                          const SizedBox(height: 8),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                _showBalance ? 'R\$ 2.546,30' : 'R\$ ****,**',
                                style: const TextStyle(
                                  color: Color(0xFF75C044), // Cor dos números do saldo
                                  fontSize: 28,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              IconButton(
                                icon: Icon(
                                  _showBalance ? Icons.visibility : Icons.visibility_off,
                                  color: Colors.white, // Ícone branco
                                ),
                                onPressed: () {
                                  setState(() {
                                    _showBalance = !_showBalance;
                                  });
                                },
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16), // Espaçamento entre os cards
                    // Card de Lançamentos Futuros (Restaurado)
                    InkWell(
                      onTap: () {
                        // Ação para lançamentos futuros
                      },
                      child: Container(
                        padding: const EdgeInsets.all(16.0),
                        decoration: BoxDecoration(
                          color: const Color(0xFF072C30), // Mesma cor do card de saldo
                          borderRadius: BorderRadius.circular(10),
                          // Removida a boxShadow
                        ),
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Lançamentos futuros',
                                  style: TextStyle(color: Colors.white70, fontSize: 16),
                                ),
                                SizedBox(height: 4),
                                Text(
                                  '-R\$ 2.419,13',
                                  style: TextStyle(
                                    color: Colors.redAccent,
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                            Icon(Icons.arrow_forward_ios, color: Colors.white, size: 20),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildActionButton(Icons.pix, 'Pix'),
                    _buildActionButton(Icons.qr_code_scanner, 'Pagar'),
                    _buildActionButton(Icons.description, 'Extrato'),
                    _buildActionButton(Icons.attach_money, 'Transferir'),
                  ],
                ),
              ),
              const SizedBox(height: 20),
              // Seção de Histórico da Conta
              Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  color: const Color(0xFFF7F6F7),
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(30),
                    topRight: Radius.circular(30),
                  ),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Histórico da conta',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.black87,
                            ),
                          ),
                          InkWell(
                            onTap: () {
                              // Ação para selecionar o mês
                            },
                            child: const Row(
                              children: [
                                Text(
                                  'Junho',
                                  style: TextStyle(
                                    fontSize: 16,
                                    color: Colors.black54,
                                  ),
                                ),
                                Icon(Icons.arrow_drop_down, color: Colors.black54),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      _buildTransactionList(),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildActionButton(IconData icon, String text) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4.0),
        child: InkWell(
          onTap: () {
            // Ação do botão
          },
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 10.0),
            decoration: BoxDecoration(
              color: const Color(0xFF75C044),
              borderRadius: BorderRadius.circular(10),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.2),
                  spreadRadius: 1,
                  blurRadius: 3,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(icon, color: Colors.white, size: 30),
                const SizedBox(height: 5),
                Text(
                  text,
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTransactionList() {
    final List<Map<String, dynamic>> transactions = [
      {
        'date': '19 Jun',
        'type': 'Pix Enviado',
        'description': 'Para João Silva',
        'value': -150.00,
        'time': '14:30',
      },
      {
        'date': '18 Jun',
        'type': 'Salário',
        'description': 'Pagamento mensal',
        'value': 2500.00,
        'time': '09:00',
      },
      {
        'date': '17 Jun',
        'type': 'Pagamento Boleto',
        'description': 'Conta de Luz',
        'value': -120.50,
        'time': '17:45',
      },
      {
        'date': '17 Jun',
        'type': 'Pix Recebido',
        'description': 'De Maria Souza',
        'value': 50.00,
        'time': '10:15',
      },
      {
        'date': '16 Jun',
        'type': 'Transferência',
        'description': 'Para Carlos Santos',
        'value': -300.00,
        'time': '11:00',
      },
      {
        'date': '15 Jun',
        'type': 'Compras',
        'description': 'Supermercado',
        'value': -85.70,
        'time': '19:20',
      },
    ];

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: transactions.length,
      itemBuilder: (context, index) {
        final transaction = transactions[index];
        final isNegative = transaction['value'] < 0;
        final valueColor = isNegative ? Colors.red : Colors.green;

        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(
                width: 60,
                child: Text(
                  transaction['date'],
                  style: const TextStyle(color: Colors.black54, fontSize: 14),
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      transaction['type'],
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                        color: Colors.black87,
                      ),
                    ),
                    Text(
                      transaction['description'],
                      style: const TextStyle(color: Colors.black54, fontSize: 14),
                    ),
                  ],
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    'R\$ ${transaction['value'].toStringAsFixed(2)}',
                    style: TextStyle(
                      color: valueColor,
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  ),
                  Text(
                    transaction['time'],
                    style: const TextStyle(color: Colors.black54, fontSize: 12),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}
