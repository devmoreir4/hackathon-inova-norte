import 'package:flutter/material.dart';
import 'package:frontend/app/features/community/screens/forum_tab.dart';
import 'package:frontend/app/features/community/screens/cursos_tab.dart';
import 'package:frontend/app/features/community/screens/eventos_tab.dart';

class CommunityScreen extends StatefulWidget {
  const CommunityScreen({super.key});

  @override
  State<CommunityScreen> createState() => _CommunityScreenState();
}

class _CommunityScreenState extends State<CommunityScreen> {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3, // Fórum, Cursos, Eventos
      child: Scaffold(
        backgroundColor: const Color(0xFF04575c), // Cor de fundo do chat
        appBar: AppBar(
          title: const Text('Comunidade'),
          backgroundColor: const Color(0xFF04575c), // Cor de fundo do chat
          bottom: const TabBar(
            indicatorColor: Colors.white,
            labelColor: Colors.white,
            unselectedLabelColor: Colors.white70,
            tabs: [
              Tab(text: 'Fórum'),
              Tab(text: 'Cursos'),
              Tab(text: 'Eventos'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            ForumTab(),
            CursosTab(),
            EventosTab(),
          ],
        ),
      ),
    );
  }
}