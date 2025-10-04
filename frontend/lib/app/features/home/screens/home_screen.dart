import 'package:flutter/material.dart';
import 'package:frontend/app/core/widgets/geometric_background.dart';
import 'package:frontend/app/features/community/screens/forum_tab.dart';
import 'package:frontend/app/features/home/screens/home_tab.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  static const List<Widget> _screens = <Widget>[
    HomeTab(),
    Center(child: Text('Extrato Screen')),
    Center(child: Text('Cartões Screen')),
    Center(child: Text('Pix Screen')),
    ForumTab(),
    Center(child: Text('Menu Screen')),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: const Color(0xFF003C44),
          title: Image.asset(
            'assets/logo.png',
            width: 100,
          ),
          actions: [
            IconButton(
              onPressed: () {},
              icon: const Icon(
                Icons.chat_bubble_outline,
                color: Colors.white,
              ),
            ),
            IconButton(
              onPressed: () {},
              icon: const Icon(
                Icons.notifications_none_outlined,
                color: Colors.white,
              ),
            ),
            IconButton(
              onPressed: () {},
              icon: const Icon(
                Icons.logout,
                color: Colors.white,
              ),
            ),
          ],
          bottom: _selectedIndex == 4
              ? const TabBar(
                  tabs: [
                    Tab(text: 'Fórum'),
                    Tab(text: 'Aulas'),
                    Tab(text: 'Calendário'),
                  ],
                )
              : null,
        ),
        body: GeometricBackground(
          child: IndexedStack(
            index: _selectedIndex,
            children: _screens,
          ),
        ),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _selectedIndex,
          onTap: _onItemTapped,
          type: BottomNavigationBarType.fixed,
          backgroundColor: Colors.white,
          selectedItemColor: const Color(0xFF007A8D),
          unselectedItemColor: Colors.grey,
          items: [
            const BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: 'Home',
            ),
            const BottomNavigationBarItem(
              icon: Icon(Icons.receipt_long),
              label: 'Extrato',
            ),
            const BottomNavigationBarItem(
              icon: Icon(Icons.credit_card),
              label: 'Cartões',
            ),
            const BottomNavigationBarItem(
              icon: Icon(Icons.pix),
              label: 'Pix',
            ),
            BottomNavigationBarItem(
              icon: Stack(
                children: [
                  const Icon(Icons.people),
                  Positioned(
                    right: 0,
                    child: Container(
                      padding: const EdgeInsets.all(1),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        borderRadius: BorderRadius.circular(6),
                      ),
                      constraints: const BoxConstraints(
                        minWidth: 12,
                        minHeight: 12,
                      ),
                      child: const Text(
                        '1',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 8,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
                ],
              ),
              label: 'Comunidade',
            ),
            const BottomNavigationBarItem(
              icon: Icon(Icons.menu),
              label: 'Menu',
            ),
          ],
        ),
      ),
    );
  }
}