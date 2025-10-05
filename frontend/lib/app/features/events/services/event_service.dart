import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/app/features/events/models/event.dart';

class EventService {
  final String _baseUrl = 'http://192.168.1.7:5000/api/v1'; // Using the correct IP and port

  Future<List<Event>> getEventsForMonth(int year, int month) async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/events/calendar/month/$year/$month'));

      if (response.statusCode == 200) {
        List<dynamic> body = json.decode(utf8.decode(response.bodyBytes));
        List<Event> events = body.map((dynamic item) => Event.fromJson(item)).toList();
        return events;
      } else {
        throw Exception('Failed to load events for month. Status code: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to load events: $e');
    }
  }

  Future<void> registerForEvent(int eventId, int userId) async {
    try {
      // The backend endpoint for registration seems to take user_id as a query param
      // and an empty body. Let's adjust if needed.
      final response = await http.post(
        Uri.parse('$_baseUrl/events/$eventId/register?user_id=$userId'),
        headers: {'Content-Type': 'application/json'},
        // The DTO EventRegistrationCreate is empty, so an empty body is likely correct.
        body: json.encode({}),
      );

      if (response.statusCode != 201) {
        // Try to parse error message from backend if available
        String detail = response.body;
        try {
          final decoded = json.decode(response.body);
          detail = decoded['detail'] ?? detail;
        } catch (_) {}
        throw Exception('Failed to register for event. Status: ${response.statusCode}, Detail: $detail');
      }
    } catch (e) {
      throw Exception('Failed to register for event: $e');
    }
  }
}
