import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/app/features/rank/screens/rank_screen.dart'; // Importar LeaderboardEntry

class GamificationService {
  final String _baseUrl = 'http://192.168.1.7:5000/api/v1'; // Base URL consistente com ForumService

  Future<List<LeaderboardEntry>> getLeaderboard() async {
    final response = await http.get(Uri.parse('$_baseUrl/gamification/leaderboard'));

    if (response.statusCode == 200) {
      List<dynamic> body = jsonDecode(response.body);
      List<LeaderboardEntry> leaderboard = body.map((dynamic item) => LeaderboardEntry.fromJson(item)).toList();
      return leaderboard;
    } else {
      throw Exception('Failed to load leaderboard');
    }
  }
}