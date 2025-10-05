import 'dart:convert';
import 'package:http/http.dart' as http;

class RagChatService {
  // TODO: Replace with your actual backend URL
  final String _baseUrl = 'http://192.168.1.7:5000/api/v1'; // Adjust if your API is hosted elsewhere

  Future<Map<String, dynamic>> sendMessage(String message, String sessionId) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/rag/chat'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'message': message, 'session_id': sessionId}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(utf8.decode(response.bodyBytes));
    } else {
      throw Exception('Failed to send message to RAG service: ${response.statusCode} - ${response.body}');
    }
  }

  Future<Map<String, dynamic>> getStatus() async {
    final response = await http.get(Uri.parse('$_baseUrl/rag/status'));

    if (response.statusCode == 200) {
      return jsonDecode(utf8.decode(response.bodyBytes));
    } else {
      throw Exception('Failed to get RAG service status: ${response.statusCode} - ${response.body}');
    }
  }
}
