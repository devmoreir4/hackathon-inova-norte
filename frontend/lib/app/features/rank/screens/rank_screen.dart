import 'package:flutter/material.dart';
// import 'package:frontend/app/data/services/gamification_service.dart'; // Não será mais usado para dados fictícios
// import 'dart:convert'; // Não será mais usado para dados fictícios

// Modelo para a entrada do leaderboard
class LeaderboardEntry {
  final int userId;
  final String username;
  final int totalPoints;

  LeaderboardEntry({
    required this.userId,
    required this.username,
    required this.totalPoints,
  });

  // Não precisamos mais do fromJson se os dados são fictícios
  // factory LeaderboardEntry.fromJson(Map<String, dynamic> json) {
  //   return LeaderboardEntry(
  //     userId: json['user_id'],
  //     username: json['username'] as String?,
  //     totalPoints: json['total_points'] as int?,
  //   );
  // })
}

class RankScreen extends StatefulWidget {
  const RankScreen({super.key});

  @override
  State<RankScreen> createState() => _RankScreenState();
}

class _RankScreenState extends State<RankScreen> {
  // final GamificationService _gamificationService = GamificationService(); // Não será mais usado
  List<LeaderboardEntry> _leaderboard = [];
  // bool _isLoading = true; // Não será mais usado
  // String _errorMessage = ''; // Não será mais usado

  final int _currentUserId = 999; // ID fictício do usuário atual

  @override
  void initState() {
    super.initState();
    _generateFictitiousLeaderboard();
  }

  void _generateFictitiousLeaderboard() {
    setState(() {
      _leaderboard = [
        LeaderboardEntry(userId: 1, username: 'João Silva', totalPoints: 1500),
        LeaderboardEntry(userId: 2, username: 'Maria Souza', totalPoints: 1200),
        LeaderboardEntry(userId: _currentUserId, username: 'Ana Silva', totalPoints: 1000), // Usuário em 3º
        LeaderboardEntry(userId: 3, username: 'Carlos Santos', totalPoints: 950),
        LeaderboardEntry(userId: 4, username: 'Ana Paula', totalPoints: 800),
        LeaderboardEntry(userId: 5, username: 'Pedro Henrique', totalPoints: 750),
        LeaderboardEntry(userId: 6, username: 'Juliana Costa', totalPoints: 600),
        LeaderboardEntry(userId: 7, username: 'Fernando Lima', totalPoints: 550),
        LeaderboardEntry(userId: 8, username: 'Patrícia Almeida', totalPoints: 400),
        LeaderboardEntry(userId: 9, username: 'Roberto Dias', totalPoints: 300),
      ];
      // _isLoading = false; // Não será mais usado
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ranking'),
        backgroundColor: const Color(0xFF04575c),
      ),
      body: Container(
        color: const Color(0xFF04575c),
        child: Column(
          children: [
            // Cabeçalho do Ranking
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
              child: Row(
                children: [
                  SizedBox(
                    width: 40,
                    child: Text(
                      '#',
                      style: TextStyle(color: Colors.white.withOpacity(0.7), fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Text(
                      'Nome',
                      style: TextStyle(color: Colors.white.withOpacity(0.7), fontWeight: FontWeight.bold),
                    ),
                  ),
                  Text(
                    'Pontos',
                    style: TextStyle(color: Colors.white.withOpacity(0.7), fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(8.0),
                itemCount: _leaderboard.length,
                itemBuilder: (context, index) {
                  final entry = _leaderboard[index];
                  final isCurrentUser = entry.userId == _currentUserId;

                  Widget leadingWidget;
                  Color crownColor;

                  if (index == 0) {
                    crownColor = Colors.amber; // Ouro
                  } else if (index == 1) {
                    crownColor = Colors.grey; // Prata
                  } else if (index == 2) {
                    crownColor = Colors.brown; // Bronze
                  } else {
                    crownColor = Colors.transparent; // Não usado para os demais
                  }

                  if (index < 3) { // Para os 3 primeiros lugares
                    leadingWidget = Stack(
                      alignment: Alignment.center,
                      children: [
                        Icon(Icons.emoji_events, color: crownColor, size: 40), // Ícone da taça maior
                        Positioned(
                          top: 8, // Ajustar este valor para mover o texto para cima/baixo
                          child: Text(
                            '${index + 1}',
                            style: const TextStyle(
                              color: Colors.white, // Letra branca para todos os 3 primeiros
                              fontWeight: FontWeight.bold,
                              fontSize: 12,
                            ),
                          ),
                        ),
                      ],
                    );
                  } else { // Para os demais
                    leadingWidget = CircleAvatar(
                      backgroundColor: isCurrentUser ? Colors.white : const Color(0xFF98CE00),
                      child: Text(
                        '${index + 1}',
                        style: TextStyle(
                          color: isCurrentUser ? const Color(0xFF003C44) : Colors.black,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    );
                  }

                  return Card(
                    color: isCurrentUser ? const Color(0xFF98CE00) : const Color(0xFF003C44),
                    margin: const EdgeInsets.symmetric(vertical: 4.0),
                    elevation: isCurrentUser ? 8 : 2,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                      side: isCurrentUser ? const BorderSide(color: Colors.white, width: 2) : BorderSide.none,
                    ),
                    child: ListTile(
                      leading: leadingWidget,
                      title: Text(
                        entry.username,
                        style: TextStyle(
                          color: isCurrentUser ? const Color(0xFF003C44) : Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      trailing: Text(
                        '${entry.totalPoints} pts',
                        style: TextStyle(
                          color: isCurrentUser ? const Color(0xFF003C44) : Colors.white,
                          fontSize: 16,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}