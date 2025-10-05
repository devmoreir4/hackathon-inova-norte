import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/app/features/courses/models/course.dart';

class CourseService {
  // TODO: Replace with your actual backend URL
  final String _baseUrl = 'http://192.168.1.7:5000';

  Future<List<Course>> fetchCourses() async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/api/v1/courses'));

      if (response.statusCode == 200) {
        List<dynamic> body = json.decode(utf8.decode(response.bodyBytes));
        List<Course> courses = body.map((dynamic item) => Course.fromJson(item)).toList();
        return courses;
      } else {
        // Consider logging the error body for debugging
        throw Exception('Failed to load courses. Status code: ${response.statusCode}');
      }
    } catch (e) {
      // Consider logging the exception for debugging
      throw Exception('Failed to load courses: $e');
    }
  }
}
