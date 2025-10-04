import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/app/data/models/user.dart';

class UserService {
  final String _baseUrl = 'http://192.168.1.7:5000/api/v1'; // Adjust if your API is hosted elsewhere

  Future<User> getUser(int userId) async {
    final response = await http.get(Uri.parse('$_baseUrl/users/$userId'));

    if (response.statusCode == 200) {
      return User.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load user');
    }
  }
}
