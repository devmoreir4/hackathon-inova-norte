
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/app/data/models/community.dart';

class CommunityService {
  // TODO: Replace with your actual backend URL
  final String _baseUrl = 'http://192.168.1:5000/api/v1'; //ADD your address ip 

  Future<List<Community>> getCommunities() async {
    final response = await http.get(Uri.parse('$_baseUrl/communities'));

    if (response.statusCode == 200) {
      List<dynamic> body = jsonDecode(utf8.decode(response.bodyBytes));
      List<Community> communities = body
          .map((dynamic item) => Community.fromJson(item))
          .toList();
      return communities;
    } else {
      throw Exception('Failed to load communities');
    }
  }
}
