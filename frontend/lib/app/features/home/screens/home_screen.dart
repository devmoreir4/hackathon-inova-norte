import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF004A5A),

        title: Image.asset('assets/logo.png'),

        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 6),
            child: IconButton(
              onPressed: () {},
              icon: Image.asset('assets/profile.png'),
            ),
          ),

          IconButton(
            onPressed: () {},
            icon: const Icon(
              Icons.notifications_none_outlined,
              color: Colors.white,
              size: 28,
            ),
          ),

          IconButton(
            onPressed: () {},
            icon: const Icon(
              Icons.logout,
              color: Colors.white,
              size: 28,
            ),
          ),
          const SizedBox(width: 8),
        ],
      ),
    );
  }
}