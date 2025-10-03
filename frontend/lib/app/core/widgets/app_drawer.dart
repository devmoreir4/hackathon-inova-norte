
import 'package:flutter/material.dart';
import 'package:frontend/app/features/auth/screens/login_screen.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF003641),
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          _buildDrawerHeader(),
          _buildDrawerItem(icon: Icons.home, text: 'Início', onTap: () => Navigator.pop(context)),
          _buildDrawerItem(icon: Icons.credit_card, text: 'Cartões', onTap: () {}),
          _buildDrawerItem(icon: Icons.pix, text: 'Pix', onTap: () {}),
          _buildDrawerItem(icon: Icons.bar_chart, text: 'Investimentos', onTap: () {}),
          const Divider(color: Color(0xFF004B44)),
          _buildDrawerItem(
            icon: Icons.exit_to_app, 
            text: 'Sair', 
            onTap: () {
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute(builder: (context) => const LoginScreen()), 
                (Route<dynamic> route) => false,
              );
            }
          ),
        ],
      ),
    );
  }

  Widget _buildDrawerHeader() {
    return const UserAccountsDrawerHeader(
      accountName: Text('Leonardo Marino', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      accountEmail: Text('Ag: 3007  CC: 16.598-3'),
      currentAccountPicture: CircleAvatar(
        backgroundColor: Color(0xFF004B44),
        child: Icon(Icons.person, color: Colors.white, size: 40),
      ),
      decoration: BoxDecoration(
        color: Color(0xFF004B44),
      ),
    );
  }

  Widget _buildDrawerItem({required IconData icon, required String text, required GestureTapCallback onTap}) {
    return ListTile(
      leading: Icon(icon, color: Colors.white),
      title: Text(text, style: const TextStyle(color: Colors.white, fontSize: 16)),
      onTap: onTap,
    );
  }
}
