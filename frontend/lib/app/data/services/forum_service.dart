import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/app/data/models/post.dart';

class ForumService {
  final String _baseUrl = 'http://192.168.1.7:5000/api/v1'; // Adjust if your API is hosted elsewhere

  Future<List<Post>> getPosts() async {
    final response = await http.get(Uri.parse('$_baseUrl/forum/posts'));

    if (response.statusCode == 200) {
      List<dynamic> body = jsonDecode(response.body);
      List<Post> posts = body.map((dynamic item) => Post.fromJson(item)).toList();
      return posts;
    } else {
      throw Exception('Failed to load posts');
    }
  }
}
